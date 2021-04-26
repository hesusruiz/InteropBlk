import json
import sqlite3

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util import logging
from docutils.parsers.rst import roles
from sphinx.addnodes import pending_xref
import requests

zot_url = "http://localhost:23119/better-bibtex/json-rpc"

target_file_name = "references.html"
references_file = "bibliography_list.result"

logger = logging.getLogger(__name__)

db = sqlite3.connect('bibliography.sqlite')
db.row_factory = sqlite3.Row

# Get all the keys in all the documents in order of appearance
citeKeys = []

def citep(role, rawtext, text, lineno, inliner,
                       options={}, content=[]):

    # Check if the citekey exists in the bibliograpy database
    r = db.execute(
        'SELECT * FROM biblio WHERE citekey = ?', (text,)
    ).fetchone()

    if not r:
        logger.warn(f"Citekey {text} does not exist: {inliner.document['source']} line {lineno}")
        # Just do nothing
        return [], []

    # Add the key to the array if it is not already there
    # We use an array to keep the order of appearance
    if text not in citeKeys:
        citeKeys.append(text)

        # Write the bibliography item to the file
        with open(references_file, "a", encoding="utf8") as f:
            order = citeKeys.index(text) + 1

            author = r["author"]
            title = r["title"]
            publication = r["publication"]
            year = r["year"]

            line = f".. _citep{order}:\n\n" + \
                "[" + str(order) + "] " + \
                author + ', ' + \
                '*' + title + '*'
            if publication:
                line = line + ", " + publication
            if year:
                line = line + ", " + year
            line = line + ".\n\n"

            f.write(line)


    # Get the order of appearance of the key in the whole set of documents
    # Starting by 1
    order = citeKeys.index(text) + 1

    # Build the reference node, pointing to the target node that will be built later
    # when creating the bibliography
    show_text = f"[{order}]"
    refid = f"{target_file_name}#citep{order}"
    refname = f"citep{order}"
    print(f"Role: {refname}")
    reference = nodes.reference(
        '',
        show_text,
        internal=False,
        refuri=refid,
#        refname=refname,
        classes=['citep']
    )

    # Return the nodes to be added to the TOCTREE
    return [reference], []


class HelloWorld(Directive):

    def run(self):

        # Write a file with the bibliography using the collected keys

        # Build the payload to call Zotero with the citeKeys
        payload = {
            "jsonrpc": "2.0",
            "method": "item.bibliography"
        }

        payload["params"] = [
            citeKeys,
            {
                "id": "http://www.zotero.org/styles/ieee",
                "contentType": "text"
            }
        ]

        # Call Zotero. Zotero must be running
        r = requests.post(zot_url, json=payload)

        result = r.json()["result"]
        lines = result.splitlines()
        return_nodes = []
        order = 1

        with open(f"{references_file}", "w", encoding="utf8") as f:

            for line in lines:
                full_line = f".. _citep_{order}:\n\n" + line + "\n\n"
                f.write(full_line)

                refname = f"citep{order}"
                print(f"Biblio: {refname}")
                target_node = nodes.target(
                    '',
                    '',
                    ids = [f"id{order}"],
                    names=[refname]
                )

                paragraph_node = nodes.paragraph(text=line)

                return_nodes.append(target_node)
                return_nodes.append(paragraph_node)


                order = order + 1

            # target_id = "perico_target"
            # target_node = nodes.target('', 'uuuu', refuri="jj", names=["myname"], ids=[target_id])
            # paragraph_node = nodes.paragraph(text="pepe")

            # return_nodes.append(target_node)

        return return_nodes


def setup(app):

    # Truncate the bibliografy file to re-create it from scratch
    f = open(references_file, "w", encoding="utf8")
    f.close()

    app.add_directive("jrmbibliography", HelloWorld)
    roles.register_canonical_role('citep', citep)


    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

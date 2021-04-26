# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
sys.path.append(os.path.abspath("./_ext"))

# -- Project information -----------------------------------------------------

project = 'InteropBlk'
copyright = '2021, Licensed under a Creative Commons Attribution 4.0 International license'
author = 'Jesus Ruiz'
release = "0.1.0"
version = "0.1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "helloworld",
    "sphinxcontrib.httpdomain",
    "sphinx.ext.graphviz"
]

root_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["docs", ".vscode", "_ext", '_build', 'Thumbs.db', '.DS_Store']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# reStructuredText to include at the end of every source file that is read
# rst_epilog = """
# .. |psf| replace:: Python Software Foundation
# """

# The name of a reST role (builtin or Sphinx extension) to use as the default role, that is, for text marked up `like this`. This can be set to 'py:obj' to make `filter` a cross-reference to the Python function “filter”. The default is None, which doesn’t reassign the default role.
default_role = None

# figures, tables and code-blocks are automatically numbered if they have a caption
numfig = True

# Trim spaces before footnote references that are necessary for the reST parser
trim_footnote_reference_space = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
pygments_style = "default"

html_theme_path = ['sphinx-better-theme']
html_theme = 'better'

html_title = "InteropBlk"
html_short_title = "Home"

html_show_sphinx = False

html_theme_options = {
  # show sidebar on the right instead of on the left
  'rightsidebar': True,

  # inline CSS to insert into the page if you're too lazy to make a
  # separate file
  'inlinecss': '',

  # CSS files to include after all other CSS files
  # (refer to by relative path from conf.py directory, or link to a
  # remote file)
  'cssfiles': ['_static/my_style.css'],  # default is empty list

  # show a big text header with the value of html_title
  'showheader': True,

  # show the breadcrumbs and index|next|previous links at the top of
  # the page
  'showrelbartop': True,
  # same for bottom of the page
  'showrelbarbottom': True,

  # show the self-serving link in the footer
  'linktotheme': False,

  # width of the sidebar. page width is determined by a CSS rule.
  # I prefer to define things in rem because it scales with the
  # global font size rather than pixels or the local font size.
  'sidebarwidth': '15rem',

  # color of all body text
  'textcolor': '#000000',

  # color of all headings (<h1> tags); defaults to the value of
  # textcolor, which is why it's defined here at all.
  'headtextcolor': 'indigo',

  # color of text in the footer, including links; defaults to the
  # value of textcolor
  'footertextcolor': '',

  # Google Analytics info
  'ga_ua': '',
  'ga_domain': '',
}

html_sidebars = {
    '**': ['localtoc.html', 'relations.html', 'searchbox.html'],
    'index': ['indexsidebar.html', 'relations.html', 'searchbox.html'],
    'ssi/introduction': ['indexsidebar.html', 'relations.html', 'searchbox.html'],
}

html_copy_source = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...) 
#html_css_files = [
#]


# -- Options for PDF output -------------------------------------------------

#latex_engine = 'xelatex'

latex_theme = "howto"

latex_elements = {
    "papersize": "a4paper",
    "pointsize": "12pt"
}


latex_additional_files = ["_static\sphinxhowto.cls"]

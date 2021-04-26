
DID Methods for organisations
=============================

The system supports several DID Methods, using the Universal Resolver to resolve each DID into a corresponding DID Document.
This section describes in detail the different DID Methods used by each network.

ELSI DID Method
---------------

In the Alastria Red T we use **ELSI** for juridical persons with identities anchored into a Public-Permissioned blockchain: `did:elsi`.

The name ELSI stands for **E**\ ``TSI`` **L**\ ``egal person`` **S**\ ``emantics`` **I**\ ``dentifier``, because it is based on the *Legal person semantic identifier* defined in the `European Norm ETSI EN 319 412-1 <https://www.etsi.org/deliver/etsi_en/319400_319499/31941201/01.04.02_20/en_31941201v010402a.pdf>`_, related to digital signatures, peer entity authentication, data authentication as well as data confidentiality.

The basic idea is to generate the DID deterministically from an existing and widely accepted identifier, which is already required by any organisation in the real world in order to perform any relevant activity.

The rational for ELSI is the following:

The DID for a juridical person is essentially different to the DID for a natural person.
    Identities of juridical persons are public, together with information associated to the identity. This is not optional, and before an organisation starts performing any relevant operation in the real world, it has to be registered in some official register, where the identity and associated information is publicly acessible.

    However, real-world identities of natural persons and associated PII are subject to very strict privacy regulations (GDPR). Identities are not public, and special care should be taken to keep everything related to the identity private.

    This suggests the need for totally different mechanisms to generate and manage the DIDs of those radically different types of entities. Clean separation of the mechanisms allows for easier implementation of each set of requirements, without polluting the code with logic to handle both cases, which is prone to error.
    Of course, there is nothing preventing reuse of common logic across both implementations, but only when it makes sense and maintaining the clean separation principle.

    In addition, this separation reflects current practice in managing identities of organisations and natural persons, so it is easier to leverage existing know-how.
    
Most organisations can already be identified by the VAT or LEI (or both).
    For example, businesses have to be registered in the Business Registrar of the country of incorporation, including the compulsory Tax Identification Number or VAT. Even organisations which do not require a VAT to be incorporated are required to have a LEI (Legal Entity Identifier).

    Using the VAT and LEI can identify an enormous amount of organisations: businesses, non profits, universities, research centers, public administrations, etc.

    In exceptional cases where VAT or LEI can not be used, ELSI uses the extensibility mechanism in ``ETSI EN 319 412-1`` to include any existing type of compulsory registration, whether international or just national.


These requirements have nothing to do with whether we use centralised technology or blockchains. It is an essential characterictic in any developed economy like the EU.

This means that the creation of the DID is completely decentralised from the point of view of the blockchain networks, because the entities willing to participate already possess everything which is needed in order to create the DID. We do not need to put in place any other entity or system to create the DID.

The ETSI norm on which ELSI is based specifies several possible identifiers that can be used to build the DID. The two most common and the ones used in ELSI are the `VAT` (Tax Identifier) and the `LEI` (`Legal Entity Identifier <https://www.gleif.org>`_).

Using both `VAT` and `LEI` in creating the DID covers every juridical person that can participate in a blockchain network, not only in the EU but in most of the world. In any case, the system is extensible and it is fairly easy to incorporate new legal identifiers if the need arises in the future.

ELSI DID syntax
***************

The ELSI DID Method refers only to legal persons, so we are using the `id-etsi-qcs-SemanticsId-Legal` definition described in Section 5.1 of ETSI EN 319 412-1.

Creating a DID is extremely simple and fully decentralized (does not require participation of any central authority), assuming that the legal person already exists. Its definition using ABNF syntax is:

.. code-block:: abnf

    did = "did:elsi:" id-etsi-qcs-SemanticsId-Legal

Which is the concatenation of the prefix ``did:elsi:`` with the legal person identifier defined in ETSI EN 319 412-1. For the full syntax, please refer to the standards document, but for the two most common basic identifiers (VAT and LEI) the identifier is composed of: 

- 3 character legal person identity type reference, like `VAT` for identification based on a national value added tax identification number or `LEI` for the `Legal Entity Identifier <https://www.gleif.org>`_.
- 2 character ISO 3166 [2] country code;
- hyphen-minus "-" (0x2D (ASCII), U+002D (UTF-8)); and
- identifier (according to country and identity type reference).

Some examples of DIDs are the following:

.. csv-table:: Some example ELSI DIDs
   :header: "Name", "DID"
   :widths: 40, 60

   **AgID** (www.agid.gov.it), **did:elsi:VATIT-97735020584**
   **Hashnet d.o.o.** (hashnet.tech), **did:elsi:VATSI-18035094**
   **Alastria** (alastria.io), **did:elsi:VATES-G87936159**
   **Enel Spa** (www.enel.com), **did:elsi:VATIT-15844561009**
   **Endesa S.A.** (www.endesa.com), **did:elsi:VATES-A81948077**
   **Inter-American Development Bank** (www.iadb.org), **did:elsi:LEIXG-VKU1UKDS9E7LYLMACP54**
   

ELSI DID Document
*****************

An example DID Document is the following:

.. code-block:: json

    {
        "payload": {
            "@context": [
                "https://www.w3.org/ns/did/v1",
                "https://w3id.org/security/v1"
            ],
            "id": "did:elsi:VATES-B60645900",
            "verificationMethod": [
                {
                    "id": "did:elsi:VATES-B60645900#key-verification",
                    "type": "JwsVerificationKey2020",
                    "controller": "did:elsi:VATES-B60645900",
                    "publicKeyJwk": {
                        "kid": "key-verification",
                        "kty": "EC",
                        "crv": "secp256k1",
                        "x": "3K4iNuzPkcrHlEbhHE8vYXlF6K5xGZ2rdOrn3cQ-LnQ",
                        "y": "9Z_l_hQLkq6aLuZz8gheq7R_o5ZUHUlxZ3IBGHsdzaA"
                    }
                }
            ],
            "service": [
                {
                    "id": "did:elsi:VATES-B60645900#info",
                    "type": "EntityCommercialInfo",
                    "serviceEndpoint": "www.in2.es",
                    "name": "IN2 Innovating 2gether"
                },
                {
                    "id": "did:elsi:VATES-B60645900#sms",
                    "type": "SecureMessagingService",
                    "serviceEndpoint": "https://privatecred.hesusruiz.org/api"
                }
            ],
            "anchors": [
                {
                    "id": "redt.alastria",
                    "resolution": "UniversalResolver",
                    "domain": "in2.ala",
                    "ethereumAddress": "0x8CDA8113567e633805e48c87747257E9FFAAdDF5"
                }
            ],
            "created": "2021-02-08T06:53:08Z",
            "updated": "2021-02-08T06:53:08Z"
        }
    }

SI-Chain DID Method
-------------------

.. topic:: TODO

    Specify the details of the DID Method in SI-Chain


IBSI DID Method
---------------

.. topic:: TODO

    Specify the details of the DID Method in IBSI
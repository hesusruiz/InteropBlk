##################################
Verifiable Credentials
##################################

**********
Data Model
**********

The credential uses the standard `W3C Verifiable Credentials Data Model <https://www.w3.org/TR/vc-data-model>`_ for its representation, with some extensions to facilitate interoperability across blockchains.

The specific credential data is encoded in the ``credentialSubject`` field of the VC. The following figure represents the VC structure without the specific credential data.

.. figure:: images/SafeIsland_VCSample.png
    :width: 90%

    W3C Verifiable Credential and extensions


The figure above represents the VC where some fields have been marked:

1. The ``iss`` field (issuer in VC terminology), uses the DID method ``elsi``, specific for juridical persons and explained in a section below.

2. There is an extension to specify the blockchain network (or networks) where the VC can be verified. More precisely, the ``issuedAt`` field of ``credentialSubject`` specifies the networks where the identity for the juridical person that issued the credential can be verified.

   A juridical person can have its `elsi` DID registered in one or more networks, and the same credential can be verified using any of those networks. The trust on the credential depends on the trust on the registration procedure of the identity of the signer. The Verifier entity can choose to verify the credential in whatever network is trusted to the Verifier.

   This mechanism provides a lot of flexibility in interoperability schemes across networks. More details are described in the section on interoperability.


********************************
Example of Verifiable Credential
********************************

.. code-block:: json

    {
        "exp": 1614770844,
        "iat": 1614252444,
        "iss": "did:elsi:VATES-X12345678X",
        "sub": "46106508H",
        "uuid": "829588b3162249d28f3eae5e84349777",
        "vc": {
                "@context": [
                    "https://www.w3.org/2018/credentials/v1",
                    "https://alastria.github.io/identity/credentials/v1",
                    "https://privacycred.org/.well-known/privacycred/v1"
                ],
                "type": [
                    "VerifiableCredential",
                    "AlastriaVerifiableCredential",
                    "PrivacyCredential"
                ],
                "credentialSchema": {
                    "id": "PrivacyCredential",
                    "type": "JsonSchemaValidator2018"
                },
                "credentialSubject": {
                    "privacyCredential": {
                            "citizen": {
                                "dob": "27-04-1982",
                                "idnumber": "46106508H",
                                "name": "COSTA/ALBERTO",
                                "type": "atRisk"
                            },
                            "comments": "These are some comments",
                    },
                    "issuedAt": [
                            "redt.alastria"
                    ],
                    "levelOfAssurance": 2
                }
        }
    }



*******************************
Verification of the credentials
*******************************

In general, verifying a credential received as a JWT involves the following:

1. Deserialize the JWT without verifying it (we do not yet have the public key).
2. Get the ``kid`` property from the header (the JOSE header of the JWT).
3. The ``kid`` has the format did#id where ``did`` is the DID of the issuer and ``id`` is the identifier of the key in the DIDDocument associated to the DID.
4. Perform resolution of the DID of the issuer with the Universal Resolver API.
5. Get the public key specified inside the DIDDocument.
6. Verify the JWT using the public key associated to the DID.
7. Verify that the DID in the ``iss`` field of the JWT payload is the same as the one that signed the JWT.


The system includes two APIs to help client applications with the verification of credentials received from other actors in the ecosystem. The choice of API depends on the trust level of the client application on the server implementing the APIs.

Using the Universal Resolver API
********************************

In the first option the client obtains the public key of the Issuer via DID resolution. Then the client performs the cryptographic verification using the public key, without reliance on any other party.

The API for DID resolution is described below:

.. topic:: DID resolution: get a DID Document from a DID

    .. http:get:: /api/did/v1/identifiers/(string:DID)
        :noindex:

        Resolves a DID and returns the DID Document (JSON format), if it exists.  
        It supports four DID methods: **ebsi**, **elsi**, **ala**, **peer**.

        Only **PEER** and **ELSI** (*https://github.com/hesusruiz/SafeIsland#62-elsi-a-novel-did-method-for-legal-entities*) are directly implemented by this API.
        The others are delegated to be resolved by their respective implementations.

        For example, for **EBSI** we call the corresponding Universal Resolver API, currently in testing and available at
        https://api.ebsi.xyz/did/v1/identifiers/{did}

        :query string DID: The DID to resolve into a DID Document.
        :>json payload didDocument: The DID document associated to the input DID
        :statuscode 200: no error
        :statuscode 404: error resolving the DID
        
        **Example request**:

        .. code-block:: http

            GET /api/did/v1/identifiers/did:elsi:VATES-B60645900 HTTP/1.1
            Host: example.com
            Accept: application/json
        
        **Example response**:

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
    

Delegating verification to a trusted server
*******************************************

In the second option the client delegates to a trusted server the verification of the credential, simplifying the code and complexity of secure cryptographic operatios to the server. This option maybe used when the client trusts the server as it happens when they are operated by the same entity. It can be also used when the server is operated by a public administration and the citizen trusts on it.

This is the easiest one to use, and it is the one requiring higher level of trust. The client app just passes the JWT in the JWS Compact Serialization format (RFC 7519) as the body of a POST request and the server verifies the credential and credential signature using internally the Universal Resolver API for resolving the DID of the Issuer and checking its digital signature. The API is described below:


.. topic:: Verification of a credential server-side

    .. http:post:: /api/verifiable-credential/v1/verifiable-credential-validations
        :noindex:

        Is the easiest one to use and the one requiring higher level of trust. The client app just passes the JWT in the JWS Compact Serialization format (RFC 7519) as the body of a POST request and the server verifies the credential and credential signature using internally the Universal Resolver API for resolving the DID of the Issuer and checking its digital signature.

        :<json JWT credential: The credential in JWT format.
        :>json object claims: The JSON object with the verified claims in the JWT. Otherwise, an error
        :statuscode 200: no error
        :statuscode 404: error resolving the DID




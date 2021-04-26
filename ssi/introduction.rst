############
Introduction
############

This document describes a proposal for a Proof of Concept (PoC) of a very simple interoperability mechanism across applications running in different blockchain networks.
It is based on Verifiable Credentials and it is suitable for a class of applications which are very common in the real world.

The system has the following characteristics.

It does not use digital identities of natural persons or any PII data
    This allows to focus on the technical properties of the system, avoiding the complexities and legal implications associated to the management of PII and crossborder tranfer of that type of data.

    However, it is expected that many pieces of the system could be leveraged in the future for other use cases where PII is involved.

Each network maintains a Trusted List of entities
    Each network has to maintain a list of the entities authorised to issue the certificates used in the PoC. The lists are different for each network, and there is not a requirement to have a global common list for all the networks.

Implementations of the Trusted List can be different in each network, but they have to implement and expose a public API to check identities of the entities in the list and associated public keys.
    In order to verify a certificate issued by an entity in the Trusted List of a given network, the Verifier has to be able to call a public API (non-authenticated) to query the DID of the entity that issued (and signed) the credential. This could be done by using one or two APIs, something to be decided later.

    An implementation with 2 APIs would have:

    1. A general DID Resolution API to get the DID Document of the DID that signed the credential. This is the API for any DID and any certificate.

    2. An API to check if the DID is a member of the Trusted List of entities for this specific certificate.

    Alternatively, the option with a single API would merge the two functionalities into one, and the API would receive a DID and return the DID Document only if the entity is in the Trusted List.

    In any case, the Verifier entity can obtain the public key of the trusted entity that signed the credential (the key is in the DID Document), and verify the credential.

Each Trusted List in each network is managed by a well-known entity which is trusted by the other networks (Root Trusted Entity).
    There is a special entity in each network which is responsible for managing the Trusted List of that network, adding and removing the entities authorised to issue credentials in that network. We will call that entity the Root Trusted Entity of the network. Each network has a different Root Trusted Entity, and each network can implement a different process for managing the Trusted List.

Verifier entities have to trust in the process used to manage the Trusted List in other networks.
    A verifier has to trust that if a DID is in a Trusted List in some network, then the legal entity associated to that DID is authorised to issue certificates, and that all the information in the DID Document is also trusted, including the public key.
    
    This implies that verifiers have to trust that the Root Trusted Entities in each network perform their management tasks in the proper way.
    
Verifiers have to understand the DID Methods implemented by each network.
    Ideally all networks use the same DID Method, even though the DIDs are anchored to different networks. Otherwise, the verifier has to understand all DID Methods of all networks with which it interacts. In the initial implementation of the PoC, it is probably a good idea to try to use one or two DID Methods, to simplify implementation.

The DID Method for juridical entities used in Spain (Alastria Red T) is ELSI
    The DID Method used in Alastria is **ELSI**, which stands for **E**\ ``TSI`` **L**\ ``egal person`` **S**\ ``emantics`` **I**\ ``dentifier``, because it is based on the *Legal person semantic identifier* defined in the `European Norm ETSI EN 319 412-1 <https://www.etsi.org/deliver/etsi_en/319400_319499/31941201/01.04.02_20/en_31941201v010402a.pdf>`_, related to digital signatures, peer entity authentication, data authentication as well as data confidentiality.

    The ELSI DID Method refers only to **legal persons**, and creating a DID is extremely simple and fully decentralized (does not require participation of any central authority), assuming that the legal person already exists in the real world.

    ELSI is described in detail in :doc:`didmethods`

The DID Method for juridical entities used in Slovenia (SI-Chain) is **xxxx**
    TODO

.. topic:: TODO

    We have to specify the DID Method used in IBSI (ideally the same) as in the other networks

The DID Method for juridical entities used in Italy (IBSI) is **xxxx**
    TODO

.. topic:: TODO

    We have to specify the DID Method used in IBSI (ideally the same) as in the other networks


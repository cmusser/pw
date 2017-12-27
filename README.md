# PW: a simple password manager

## Introduction
pw is a system that attempts to keep large collections of passwords secure and accessible. A set of scripts take a single master password to access a password list, and then allow credentials to be searched and managed. Other systems, notably PasswordSafe, by cryptographer Bruce Schneier, are similar. This implementation attempts to leverage recent advances in encryption and key derivation.

## Security
Systems such as pw address the trouble inherent in passwords. Ideally, every credential should have a distinct password, but remembering dozens of them is impractical. The converse (and common) practice of re-using a password for many credentials is convenient, but is insecure. If one username/password combination is recovered, even a not-so-enterprising cracker can attempt to try them out on other popular sites.

The security of pw derives, in part, from the fact that the credential data is only persisted in encrypted form and the key to unlock it is never stored at all. When needed, the key is derived from a master password and a cryptographic salt that was generated when the data was encrypted. Recovering the key is conjectured to be difficult given only the encrypted data file and the salt.

Key generation is done using the "scrypt" key derivation function, by Colin Percival. This intentionally uses large amounts of memory to thwart certain attacks that use large numbers of specialized cracking processors in parallel. The idea is that it's inexpensive to build massively parallel processing machines, but expensive to build such machines with large amounts of memory. The actual encryption is done with NaCl, by Dan Bernstein. The cipher used by NaCl is based on elliptic curves, which provide good security with relatively small key sizes. NaCl uses a particular elliptic curve variant, known as an Edwards curve, which can be computed quickly. Speed is not a concern for this application; rather, NaCl was chosen for the strong security inherent in elliptic curves and its simple API. "pw" enhances security in one other minor way: by default it does not display passwords; instead, it copies them directly to the clipboard for eventual pasting to a destination.

## Installation

pw depends on two external Python packages, PyNaCl and SCrypt. The application itself is a Python package built with setuptools. Installation of PyNaCl is a multi-step operation due to the multiple ways that the underlying libsodium library can be present (or not) on the system. THis make the installation somewhat tedious, which is an area for further refinement.


## Usage
The package installs a number of command-line utilities for managing credentials.

1. `getpw` is for day-to-day credential lookups.
2. `editpw` is used to create or edit credentials and creating new credential databases.
3. `rmpw` is used to remove a credential that you don't need anymore.
4. `dumppw` is an export utility.
5. `chpw` is for changing the master password for a database.
6. `buildpw` takes a plaintext password list in a structured format and creates the encrypted JSON database.

The first five scripts are for normal use. The latter script is a vestige of early development, when I was transitioning from in-the-clear text files and needed to create credential databases. It need not be used; to create a new database, just use `editpw`.


## Implementation

pw is written in Python and the package was built using the setuptools infrastructure. It has an object that represents the credential store, an object that represents an interactive CLI and a helper object that the CLI calls for to get application-specific things done. The package includes scripts based on these objects. The scripts are installed in a bin directory for easy access by users.

The way the objects cooperate is as follows:

- The storage object provides a persistent storage for credentials. It provides a find function, performs encryption and decryption, and takes care of loading and storing the data. This is in stored in a local file, in JSON format, but encrypted.
- The CLI helper object provides some basic actions for a CLI, and is meant to be subclassed by an application for its particular operations. Often, the only method that needs overriding is `process_input()`. The subclass (not an instance of the subclass) is then injected into the CLI object's `run()` method.
- The CLI object provides a generic implementation of CLI application. Most of the action happens in its `run()` method. It creates an instance of the Store object and of the injected CLI helper class, and parses command line arguments. If the name of a credential was specified as an argument, it provides a one-shot process; otherwise it enters an interactive loop. In either case, it calls the CLI Helper's methods for processing input, displaying lists of credentials and other application-specific actions.

Most of the command-line tools leverage all three entities, making them small, simple, and easy to understand. The intent was to eliminate duplicate code. A couple are even simpler, in that they need not provide interactivity or operate directly on the contents of the store. These only make use of the storage object.

Currently, the functionality is CLI oriented, but obviously it's been designed in a way that opens the door to other possibilities, such as GUI applications or remote storage. A larger goal was to have a design that was easy to understand and explain, and unintimidating to modify.

## Future Directions and Other Ideas

For now, the command-line scripts are an acceptable solution. If you have Python, patience, and sysadmin privileges, installation is certainly within your reach, but tedious. Right now, it would fail my very low inconvenience bar for other people's packages, but since I'm the developer, I muddle through on new machines. Most of the trouble involves installing PyNaCl. The NaCl header files need to be present for the Python bindings to be generated, and it's really best to clone the PyNaCl repo and build locally. The version in PIP is older, with rough edges that cause scary (though ultimately innocuous) warnings to be printed in the terminal.

One minor enhancement to the existing `getpw` script would be to zap the password from the clipboard, after a period of time.

Farther down the road, it would be nice to simplify and reduce the dependendies. One possibitity is a Python binding for the newly released TweetNaCl. The binding itself is a separate project, obviously, but it could be used in pw with minimal (maybe no) changes. Another improvement is not having a separate KDF, currently provided by SCrypt. At the time the project was started, NaCl didn't have key-derivation that I was aware of. Maybe it does now, and in any case fewer dependencies is always nice.

## Contributions
Patches, discussion and (perhaps most importantly) analyses of the application's security are all welcome.



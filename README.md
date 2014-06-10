# PW: a simple password manager

## Introduction
pw is a set of command-line scripts that attempts to keep large collections of passwords secure and accessible. A single master password is used to access a password list, and the scripts help with searching for credentials and editing them. Other systems, notably PasswordSafe, by cryptographer Bruce Schneier, are similar. My implementation attempts to leverage recent advance in encryption and key derivation, and served as my entre into Python programming.

## Security
These systems address the trouble inherent in passwords. Having dozens of credentials with distinct passwords increases security, but remembering them all is difficult. The common practice of re-using a password for many credentials is convenient, but is insecure. If one username/password combination is recovered, even a not-so-enterprising cracker can attempt to try them out on other popular sites.

The security of "pw" derives, in part, from the fact that the password list is only persisted in encrypted form and the key to unlock it is never stored at all. When needed, the key is derived from the master password and a cryptographic salt that was generated when the data was encrypted. The presumption is that recovering the key is difficult, given only the encrypted data file and the salt, both of which could be accessible to attackers.

Key generation is done using the "scrypt" key derivation function, by Colin Percival. This intentionally uses large amounts of memory to thwart certain attacks that use large numbers of specialized cracking processors in parallel. The idea is that it's inexpensive to build massively parallel processing machines, but expensive to build such machines with large amounts of memory. With large key in hand, the actual encryption is done with NaCl, by Dan Bernstein. The cipher used by NaCl is based on elliptic curves, which provide good security with relatively small key sizes. NaCl uses a particular elliptic curve variant, known as an Edwards curve, which can be computed quickly. Speed is not a concern for this application; rather, NaCl was chosen for the strong security inherent in elliptic curves and, perhaps more importantly, for its simple, goof-proof API. "pw" enhances security in one other minor way: by default it does not display passwords; instead, it copies them directly to the clipboard for eventual pasting to a destination.

## Implementation
"pw" is implemented as a Python package, currently a few scripts and a library with several modules. All of them operate on the same dataset: a JSON database encrypted. The "pw" script is the one used for day-to-day password lookups. "editpw" is used to create or edit credentials. "buildpw" takes a plaintext password list in a structured format and turns it into the encrypted database. This latter script is only used to get started. The whole point is encryption, so you should discard any plaintext record of your passwords once you start using the system.  The encrypted files can be put on your laptop (the scrypts assume they are in the ~/.pw directory), copied up to a central server and generally made available enough to be useful.

## Future Directions

For now, the rough-n-ready command-line script implementation is acceptable solution because it works on most system with Python. Installing the dependencies is a bit fiddly, which is unfortunate. The NaCl header files need to be present for the Python bindings to be generated, and the Python NaCl code itself has some rough edges that cause scary (though ultimately innocuous) warnings to be printed in the terminal. 

Ultimately, this system would be even more useful if integrated into web browsers, where people spend most of their time. If one assumes that the files are encrypted securely (and I believe they are), they should be suitable for storage in an untrusted environment: cloud drives and so forth. This makes it feasible to build a sync that makes the credentials conveniently available across devices.

One minor enhancement would be to zap the password from the clipboard, after a period of time.


## Contributions
Patches, discussion and (perhaps most importantly) analyses of the application's security are all welcome.



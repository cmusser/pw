# PW: a simple password manager

## Introduction
pw is a set of command-line scripts that attempts to keep large collections of passwords secure and accessible. A single master password is used to access a password list, and the scripts help with searching for credentials and editing them. Other systems, notably PasswordSafe, by cryptographer Bruce Schneier, are similar. My implementation attempts to leverage recent advance in encryption and key derivation, and served as my introduction to Python programming.

## Security
These systems address the trouble inherent in passwords. Ideally, every credential should have a distinct password, but remembering dozens of them is impractical. The common practice of re-using a password for many credentials is convenient, but is insecure. If one username/password combination is recovered, even a not-so-enterprising cracker can attempt to try them out on other popular sites.

The security of "pw" derives, in part, from the fact that the password list is only persisted in encrypted form and the key to unlock it is never stored at all. When needed, the key is derived from the master password and a cryptographic salt that was generated when the data was encrypted. Recovering the key is conjectured to be difficult given only the encrypted data file and the salt.

Key generation is done using the "scrypt" key derivation function, by Colin Percival. This intentionally uses large amounts of memory to thwart certain attacks that use large numbers of specialized cracking processors in parallel. The idea is that it's inexpensive to build massively parallel processing machines, but expensive to build such machines with large amounts of memory. The actual encryption is done with NaCl, by Dan Bernstein. The cipher used by NaCl is based on elliptic curves, which provide good security with relatively small key sizes. NaCl uses a particular elliptic curve variant, known as an Edwards curve, which can be computed quickly. Speed is not a concern for this application; rather, NaCl was chosen for the strong security inherent in elliptic curves and its simple API. "pw" enhances security in one other minor way: by default it does not display passwords; instead, it copies them directly to the clipboard for eventual pasting to a destination.

## Implementation
"pw" is implemented as a Python package, currently a few scripts and a library with several modules. All of them operate on the same dataset: an encrypted JSON database. The "pw" script is the one used for day-to-day password lookups. "editpw" is used to create or edit credentials. "buildpw" takes a plaintext password list in a structured format and turns it into the encrypted database. This latter script is only used to get started. The whole point is encryption, so you should discard any plaintext record of your passwords once you start using the system.  The encrypted files can be put on your laptop (the scripts assume they are in the ~/.pw directory), or even copied up to a central server.

## Future Directions

For now, the rough-n-ready command-line script implementation is an acceptable solution. It works on most system with Python, even if installing the dependencies is a bit fiddly. The NaCl header files need to be present for the Python bindings to be generated, and the Python NaCl code itself has some rough edges that cause scary (though ultimately innocuous) warnings to be printed in the terminal. 

Ultimately, this system would be even more useful if integrated into web browsers, where people spend most of their time. If one assumes that the files are encrypted securely (and I believe they are), they should be suitable for storage in an untrusted environment: a cloud-based service, for instance. This makes it feasible to build a syncing system that makes the credentials conveniently available across devices.

One enhancement would be to zap the password from the clipboard, after a period of time.


## Contributions
Patches, discussion and (perhaps most importantly) analyses of the application's security are all welcome.



# PW: a simple password manager

## Introduction
pw is a pair of command-line scripts that attempts to keep large collections of passwords secure and at least somewhat convenient. A single master password is used to access a password list, and the scripts provide help with searching for a specific credential and copying the password into the clipboard for use. This kind of system is not new. Other systems, notably PasswordSafe, by cryptographer Bruce Schneier, offer similar capabilities. These systems address the difficulties inherent in passwords: having dozens of credentials with distinct passwords increases security, but remembering them all is difficult; re-using a password for many credentials is convenient, but a security disaster. 

## Security
The security of "pw" derives from the fact that the password list is only persisted in encrypted form, and the key to unlock it is never stored at all. When needed, the key is derived from the master password and a cryptographic salt that was generated when the data was encrypted. The presumption is that it would be difficult to recover the key, given only the encrypted data file and the salt, both of which could be accessible to attackers. Key generation is done using the "scrypt" key derivation function, deviced by Colin Percival. This intentionally uses large amounts of memory to thwart certain attacks that use large numbers of specialized cracking processors in parallel. The idea is that it's inexpensive to build massively parallel processing machines, but inpractically expensive to build such machines with large amounts of memory. With large key in hand, the actual encryption is done with NaCl, by Dan Bernstein. The cipher used by NaCl is based on elliptic curves, which provide good security with relatively small key sizes. Implementations of such ciphers run quickly, although speed is not a concern for this application. "pw" enhances security in one other minor way: by default it does not display passwords, instead copying them directly to the clipboard for eventual pasting to a destination. 

## Implementation
"pw" is implemented as a pair of Python scripts. The first takes a plaintext password list and produces an encrypted JSON database. The second uses this database to provide password retrieval. The practical paranoid will keep the unecrypted source files somewhere secure, like a desktop machine or on a USB key that can be physically hidden away. The encrypted files can be put on your laptop (by default, they go in the ~/.pw directory), copied up to a central server and generally made available enough to be useful.

## Future Directions
Ultimately, the second script will be augmented with editing capability. This would relegate the "buildpw" script to initial import, an allow the original plaintext source file to be deleted. 

## Contributions
Patches, discussion and (perhaps most importantly) analyses of the application's security are all welcome.

## Notes on Infrastructure
One problem is getting the required cryptographic components in place. This seems to be a problem generally and not just for this project, which is essentially a prototype application. For "pw", the operating system and scripting environment's package managers both needed to be employed to locate, build and install the parts. Ideally, the newer components employed by "pw" should be ubiquitous in the same way that OpenSSL is now. More ideally, they should be baked into the where people spend most of their time: the web browser. A project to embed Scrypt and NaCl into Chrome (or Firefox, or Safari) is worthwhile endeavor.


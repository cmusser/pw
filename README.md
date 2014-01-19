# PW: a simple password manager

## Introduction
pw is a pair of scripts that helps make using password-based security systems secure, while removing some of the tedium of using them. It  works from an encrypted list of passwords (the plaintext is a JSON database). After unlocking the list with a single master password, the utility provides a search function to look up specific passwords by name. After selecting the one you want, it helpfully puts the password into the clipboard. The common case of needing to type a password into a website login page is thus made a little easier. 

## Security
Automating the password retrieval means you can avoid one of the more egregious
security faux pas: password reuse. Given a large set of websites that need to be accessed regularly, many people simply use the same password for all of them.
If an attacker recovers a password for one site you use, she can simply try the password on other sites and often will be able to access your stuff there too. pw allows you to remember a single (hopefully secure) master password that unlocks the rest of the passwords. These, then, can be long, random non-words that are difficult to guess or derive by brute force. Until websites allow the use of more sophisticated security (public keys, security devices, etc), this makes passwords a little safer.

pw enhances your security in other ways. Since the password lists are encrypted, they can be stored on your laptop (or other physically accessible machine) and still be reasonably secure. Possession of the files isn't enough: to unlock them, the master password must be used. Also, the passwords are not shown on the screen by default, instead, they are copied directly to the systems clipboard. A future enchancement is to zap the clipboard contents after a short period of time.

## Implementation
"pw" is implemented as a pair of Python scripts. The first takes a plaintext password list and produces an encrypted JSON database. The second uses this database to provide password retrieval. The practical paranoid will keep the unecrypted source files somewhere secure, like a desktop machine or on a USB key that can be physically hidden away. The encrypted files can be put on your laptop (by default, they go in the ~/.pw directory), copied up to a central server and generally made available enough to be useful.

## Crypto
Two external libraries provide the required cryptographic functions. Colin Percival's "scrypt" library is used as the key derivation function. Encryption and random numbers are provided by Dan Bernstein's NaCl library (available via the PyNaCl module). Incorporating the libraries into a running system required some futing, which is described below.

## Motivation, Notes, Etc.
I'm a big fan of convenience and hence a big non-fan of passwords. Plus I was looking for a project with which to learn Python. A "meta-password" isn't an original idea. Several standalone programs (including PasswordSafe, by actual famous cryptographer Bruce Schneier) provide this functionality. The Mac OS X Keychain Access is another example of this, and is tightly integrated into the operating system to boot. My implementation provides a simple command-line version, which is flexible, if a little clunky in some cases.

## Future Directions
In the short term, a password editing feature would be nice. This would allow the password list to only exist on disk in encrypted form, and would obviate the need for the "buildpw" script, except for the purpose of an initial import.

Since a very common use is website access, one wonders whether the functionality shouldn't be in the browser. pw's clipboard copy feature is moderately convenient, but it still involves using a command line utility. I like that, but it may not fit the usage patterns of others. One impediment is making the required crypto available to the browser. Web browsers support connection encryption well, via their SSL/TLS support, but offer little else in the way of cryptographic primitives. A Chrome plugin that exposes a Javascript interaface to the NaCl primitives would be a worthwhile effort.

## Integration of Crypto Libraries:

pw depends on scrypt for key derivation and PyNaCl for encryption and random number generation. PyNaCl, in turn, depends on the libsodium shared library. During initial development, I integrated these rather haphazardly into my development machines (and found some problems on the way). This section attempts an overview of this aspect of the pw system.

### Mac OS X:
Installation of libsodium was via "brew". I can't remember how of PyNaCl was installed. It was not via "pip", which is not installed on my system. It's probably worth re-reading the PyNaCl homepage, because I probably followed the installation directions there. Python Scrypt is not installed yet.

### Linux
libsodium was compiled from source. PyNaCl and Scrypt were installed via "pip". Scrypt installed without problems. PyNaCl had two errors, both of which should be fixed. The first was in secret.py, where the KEYBYTES value had the wrong prefix. The second problem is in xxx.py, where an "initialized" variable wasnever set, causing some CFFI routine to be re-invoked, resulting in an exception.

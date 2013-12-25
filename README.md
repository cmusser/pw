# PW: a simple password manager

## Introduction
pw is a bare bones toolkit that seeks to keep passwords lists secure, while easing some of the tedium of using password-based security systems. It  works from an encrypted list of passwords (the plaintext is a JSON database). After unlocking the list with a single master password, the utility provides a search function to look up passwords by name. After selecting the one you want, it helpfully puts the password into the clipboard. This eases the common case of needing to type a password into a login screen on a website. 

## Security
Automating the password retrieval means you can avoid one of the more egregious
security faux pas: password reuse. Most people, given a large set of websites that need to be accessed regularly, simply use the same password for all of them.
If an attacker recovers a password for one site you use, she can simply try the password on other sites and often, will be able to access your stuff there too. With "pw" you can focus on remembering a single (hopefully secure) master password. The rest of the passwords are free to be long, random non-words that are difficult to guess or derive by brute force.

"pw" enhances your security in other ways. Since the password lists are encrypted, they can be stored on your laptop (or other accessible machine) and still be reasonably secure. Possession of the files isn't enough: to unlock them, the master password must be used. Also, the passwords are not shown on the screen by default, instead, they are copied directly to the systems clipboard. A future enchancement is to zap the clipboard contents after a short period of time.

## Implementation
"pw" is implemented as a pair of Python scripts. The first takes a plaintext password list and produces an encrypted JSON database. The second uses this database to provide password retrieval. The practical paranoid will keep the unecrypted source files somewhere secure, like a desktop machine or on a USB key that can be physically hidden away. The encrypted files can be put on your laptop (by default, they go in the ~/.pw directory), copied up to a central server and generally made available enough to be useful.

## Crypto
The cryptography is provided by Dan Bernstein's NaCl library (available via the PyNaCl module), which uses ciphers based on Edwards curves. I used it because I had previous experience with it on another project, it has a simple API and is considered to be quite secure. The ciphers are said to be fast, although that's not really important for this application. Other approaches were considered, and may be supported in the future. These include using OpenSSL and via the PyCrypto module, both of which offer AES.

## Future Directions
Since the most common use is access to websites, tighter integration with the web browser is desirable. pw's clipboard copy is moderately convenient, but it still involves using a command line utility, which some users will find annoying. Some sort of direct usage of NaCl within the browser (via a Chrome plugin), along with a user interface, would be nice.

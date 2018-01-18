pw is a system that attempts to keep large collections of passwords secure and accessible. A set of scripts take a single master password to access a password list, and then allow credentials to be searched and managed. Other systems, notably PasswordSafe, by cryptographer Bruce Schneier, are similar. This implementation uses NaCL for encryption and Scrypt for key derivation.

The package installs a number of command-line utilities for managing credentials.

1. getpw is for day-to-day credential lookups.
2. editpw is used to create or edit credentials and creating new credential databases.
3. rmpw is used to remove a credential that you don't need anymore.
4. dumppw is an export utility.
5. chpw is for changing the master password for a database.


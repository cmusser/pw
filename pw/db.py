import errno
import json
import nacl.secret
import nacl.utils
import os
import re
import readline  # noqa (import for prompt hist.; never referenced explicitly)
import scrypt

RO = 1
RW = 2
RW_CREATE_EMPTY = 3
FIELDS = 'site', 'username', 'password', 'extra'
MAX_FIELD_LEN = len(max(FIELDS, key=len))


class Base(object):

    def __init__(self):
        '''
        Initialize object. Note that the only assumptions are that the data
        is a dictionary and that the minimum functionality needed is
        provided by the methods defined below. Other decisions, such as how
        to store the data and whether to remember a password (and for how long)
        devolve to subclasses.
        '''
        self.data = {}

    def export_encrypted(self, salt, password):
        '''
        Return the data dictionary as an encrypted JSON text. This format
        is suitable for storage or transmission.
        '''
        key = scrypt.hash(password, salt, buflen=32)
        box = nacl.secret.SecretBox(key)
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        return box.encrypt(json.dumps(self.data), nonce)

    def import_from_encrypted(self, salt, password, encrypted):
        '''
        Load the data dictionary from an encrypted JSON text.
        '''
        key = scrypt.hash(password, salt, buflen=32)
        box = nacl.secret.SecretBox(key)
        self.data = json.loads(box.decrypt(encrypted))

    def find(self, search_term):
        return [name for name in self.data if re.search(search_term, name,
                                                        re.I)]


class File(Base):

    def __init__(self, pw_name, pw_func, access=RW):
        self.pw_filename = os.path.expanduser('~/.pw/' + pw_name + '.pw')
        self.pw_func = pw_func
        super(File, self).__init__()

        try:
            with open(self.pw_filename,
                      "r" if access == RO else 'r+') as pw_file:
                self.password = self.pw_func()
                self.import_from_encrypted(pw_file.read(64), self.password,
                                           pw_file.read())
        except IOError as e:
            if e.errno == errno.ENOENT and access == RW_CREATE_EMPTY:
                self.password = self.pw_func('Password for new database '
                                             '"{}": '.format(pw_name))
                self.save()
            else:
                raise e

    def load(self):
        with open(self.pw_filename, "r") as pw_file:
            self.import_from_encrypted(pw_file.read(64), self.password,
                                       pw_file.read())

    def save(self):
        with open(self.pw_filename, "w") as pw_file:
            salt = nacl.utils.random(64)
            pw_file.write(salt)
            pw_file.write(self.export_encrypted(salt, self.password))

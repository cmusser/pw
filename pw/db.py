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


class Base(object):

    def encrypt(password, data):
        salt = nacl.utils.random(64)
        key = scrypt.hash(password, salt, buflen=32)
        box = nacl.secret.SecretBox(key)
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        return box.encrypt(json.dumps(data), nonce)

    def decrypt(salt, password, encrypted):
        key = scrypt.hash(password, salt, buflen=32)
        box = nacl.secret.SecretBox(key)
        return json.loads(box.decrypt(encrypted))


class File(object):
    fields = 'site', 'username', 'password', 'extra'
    max_field_len = len(max(fields, key=len))

    def __init__(self, pw_name, pw_func, access=RW):
        self.pw_filename = os.path.expanduser('~/.pw/' + pw_name + '.pw')
        self.pw_func = pw_func

        try:
            with open(self.pw_filename,
                      "r" if access == RO else 'r+') as pw_file:
                self.password = self.pw_func()
                salt = pw_file.read(64)
                key = scrypt.hash(self.password, salt, buflen=32)
                box = nacl.secret.SecretBox(key)
                self.data = json.loads(box.decrypt(pw_file.read()))
        except IOError as e:
            if e.errno == errno.ENOENT and access == RW_CREATE_EMPTY:
                self.password = self.pw_func('Password for new database '
                                             '"{}": '.format(pw_name))
                self.data = {}
                self.save()
            else:
                raise e

    def load(self):
        with open(self.pw_filename, "r") as pw_file:
            salt = pw_file.read(64)
            key = scrypt.hash(self.password, salt, buflen=32)
            box = nacl.secret.SecretBox(key)
            json_data = box.decrypt(pw_file.read())

        self.data = json.loads(json_data)

    def save(self):
        with open(self.pw_filename, "w") as pw_file:
            salt = nacl.utils.random(64)
            key = scrypt.hash(self.password, salt, buflen=32)
            box = nacl.secret.SecretBox(key)
            nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
            encrypted = box.encrypt(json.dumps(self.data), nonce)
            pw_file.write(salt)
            pw_file.write(encrypted)

    def find(self, search_term):
        return [name for name in self.data if re.search(search_term, name,
                                                        re.I)]

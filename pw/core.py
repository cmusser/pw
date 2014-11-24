import argparse
import getpass
import json
import nacl.secret
import nacl.utils
import os
import re
import readline
import scrypt
import sys


class Store:

    fields = 'site', 'username', 'password', 'extra'
    max_field_len = len(max(fields, key=len))

    def __init__(self, pw_name, password):
        self.pw_filename = os.path.expanduser('~/.pw/' + pw_name + '.pw')
        self.password = password
        self.data = None

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


class Cli:

    @property
    def fields(self):
        return self._pw_store.fields

    @property
    def max_field_len(self):
        return self._pw_store.max_field_len

    @property
    def data(self):
        return self._pw_store.data

    @data.setter
    def data(self, new_data):
        self._pw_store.data = new_data

    def find(self, search_term):
        return self._pw_store.find(search_term)

    # Find some way for applications to not have to call this explicitly.
    def save(self):
        self._pw_store.save()

    @staticmethod
    def create_arg_parser(description):
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('pw_file', help='password list')
        parser.add_argument('credential_name', nargs='?', default=None,
                            help=('name of credential (if not specified, '
                                  'command will prompt.'))

        return parser

    @staticmethod
    def display_names(cli, names):
        n = 0
        for name in names:
            n += 1
            prefix = '' if len(names) == 1 else '{}.) '.format(n)
            print '{}{}'.format(prefix, name)

    def __init__(self, pw_name):
        try:
            self._pw_store = Store(pw_name, getpass.getpass())
        except (KeyboardInterrupt):
            print
            sys.exit()

    def run(self, prompt_str, pre_func=None, display_func=Cli.display_names,
            action_func=None, credential_name=None):

        def input_function(self, pre_func, display_func, action_func,
                           search_term):

            # pre_func returns True if processing should proceed, else False.
            if pre_func:
                if not pre_func(search_term):
                    return

            # Call display function with names sorted.
            names = self._pw_store.find(search_term)
            names.sort()
            display_func(self, names)

            # Call action function with exactly one name (which may be None).
            credential_name = None
            if len(names) == 1:
                credential_name = names[0]
            elif len(names) > 1:
                count = len(names)
                need_choice = True
                while need_choice:
                    choice = raw_input("1-{}> ".format(count))
                    try:
                        # The "cast" will either yield an integer or a
                        # ValueError, in the case of non-numeric input.
                        # Similarly, accessing the names at an index will
                        # elicit an IndexError.
                        choice_idx = int(choice) - 1
                        credential_name = names[choice_idx]
                        need_choice = False
                    except (ValueError, IndexError):
                        print "choice must be 1-{}".format(count)

            # The search term is included for the benefit of programs
            # that need it to create new entries.
            action_func(self, search_term, credential_name)

        try:
            if credential_name is None:
                while True:
                    line = raw_input('{}>'.format(prompt_str))
                    if line and not line.isspace():
                        self._pw_store.load()
                        input_function(self, pre_func, display_func,
                                       action_func, line)
                        print
            else:
                self._pw_store.load()
                input_function(self, pre_func, display_func, action_func,
                               credential_name)

        except (IOError, nacl.exceptions.CryptoError) as e:
            print e

        except (KeyboardInterrupt, EOFError):
            print

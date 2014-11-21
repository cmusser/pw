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

    @staticmethod
    def create_arg_parser(description):
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('pw_file', help='password list')
        parser.add_argument('credential_name', nargs='?', default=None,
                            help=('name of credential (if not specified, '
                                  'command will prompt.'))

        return parser

    @staticmethod
    def prompt_for_idx(list):
        count = len(list)
        need_choice = True
        while need_choice:
            choice = raw_input("1-{}> ".format(count))
            try:
                # The "cast" will either yield an integer or a ValueError, in
                # the case of non-numeric input.
                choice_idx = int(choice) - 1

                #  The value is not used, but accessing it
                # with the index causes a range check.
                list[choice_idx]
                need_choice = False
            except (ValueError, IndexError):
                print "choice must be 1-{}".format(count)

        return choice_idx

    def __init__(self, pw_name):
        try:
            self.pw_store = Store(pw_name, getpass.getpass())
        except (KeyboardInterrupt):
            print
            sys.exit()

    def lookup_credential_for_edit(self, search_term):
        names = self.pw_store.find(search_term)
        match_count = len(names)
        if match_count == 0:
            credential_name = search_term
        elif match_count == 1:
            credential_name = names[0]
        else:
            n = 0
            for name in names:
                n += 1
                print "\n{}.) {}".format(n, name)
                credential_name = names[self.prompt_for_idx(names)]

        return credential_name

    def prompt_loop(self, prompt, input_function):
        while True:
            line = raw_input('{}>'.format(prompt))
            if line and not line.isspace():
                input_function(self, line)
                print

    def run(self, prompt_str, process_func, credential_name=None):
        try:
            if credential_name is None:
                # The result of the load is not used here, but it gives the
                # function a chance to throw an exception if the file cannot
                # be accessed or the password was invalid..
                self.pw_store.load()
                self.prompt_loop(prompt_str, process_func)
            else:
                process_func(self, credential_name)

        except (IOError, nacl.exceptions.CryptoError) as e:
            print e

        except (KeyboardInterrupt, EOFError):
            print

import argparse
from . import db
import getpass
import nacl.secret
import nacl.utils
import readline  # noqa (import for prompt hist.; never referenced explicitly)
import sys


def get_default_file_args(description):
    '''
    Return an argument parser with arguments needed for CLI applications that
    use file access. Most callers can use the returned object as-is, but can
    call add_argument() if needed.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('pw_file', help='password list')
    parser.add_argument('credential_name', nargs='?', default=None,
                        help=('name of credential (if not specified, '
                              'command will prompt.'))

    return parser


def pw_prompt(prompt_str='Password: '):
    '''
    Provide a default command-line based password prompt.
    '''
    try:
        return getpass.getpass(prompt_str)

    except (KeyboardInterrupt):
        print()
        sys.exit()


class CliHelper(object):

    @property
    def cli(self):
        return self._cli

    @cli.setter
    def cli(self, cli):
        # Ideally, this should validate (via duck-typing, isinstance() or
        # something) that the passed object is a Cli. It's probably not
        # critical. In practice, CliHelpers are created to be passed to a Cli,
        # which does set this attribute to something valid (itself) in its
        # run() method.
        self._cli = cli

    def __init__(self):
        self._cli = None

    def preprocess_input(self, cli_input):
        ''' Called to process input from CLI before credential is chosen.

        This gives the application to catch commands that are not interpreted
        as the name of a credential to be looked up and manipulated. The
        function should return True if it handled the input and no action from
        the Cli class instance is required, False otherwise.

        Override this if additional commands are needed.
        '''
        if cli_input == 'list':
            for name in self.cli.data:
                print(name)
            print('\n{} credentials'.format(len(self.cli.data)))
            return True

        return False

    def display(self, names):
        ''' Called to display a list of credentials that matched the input.

        Only the names are provided. The application can use self.cli.data
        to access the credential information.

        Override this if a different format than "1.) Credential Name" is
        needed.
        '''
        if len(names) > 1:
            n = 0
            for name in names:
                n += 1
                print('{}.) {}'.format(n, name))

    def process_input(self, cli_input, name):
        ''' Called to process input from CLI, once a choice has been made.

        This is presented with the credential name resulting from the
        credential lookup, as well as the original input, which is sometimes
        useful, i.e., when creating a new credential.

        Override this to provide the essential application functionality. All
        subclasses need to do this; the code below doesn't do anything useful.
        '''
        print('original input: {}, resulting name: {}'.format(cli_input, name))


class Cli(object):
    '''
    This class provides the CLI, calling CliHelper functions to provide either
    a looping or one-shot interactive user interface.
    '''
    @property
    def data(self):
        return self._pw_db.data

    @data.setter
    def data(self, new_data):
        self._pw_db.data = new_data

    def find(self, search_term):
        return self._pw_db.find(search_term)

    # Find some way for applications to not have to call this explicitly.
    def save(self):
        self._pw_db.save()

    def __init__(self, pw_db, prompt_str, helper):
        self._pw_db = pw_db
        self._prompt_str = prompt_str
        self._helper = helper
        self._helper.cli = self

    def input_function(self, search_term):
        '''
        Normally not called by applications, but public to facilitate testing.
        '''
        # pre_func returns True if processing should proceed, else False.
        if self._helper.preprocess_input(search_term):
            return

        # Call display function with names sorted.
        names = self._pw_db.find(search_term)
        names.sort()
        self._helper.display(names)

        # Call action function with exactly one name (which may be None).
        credential_name = None
        if len(names) == 1:
            credential_name = names[0]
        elif len(names) > 1:
            count = len(names)
            need_choice = True
            while need_choice:
                choice = input("1-{}> ".format(count))
                try:
                    choice_idx = int(choice) - 1
                    credential_name = names[choice_idx]
                    need_choice = False
                except (ValueError, IndexError):
                    print("choice must be 1-{}".format(count))

        # The search term is included for the benefit of programs
        # that need it to create new entries.
        self._helper.process_input(search_term, credential_name)

    def run(self, credential_name):

        try:
            if credential_name is None:
                while True:
                    line = input('{}>'.format(self._prompt_str))
                    if line and not line.isspace():
                        self._pw_db.load()
                        self.input_function(line)
                        print()
            else:
                self._pw_db.load()
                self.input_function(credential_name)

        except (IOError, nacl.exceptions.CryptoError) as e:
            print(e)

        except (KeyboardInterrupt, EOFError):
            print()


class FileCli(Cli):
    '''
    This class is for use with CLIs with File databases. The only functionaity
    it adds is gracefully handling exceptions peculiar to the constructor of
    the File class.
    '''
    def __init__(self, pw_file, prompt_str, helper, access=db.RW):
        try:
            super(FileCli, self).__init__(db.File(pw_file, pw_prompt, access),
                                          prompt_str, helper)
        except (IOError, nacl.exceptions.CryptoError) as e:
            print(e)
            sys.exit()

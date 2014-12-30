import argparse
import getpass
import nacl.secret
import nacl.utils
import readline  # noqa (import for prompt hist.; never referenced explicitly)
import db
import sys


class CliHelper(object):

    def __init__(self, cli):
        self.cli = cli

    def preprocess_input(self, cli_input):
        ''' Called to process input from CLI before credential is chosen.

        This gives the application to catch commands that are not interpreted
        as the name of a credential to be looked up and manipulated. The
        function should return True if it handled the input and no action from
        the Cli class instance is required, False otherwise.
        '''
        if cli_input == 'list':
            self.show_list()
            return True

        return False

    def display(self, names):
        ''' Called to display a list of credentials that matched the input.

        Only the names are provided. The application can use self.cli.data
        to access the credential information.
        '''
        if len(names) > 1:
            n = 0
            for name in names:
                n += 1
                print '{}.) {}'.format(n, name)

    def process_input(self, cli_input, name):
        ''' Called to process input from CLI, once a choice has been made.

        This is presented with the credential name resulting from the
        credential lookup, as well as the original input, which is sometimes
        useful, i.e., when creating a new credential.
        '''
        print 'original input: {}, resulting name: {}'.format(cli_input, name)

    def show_list(self):
        for name in self.cli.data:
            print name
        print '\n{} credentials'.format(len(self.cli.data))
        pass


class Cli(object):

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

    def __init__(self, description):
            self._parser = argparse.ArgumentParser(description=description)
            self._parser.add_argument('pw_file', help='password list')
            self._parser.add_argument('credential_name', nargs='?',
                                      default=None,
                                      help=('name of credential (if not '
                                            'specified, command will prompt.'))

    def pw_prompt(self, prompt_str='Password: '):
        try:
            return getpass.getpass(prompt_str)

        except (KeyboardInterrupt):
            print
            sys.exit()

    def run(self, prompt_str, helper_class, access=db.RW):

        def input_function(self, search_term):

            # pre_func returns True if processing should proceed, else False.
            if helper.preprocess_input(search_term):
                return

            # Call display function with names sorted.
            names = self._pw_db.find(search_term)
            names.sort()
            helper.display(names)

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
            helper.process_input(search_term, credential_name)

        # This is the start of the run() method.
        self.args = self._parser.parse_args()
        helper = helper_class(self)
        try:
            self._pw_db = db.File(self.args.pw_file, self.pw_prompt, access)
        except (IOError, nacl.exceptions.CryptoError) as e:
            print e
            sys.exit()

        try:
            if self.args.credential_name is None:
                while True:
                    line = raw_input('{}>'.format(prompt_str))
                    if line and not line.isspace():
                        self._pw_db.load()
                        input_function(self, line)
                        print
            else:
                self._pw_db.load()
                input_function(self, self.args.credential_name)

        except (IOError, nacl.exceptions.CryptoError) as e:
            print e

        except (KeyboardInterrupt, EOFError):
            print

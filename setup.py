from setuptools import setup, find_packages

setup(
    name='Pw',
    version='0.1.0',
    author='Chuck Musser',
    author_email='cmusser@sonic.net',
    packages=['pw'],
    scripts=['bin/getpw', 'bin/editpw', 'bin/chpw', 'bin/mvpw', 'bin/rmpw',
             'bin/dumppw'],
    url='http://pypi.python.org/pypi/Pw/',
    license='LICENSE.txt',
    description='Simple, secure command-line password manager.',
    long_description=open('README.txt').read(),
    install_requires=[
        "pynacl",
        "scrypt",
    ],
)

import json
import nacl.secret
import nacl.utils
import os
import scrypt


def path(name):
    return os.path.expanduser('~/.pw/' + name + '.pw')


def load(pw_filename, password):
    with open(pw_filename, "r") as pw_file:
        salt = pw_file.read(64)
        key = scrypt.hash(password, salt, buflen=32)
        box = nacl.secret.SecretBox(key)
        json_data = box.decrypt(pw_file.read())

    return json.loads(json_data)


def save(pw_filename, password, pw_data):
    with open(pw_filename, "w") as pw_file:
        salt = nacl.utils.random(64)
        key = scrypt.hash(password, salt, buflen=32)
        box = nacl.secret.SecretBox(key)
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        encrypted = box.encrypt(json.dumps(pw_data), nonce)
        pw_file.write(salt)
        pw_file.write(encrypted)

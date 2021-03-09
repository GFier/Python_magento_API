from cryptography.fernet import Fernet
import os

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open(os.getcwd() + "/app/data/secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def encrypt_message(key, message):
    """
    Encrypts a message
    """
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

def decrypt_message(key, encrypted_message):
    """
    Decrypts an encrypted message
    """
    if encrypted_message != '':
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)
        the_secret = decrypted_message.decode()
    else:
        the_secret = ''
    return the_secret

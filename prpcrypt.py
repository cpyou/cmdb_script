import hashlib
import json
import os

from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES


def to_bytes(value):
    if not isinstance(value, bytes):
        return bytes(value, encoding="utf-8")
    return value


def to_string(value):
    if not isinstance(value, str):
        return str(value, encoding="utf-8")
    return value


def encrypt(salt, password):
    key_md5 = hashlib.md5(to_bytes(salt)).hexdigest()
    cipher = AES.new(to_bytes(key_md5), AES.MODE_CFB, b'0000000000000000')
    ntext = to_bytes(password + ('\0' * (16 - (len(password) % 16))))
    return to_string(b2a_hex(cipher.encrypt(ntext)))


def decrypt(salt, password_hash):
    key_md5 = hashlib.md5(to_bytes(salt)).hexdigest()
    cipher = AES.new(to_bytes(key_md5), AES.MODE_CFB, b'0000000000000000')
    t = cipher.decrypt(a2b_hex(password_hash))
    return to_string(t).rstrip('\0')


def get_default_salt():
    return os.environ.get('SECRET_KEY') or 'X=Mc<Qm)aGM+R9DzLxx!kS<gy+6}{fN:]+<Jp#7QZkxYW(&E"ej<su*9LX,Zasd'


def get_pass(key):
    pass_path = '/data/app/current/src/pass.json'
    with open(pass_path, 'r') as load_f:
        load_dict = json.load(load_f)
        return decrypt(get_default_salt(), load_dict.get(key, ''))

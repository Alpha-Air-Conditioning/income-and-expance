from cryptography.fernet import Fernet
import jwt
import os
import environ
from django.conf import settings

environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))
env = environ.Env()

key = Fernet.generate_key()
cipher_suite = Fernet(key)
JWT_SECRET = env("SECRET_KEY")


def create_token(payload):
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    encrypted_token = cipher_suite.encrypt(token.encode()).decode()
    return encrypted_token


def decrypt_token(enc_token):
    try:
        dec_token = cipher_suite.decrypt(enc_token.encode()).decode()
        payload = jwt.decode(dec_token, JWT_SECRET, algorithms=['HS256'])
        return {'payload': payload, 'status': True}
    except:
        return {'status': False}
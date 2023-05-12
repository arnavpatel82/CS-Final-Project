import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random

random_code = Random.new().read
rsa = RSA.generate(1024, random_code)

private_pem = rsa.export_key()
with open('client-private.pem', 'w') as f:
    f.write(str(private_pem))

public_pem = rsa.publickey().export_key()
with open('client-public.pem', 'w') as f:
    f.write(public_pem)

def C_encrypt(my_msg):
    with open('client-public.pem', 'r') as f:
        key = f.read()
    rsakey = RSA.import_key(key)
    cipher = PKCS1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(my_msg.encode(encoding="utf-8"))).decode()
    return cipher_text

def C_decrypt(cipher_text):
    with open('client-private.pem') as f:
        key = f.read()
    rsakey = RSA.import_key(key)
    cipher = PKCS1_v1_5.new(rsakey)
    text = cipher.decrypt(base64.b64decode(cipher_text), "ERROR").decode("utf-8")
    return text

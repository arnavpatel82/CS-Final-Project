import base64
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5

randomizer = Random.new().read
rsa = RSA.generate(1024,randomizer)

pem_private_key = rsa.exportKey()
with open ('client-private.pem','wb') as f:
    f.write(pem_private_key)

pem_public_key = rsa.publickey().exportKey()
with open ('client-public.pem','wb') as f:
    f.write(pem_public_key)




def Encryption(m):
   with open ('client-public.pem','r') as f:
    key = f.read()
    rsa_key = RSA.importKey(key)
    cipher = PKCS1_v1_5.new(rsa_key)
   cipher_text = base64.b64encode(cipher.encrypt(m.encode(encoding = 'utf-8'))).decode('utf-8')
   return cipher_text

def Decryption(encrypted_text):
   with open ('client-private.pem') as f:
      key = f.read()
      rsa_key = RSA.importKey(key)
      cipher = PKCS1_v1_5.new(rsa_key)
      text = cipher.decrypt(base64.b64decode(encrypted_text), None).decode('utf-8')
      return text


   




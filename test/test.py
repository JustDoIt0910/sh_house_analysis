import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

if __name__ == '__main__':

    public_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCCB81pk1Go/d7K8unYqeB6YyQdDgIRsLji7BxlBfMC2U8/0lyOLxJ6sQb1RmKaILuxN0hRci4zWPfkkPhttWaogq3XABYiDYbx0843ge4D79pG21+qWplw43uHZNs0B6iUChJW1O3DDJPXGwj50L1ySTVt7G7iqsIr9PLZVRSZmQIDAQAB"
    key = "-----BEGIN RSA PUBLIC KEY-----\n" + public_key + "\n-----END RSA PUBLIC KEY-----"
    cipher = PKCS1_cipher.new(RSA.importKey(key.encode()))
    pwd = "20010910cheng"
    encrypt_text = base64.b64encode(cipher.encrypt(pwd.encode("utf-8")))
    print(encrypt_text.decode('utf-8'))
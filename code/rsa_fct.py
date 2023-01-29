import base64

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey.RSA import RsaKey


def generateKeys() -> list:
    """
    Generate the RSA keys for encryption and decryption
    :return: The public key that contain the n and the e and the private key that contain the n and d for decryption
    """
    keyPair = RSA.generate(2048)
    pubKey = keyPair.publickey()
    public_key = pubKey.exportKey("PEM")

    pair_key = keyPair.exportKey()

    return [pubKey, keyPair]


def rsaEncryption(plaintText: str, pubKey) -> bytes:
    """
    Function that encrypt a plain Text with the public key
    :param plaintText: The text int string we want to crypt
    :param pubKey: The public key that have n and the e to make the encryption
    :return: The plain text encrypted
    """
    str_1_encoded = bytes(plaintText, 'UTF-8')
    encryptor = PKCS1_OAEP.new(pubKey)

    return encryptor.encrypt(str_1_encoded)


def rsaDecryption(encrypted: bytes, keyPair) -> bytes:
    """
    The fonction text a plainText encrypted and decrypted it using the key pair
    :param encrypted:
    :param keyPair: contains the n and d for decrypted
    :return:
    """
    decryptor = PKCS1_OAEP.new(keyPair)
    return decryptor.decrypt(encrypted)


def rsa(plainText: str) -> None:
    # We get the 2 keys
    publicKey, keyPair = generateKeys()
    # We encrypt the plain text passed in parameter
    encrypted = rsaEncryption(plainText, publicKey)
    # We decrypt the plain text and render it
    print(rsaDecryption(encrypted, keyPair))

def encrypt_message(serv_pub_key: RsaKey, message: bytes) -> bytes:
    """
    We encrypt the ciphertext with the given public key;
    :param serv_pub_key:
    :param message:
    :return:
    """
    cipher = PKCS1_OAEP.new(serv_pub_key)
    encrypted_message = cipher.encrypt(message)
    return base64.b64encode(encrypted_message)


def decrypt_message(key, rep):
    """
    We create a PKCS1_OAEP_Cipher object from the RSA private key
    and use it to decrypt the ciphertext.
    :param key:
    :param serv_rep:
    :return:
    """
    server_rep_str = rep.decode('latin-1')
    decode_rep = base64.b64decode(server_rep_str.encode('latin-1'))
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(decode_rep).decode('latin-1')
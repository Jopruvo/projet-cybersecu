from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


def generateKeys() -> list:
    """
    Generate the RSA keys for encryption and decryption
    :return: The public key that contain the n and the e and the private key that contain the n and d for decryption
    """
    keyPair = RSA.generate(3072)
    pubKey = keyPair.publickey()
    print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
    pubKey.exportKey()

    print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
    keyPair.exportKey()

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

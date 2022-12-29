from rsaPKCS1_0AEP import *

if __name__ == '__main__':
    plainText = "SUUUUUUUUUUU"

    publicKey, keyPair = generateKeys()

    encrypted = rsaEncryption(plainText, publicKey)
    decrypted = rsaDecryption(encrypted, keyPair)

    print("encrypted: "+encrypted.decode("latin-1"))
    print("decrypted: "+decrypted.decode("latin-1"))

from rsaPKCS1_0AEP import *

if __name__ == '__main__':
    plainText = "SUUUUUUUUUUU"

    publicKey, keyPair = generateKeys()

    encrypted = rsaEncryption(plainText, publicKey)
    decrypted = rsaDecryption(encrypted, keyPair)

    print(decrypted)

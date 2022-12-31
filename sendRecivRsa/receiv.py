from rsa.rsaPKCS1_0AEP import *

import rsa
import base64
import socket

# on génére les clef du cryptage rsa
key = RSA.generate(2048)
print(key)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('localhost', 1234))
while True:
    sock.listen()
    print("--- Its Listening ! ---")

    conn, addr = sock.accept()
    print('--- Request Accepted ---')

    # On recoit la pub key du client
    client_public_key_str = conn.recv(4096).decode('utf-8')
    client_public_key = RSA.import_key(client_public_key_str)
    print('[*] Client public key received !')

    # Envoi de la clé publique RSA au sendeur
    serv_public_key = key.publickey().export_key('PEM')
    conn.send(serv_public_key)
    print('[*] Server public key sent !')

    # Réception et conversion du message crypté en chaîne de caractères
    encrypted_message_str = conn.recv(4096).decode('utf-8')
    encrypted_message = base64.b64decode(encrypted_message_str.encode('utf-8'))

    # Création d'un objet PKCS1_OAEP_Cipher à partir de la clé privée RSA
    cipher = PKCS1_OAEP.new(key)

    # Décryptage du message
    decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')

    # Affichage du message décrypté
    print(decrypted_message)

    if encrypted_message:
        # On encrypt Le message
        cipher = PKCS1_OAEP.new(client_public_key)
        str_1_encoded = bytes(decrypted_message + " BIEN RENVOYER", 'UTF-8')
        encrypted_message = cipher.encrypt(str_1_encoded)
        encrypted_message_str = base64.b64encode(encrypted_message).decode('utf-8')

        # On envoie le message crypté avec la clef publique du serveur au serveur
        conn.send(encrypted_message_str.encode("utf-8"))
        print('[*] Response encrypted send to the client')
        break

sock.close()
print("[*] Socket closed")

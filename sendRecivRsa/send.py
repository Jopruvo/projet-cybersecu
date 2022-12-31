from rsa.rsaPKCS1_0AEP import *

import rsa
import base64
import socket

# Génération de la clé publique et privée RSA
key = RSA.generate(2048)

# Envoi de la clé publique RSA au destinataire
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 1234))
client_public_key = key.publickey().export_key('PEM')
sock.send(client_public_key)
print('[*] Client public key sent')

# On recoit la clef public du serv
serv_public_key_str = sock.recv(4096)
print('[*] Server public key received !')

# On encrypt Le message
serv_pub_key = RSA.import_key(serv_public_key_str)
cipher = PKCS1_OAEP.new(serv_pub_key)
encrypted_message = cipher.encrypt(b'SUUUUUUUUUUUUU')
encrypted_message_str = base64.b64encode(encrypted_message).decode('utf-8')

# On envoie le message crypté avec la clef publique du serveur au serveur
sock.send(encrypted_message_str.encode("utf-8"))


#On recoit la rep crypté du serv
server_rep_str = sock.recv(4096).decode('utf-8')
serv_rep = base64.b64decode(server_rep_str.encode('utf-8'))

# Création d'un objet PKCS1_OAEP_Cipher à partir de la clé privée RSA
cipher = PKCS1_OAEP.new(key)

# Décryptage du message
decrypted_message = cipher.decrypt(serv_rep).decode('utf-8')

# Affichage du message décrypté
print(decrypted_message)

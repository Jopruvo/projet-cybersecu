from Cryptodome.PublicKey import RSA
from tools.rsa_fct import encrypt_message, decrypt_message
import socket


def init_sock(host: str, port: int) -> socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((host, port))
    print("[*] Socket successfully connected")
    return server_sock


def send_message(ciphertext: bytes, port):
    # Initialisation des sockets
    server_sock = init_sock('localhost', port)
    print()

    # Génération de la clé publique et privée RSA
    rsa_keys = RSA.generate(2048)
    print(rsa_keys)

    # Envoi de la clé publique RSA au destinataire
    client_public_key = rsa_keys.publickey().export_key('PEM')
    server_sock.send(client_public_key)
    print('[*] Client public key sent')

    # On recoit la clef public du serv
    serv_public_key_bytes = server_sock.recv(2048)
    serv_public_key_rsa_key = RSA.import_key(serv_public_key_bytes)
    print('[*] Server public key received !')

    # On envoie le message crypté avec la clef publique du serveur au serveur
    chunk_size = 128
    chunks = [ciphertext[i:i + chunk_size] for i in range(0, len(ciphertext), chunk_size)]
    for chunk in chunks:

        server_sock.send(encrypt_message(serv_public_key_rsa_key, chunk))

    # On recoit la rep crypté du serv
    server_rep = server_sock.recv(1024)

    # Affichage du message décrypté
    print("Server response :", decrypt_message(rsa_keys, server_rep))



# send_message(b"My request")

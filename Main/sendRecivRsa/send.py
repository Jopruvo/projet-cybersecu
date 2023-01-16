from Cryptodome.PublicKey import RSA
from rsa_fct import encrypt_message, decrypt_message
import socket


def init_sock(host: str, port: int) -> socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((host, port))
    print("[*] Socket successfully connected")
    return server_sock


def send_message(ciphertext: bytes, port):
    # Initialisation des sockets
    server_sock = init_sock('localhost', port)

    # Génération de la clé publique et privée RSA
    rsa_keys = RSA.generate(2048)
    print(rsa_keys)

    # Envoi de la clé publique RSA au destinataire
    client_public_key = rsa_keys.publickey().export_key('PEM')
    server_sock.send(client_public_key)
    print('[SEND] Client public key sent')

    # On recoit la clef public du serv
    serv_public_key_bytes = server_sock.recv(2048)
    serv_public_key_rsa_key = RSA.import_key(serv_public_key_bytes)
    print('[SEND] Server public key received !')



    # [ALLER] Envoie du message crypté
    chunk_size = 128
    chunks = [ciphertext[i:i + chunk_size] for i in range(0, len(ciphertext), chunk_size)]
    encrypted_request=b""
    for chunk in chunks:
        encrypted_request+=encrypt_message(serv_public_key_rsa_key, chunk)+b";"
    print("\n[SEND] encrypted request: "+str(encrypted_request[:-1]))
    server_sock.send(encrypted_request[:-1])





    #[RETOUR] Reception du message crypté
    decr_client_request = b''
    try:
        encrypt_response = server_sock.recv(2048)
        print("\n[SEND]"+str(encrypt_response))
        encrypt_chunk_list = encrypt_response.split(b";")
        
        for chunk in encrypt_chunk_list:
            decr_client_request+=bytes(decrypt_message(rsa_keys, chunk), 'latin-1')
    except socket.error as e:
        print("[ERROR] -"+e)

    print("\n[SEND]"+str(decr_client_request))
    print("\n[SEND]"+str(len(decr_client_request)))



from Cryptodome.PublicKey import RSA
from tools.rsa_fct import encrypt_message, decrypt_message
import socket


def reciev(port):
    # on génére les clef du cryptage tools
    rsa_keys = RSA.generate(2048)
    print(rsa_keys)
    # Initialisation des sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', port))

    while True:
        sock.listen()
        print(f"--- Its Listening on port : {port} ---")

        client_conn, addr = sock.accept()
        print('--- Request Accepted ---')

        # On recoit la pub rsa_keys du client
        client_public_key_bytes = client_conn.recv(2048).decode('utf-8')
        client_public_key_rsa_key = RSA.import_key(client_public_key_bytes)
        print('[*] Client public rsa_keys received !')

        # Envoi de la clé publique RSA au sendeur
        serv_public_key = rsa_keys.publickey().export_key('PEM')
        client_conn.send(serv_public_key)
        print('[*] Server public rsa_keys sent !')
        done = False
        decr_client_request = b''
        client_conn.settimeout(0.5)
        while True:
            try:
                encrypt_chunk = client_conn.recv(2048)
                decr_chunk = bytes(decrypt_message(rsa_keys, encrypt_chunk), 'UTF-8')
                decr_client_request += decr_chunk
            except socket.error as e:
                print(e)
                break

        # Réception et conversion du message crypté en chaîne de caractères de la requete du client
        print('je suis sortie')
        # Décryptage du message Affichage du message décrypté
        decrypted_message = decr_client_request
        print("ici", decr_client_request)

        if decrypted_message:
            # Todo PROXY CALL
            serv_rep = bytes(decrypted_message.decode() + " BIEN RENVOYER", 'UTF-8')
            client_conn.send(encrypt_message(client_public_key_rsa_key, serv_rep))
            print('[*] Response encrypted send to the client')
            break
    sock.close()
    client_conn.close()
    print("[*] Socket closed")

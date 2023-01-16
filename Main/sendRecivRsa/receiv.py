from Cryptodome.PublicKey import RSA
from rsa_fct import encrypt_message, decrypt_message
import socket


def reciev(port):
    # on génére les clef du cryptage tools
    rsa_keys = RSA.generate(2048)
    print(rsa_keys)
    # Initialisation des sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', port))
    chunk_size = 128
    sock.listen()
    print(f"--- Its Listening on port : {port} ---")

    client_conn, addr = sock.accept()
    print('--- Request Accepted ---')

    # On recoit la pub rsa_keys du client
    client_public_key_bytes = client_conn.recv(2048).decode('utf-8')
    client_public_key_rsa_key = RSA.import_key(client_public_key_bytes)
    #vraiment necessaire de le faire à chaque requête?
    print('[RECEIVE] Client public rsa_keys received !')

    # Envoi de la clé publique RSA au sendeur
    serv_public_key = rsa_keys.publickey().export_key('PEM')
    client_conn.send(serv_public_key)
    print('[RECEIVE] Server public rsa_keys sent !')


    # [ALLER] Reception du message crypté
    decr_client_request = b''
    try:
        encrypt_request = client_conn.recv(2048)
        encrypt_chunk_list = encrypt_request.split(b";")
        for chunk in encrypt_chunk_list:
            decr_client_request+=bytes(decrypt_message(rsa_keys, chunk), 'latin-1')
    except socket.error as e:
        print("[ERROR] -"+e)

    # Réception et conversion du message crypté en chaîne de caractères de la requete du client
    # Décryptage du message Affichage du message décrypté
    decrypted_message = decr_client_request
    print("\n[RECEIVE]full decrypted message: ", decr_client_request)
    print("[RECEIVE]full decrypted message lenght: ", len(decr_client_request))



    #[RETOUR] Envoie du message crypté
    if decrypted_message:
        # Todo PROXY CALL
        encrypted_response = b""
        chunks = [decr_client_request[i:i + chunk_size] for i in range(0, len(decr_client_request), chunk_size)]
        for chunk in chunks:
            encrypted_response+=encrypt_message(client_public_key_rsa_key, chunk)+b";"
        client_conn.send(encrypted_response[:-1])
        print('\n[RECEIVE] sending: '+str(encrypted_response[:-1]))

    sock.close()
    client_conn.close()
    print("[*] Socket closed")

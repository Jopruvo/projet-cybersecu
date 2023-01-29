from _thread import start_new_thread
import socket, sys
from time import sleep
from contextlib import closing
from Cryptodome.PublicKey import RSA
from rsa_fct import encrypt_message, decrypt_message
import socket


listening_port = 8080
sending_port = 8081
max_conn = 5
buffer_size = 4096

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0)) 
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]



def init_sock(host: str, port: int) -> socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((host, port))
    print("[*] Socket successfully connected")
    return server_sock


def send_request(ciphertext: bytes):
    print("\n[*] NEW REQUEST ->"+str(ciphertext)+"\n")
    # Initialisation des sockets
    server_sock = init_sock('localhost', sending_port)

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

    # [ALLER] Envoie de la requête crypté
    chunk_size = 128
    chunks = [ciphertext[i:i + chunk_size] for i in range(0, len(ciphertext), chunk_size)]
    encrypted_request=b""
    for chunk in chunks:
        encrypted_request+=encrypt_message(serv_public_key_rsa_key, chunk)+b";"
    print("\n[*] encrypted request: "+str(encrypted_request[:-1]))
    server_sock.send(encrypted_request[:-1])
    receive_response(server_sock,rsa_keys)



def receive_response(server_sock,rsa_keys):
    #[RETOUR] Reception de la réponse crypté
    decr_client_response = b''
    try:
        encrypt_response = server_sock.recv(8192)
        print("\n[*] encrypt response: "+str(len(encrypt_response)))
        encrypt_chunk_list = encrypt_response.split(b";")
        
        for chunk in encrypt_chunk_list:
            decr_client_response+=bytes(decrypt_message(rsa_keys, chunk), 'latin-1')
    except socket.error as e:
        print("[ERROR] -"+e)
    print("\n[*] decrypted response"+str(len(decr_client_response)))
    conn.send(decr_client_response)



def start():
    global conn
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # init socket
        print("[*] Initializing Sockets")
        client_socket.bind(('localhost', listening_port))
        print("[*] Socket bind Successfully")
        client_socket.listen(max_conn)
        print(f"[*] Server starting to listen on : {listening_port}")
    except Exception as e:
        print(f"[*] Error {e} \n[*] Unable to initialize Socket")
        sys.exit(2)

    while True:
        try:
            conn, addr = client_socket.accept()
            client_data = conn.recv(buffer_size)
            start_new_thread(send_request, (client_data,))
        except KeyboardInterrupt:
            client_socket.close()
            print(f"[*] KeyboardInterrupt :-> Proxy server Shutting Down")
            sys.exit()

start()

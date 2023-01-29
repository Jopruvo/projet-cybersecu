from _thread import start_new_thread
import socket, sys
from Cryptodome.PublicKey import RSA
from rsa_fct import encrypt_message, decrypt_message
import socket



listening_port = 8081
max_conn = 5
buffer_size = 4096
client_public_key_rsa_key=b''

def proxy_server(webserver, port, conn, client_data, addr):
    print("proxy_server")
    method = client_data.split(" ")[0]
    try:
        if (method == "CONNECT"):
            return https_request(webserver, port, conn, client_data, addr)
        else:
            # we create a new socket that will send the request for the client
            return http_request(webserver, port, conn, client_data, addr)
    except Exception as e:
        print("Proxy server error handling request ", e)
        sys.exit(1)


def https_request(webserver, port, conn, client_data, addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # If successful, send 200 code response
        s.connect((webserver, port))
        reply = "HTTP/1.0 200 Connection established\r\n"
        reply += "Proxy-agent: SigmaIDU\r\n"
        reply += "\r\n"
        send_response(conn,reply.encode())
    except socket.error as err:
        pass
    conn.setblocking(0)
    s.setblocking(0)
    while True:
        try:
            request = conn.recv(buffer_size)
            if request != b'':
                print("request: " + str(request))
            s.sendall(request)
        except socket.error as err:
            #print("error1: "+ str(err))
            pass

        try:
            reply = s.recv(buffer_size)
            send_response(conn,response)
        except socket.error as err:
            #print("error1: "+ str(err))
            pass


def http_request(webserver, port, conn, client_data, addr):
    print("http")
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.connect((webserver, port))
        server_socket.send(client_data.encode('utf-8'))

        while True:
            response = server_socket.recv(buffer_size)
            if (len(response) > 0):
                send_response(conn,response)
                # print(f'[*] Request done ! {addr[0]}')
                # print('Response : ', response)
            else:
                break
        server_socket.close()
        conn.close()

    except socket.error:
        server_socket.close()
        conn.close()
        sys.exit(1)


def conn_string(conn, client_data: bytes, addr):
    """
    This function take the client request and find the webserver dns and the port of the request.
    :param conn:
    :param client_data:
    :param addr:
    :return:
    """
    client_data = client_data.decode("latin-1")
    # print("CLIENT DATA: ", client_data)
    try:
        first_line = client_data.split('\n')[0]
        print(f'\n\nFirst line : {first_line}')
        url = first_line.split(' ')[1]
        http_pos = url.find("://")  # Find the pos of ://
        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos + 3):]  # Get the rest of the url
        port_pos = temp.find(":")  # get the index of the port
        webserver_pos = temp.find("/")  # get the index of the end of the webserver

        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if (port_pos == -1 or webserver_pos < port_pos):  # default port 80
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[port_pos + 1:])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]
        print(f'Webserver : {webserver} \nPort : {port}')
        proxy_server(webserver, port, conn, client_data, addr)
    except Exception as e:
        print("ERRR", e)
        sys.exit(1)


def reciev_request(client_conn,client_public_key_bytes,addr):
    global client_public_key_rsa_key
    # on génére les clef du cryptage tools
    print("listening on "+str(addr))
    rsa_keys = RSA.generate(2048)
    print(rsa_keys)
    # Initialisation des sockets
    chunk_size = 128

    # On recoit la pub rsa_keys du client
    client_public_key_rsa_key = RSA.import_key(client_public_key_bytes)
    #vraiment necessaire de le faire à chaque requête?
    print('[*] Client public rsa_keys received !')

    # Envoi de la clé publique RSA au sendeur
    serv_public_key = rsa_keys.publickey().export_key('PEM')
    client_conn.send(serv_public_key)
    print('[*] Server public rsa_keys sent !')


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
 
    print("\n[RECEIVE]full decrypted message: ", decr_client_request)
    conn_string(client_conn, decr_client_request, addr)

def send_response(client_conn,response):
    global client_public_key_rsa_key
    chunk_size = 128
    encrypted_response = b""
    chunks = [response[i:i + chunk_size] for i in range(0, len(response), chunk_size)]
    for chunk in chunks:
        encrypted_response+=encrypt_message(client_public_key_rsa_key, chunk)+b";"
    client_conn.send(encrypted_response[:-1])



def start():
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
            client_public_key_bytes = conn.recv(buffer_size)
            start_new_thread(reciev_request, (conn, client_public_key_bytes, addr))
        except KeyboardInterrupt:
            client_socket.close()
            print(f"[*] KeyboardInterrupt :-> Proxy server Shutting Down")
            sys.exit()

start()


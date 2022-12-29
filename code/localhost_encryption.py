from _thread import start_new_thread
import socket, sys
import threading
import ssl
from rsaPKCS1_0AEP import *

proxy_server="localhost"
proxy_port=8000
listening_port = 8080
max_conn = 5
buffer_size = 4096

def forwardProxy(conn, client_data, addr):
    encr_Client_data=rsaEncryption(client_data)
    print(encr_Client_data)
    server_socket.connect((webserver, port))
    pass

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
            client_data = conn.recv(buffer_size)
            # threading.Thread(target=conn_string, args=(conn, client_data, addr))
            start_new_thread(forwardProxy, (conn, client_data, addr))
        except KeyboardInterrupt:
            client_socket.close()
            print(f"[*] KeyboardInterrupt :-> Proxy server Shutting Down")
            sys.exit()

start()
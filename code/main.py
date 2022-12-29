##--------------------------------------------------------------------------------------------##
##                                 SUJET 1 - PROJET CYBERSECURITE                             ##
##  authors : PRUVOST Jordan, TAKAHASHI Vincent, OUKZIZ Salma, GONAY Arthur & BOUGHAMNI Rami  ##
##                                       date : 27/10/22                                      ##
##--------------------------------------------------------------------------------------------##

#_____________________________________________________________________________________________#

# Build proxy server
from _thread import start_new_thread
import socket, sys
import threading
import ssl

listening_port = 8080
max_conn = 5
buffer_size = 4096


def proxy_server(webserver, port, conn, client_data, addr):
    method = client_data.split(" ")[0]
    try:
        if (method == "CONNECT"):
            https_request(webserver, port, conn, client_data, addr)
        else:
            # we create a new socket that will send the request for the client
            http_request(webserver, port, conn, client_data, addr)
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
        conn.sendall(reply.encode())
    except socket.error as err:
        pass
    conn.setblocking(0)
    s.setblocking(0)
    while True:
        try:
            request = conn.recv(buffer_size)
            s.sendall(request)
        except socket.error as err:
            pass

        try:
            reply = s.recv(buffer_size)
            conn.sendall(reply)
        except socket.error as e:
            pass


def http_request(webserver, port, conn, client_data, addr):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.connect((webserver, port))
        server_socket.send(client_data.encode('utf-8'))

        while True:
            response = server_socket.recv(buffer_size)
            if (len(response) > 0):
                conn.send(response)
                print(f'[*] Request done ! {addr[0]}')
                print('Response : ', response)
            else:
                conn.send(response)
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
            start_new_thread(conn_string, (conn, client_data, addr))
        except KeyboardInterrupt:
            client_socket.close()
            print(f"[*] KeyboardInterrupt :-> Proxy server Shutting Down")
            sys.exit()

start()

from time import sleep

default_port = 1234
from receiv import reciev
from send import send_message
from _thread import start_new_thread


def sendData(message: bytes, default_port: int) -> None:
    print("new thread started")
    start_new_thread(reciev, (default_port,))
    sleep(2)
    send_message(message, default_port)




#message = b"POST http://ocsp.pki.goog/gts1c3 HTTP/1.1\r\nHost: ocsp.pki.goog\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0\r\nAccept: */*\r\nAccept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nContent-Type: application/ocsp-request\r\nContent-Length: 83\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\n\r\n0Q0O0M0K0I0\t\x06\x05+\x0e\x03\x02\x1a\x05\x00\x04\x14\xc7.y\x8a\xdd\xffa4\xb3\xba\xedGB\xb8\xbb\xc6\xc0$\x07c\x04\x14\x8at\x7f\xaf\x85\xcd\xee\x95\xcd=\x9c\xd0\xe2F\x14\xf3q5\x1d'\x02\x10nF\x9d\xaf\x80*\x1e@\x12P\xbfo\x9a\x10Q\xe0"
#message = b'HTTP/1.ed\r\nDate: Thu, 05 Jan 2023 15:52:35 GMT\r\nServer:Serv15:52:35 GMT\r\nServer:Server:Server: Apache\r\nConnection: close\r\nETag: "11a7-29045ccd3d840"\r\n\r\n'
message = b"Test"
#Todo gerer l'envoie de paquet trop gros pour etre crypté par le rsa
print(len(message))
sendData(message, default_port)



#!/usr/bin/env python3
import socket
import paramiko
import threading
import logging

# Configurar o logging
logging.basicConfig(
    filename="honeypot.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(message)s"
)

class SSH_Server(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        logging.info(f"Username: {username}, Password: {password}")
        print(f"{username}:{password}")
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_FAILED

def handle_connection(client_sock, server_key):
    client_addr = client_sock.getpeername()[0]  # Obtém o endereço IP do cliente
    transport = paramiko.Transport(client_sock)
    transport.add_server_key(server_key)
    ssh = SSH_Server()
    logging.info(f"Connection from {client_addr}")  # Log do IP do cliente
    transport.start_server(server=ssh)


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('0.0.0.0', 5777))
    server_sock.listen(100)

    server_key = paramiko.RSAKey.generate(2048)

    while True:
        client_sock, client_addr = server_sock.accept()
        print(f"Connection: {client_addr[0]}:{client_addr[1]}")
        t = threading.Thread(target=handle_connection, args=(client_sock, server_key))
        t.start()

if __name__ == "__main__":
    main()

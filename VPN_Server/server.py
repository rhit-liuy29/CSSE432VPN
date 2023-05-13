import socket
import struct
import sys
import os


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def client_program():
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_(IP)_address> <server_port_number>")
        sys.exit()
    #host = socket.gethostname()
    #host = sys.argv[2]
    port = int(sys.argv[2])

    server_ip = socket.gethostbyname(sys.argv[1])
    print("server IP: ", server_ip)

    server_addr = (server_ip, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect(server_addr)  # connect to the server

    message = "server"

    client_socket.send(message.encode())  # send message, default encoding encoding="utf-8", errors="strict"
    print(os.path.dirname(os.path.realpath(__file__)))
    with open(r'/etc/openvpn/server/tc.key', 'rb') as f:
        file_contents = f.read()
        # print(file_contents)
        send_msg(client_socket, file_contents)
        print("tlc-crypt sent")
        f.close()

    data = client_socket.recv(4096).decode()  # receive response
    try:
        with open(r'/etc/openvpn/server/ca.crt', 'w') as f:
            f.write(data)
            f.close()
            print("ca cert has been written into ca.crt")
    except FileNotFoundError:
        print("The directory does not exist")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    middle_path = '/etc/openvpn/server/easy-rsa/pki/reqs'
    file_list = os.listdir(path=middle_path)[0]
    server_req = open(middle_path+'/'+file_list, "r")
    data = server_req.read();
    client_socket.send(data.encode())
    server_req.close()
    print("receiving crt size......")
    data = client_socket.recv(1024).decode()
    try:
        with open(r'/etc/openvpn/server/server.crt', 'wb') as f:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                f.write(data)
        print("server cert has been written into server.crt")
        f.close()
    except FileNotFoundError:
        print("The directory does not exist")
        client_socket.close()

    #file_size = os.path.getsize(r'/etc/openvpn/server/tc.key')
    #client_socket.send(str(file_size).encode('utf8'))

    client_socket.close()
    exit(1)
        # close the connection


if __name__ == '__main__':
    client_program()
import socket
import sys
import os
import struct


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

def server_program():
    # get the hostname
    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)
    print("Host name: " + str(host))
    print("Host IP: " + str(host_ip))
    # host = 'localhost'
    if len(sys.argv) != 2:
       print("Usage: python server.py <port_number>")
       sys.exit()
    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind(('', port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    while True: # keep looping looking for new clients when previous closes
         conn, address = server_socket.accept()  # accept new connection
         print("Connection from: " + str(address))
         # receive data stream. it won't accept data packet greater than 1024 bytes
         data = conn.recv(1024).decode()
         if data == 'client':
           print("incoming connection from client")
           ca_cert = open("/home/rose/easy-rsa/pki/ca.crt", "r")
           data = ca_cert.read()
           conn.send(data.encode())  # send data to the client
           ca_cert.close()
           print("ca_cert sent")

           data = conn.recv(4096).decode()
           with open("/home/rose/easy-rsa/pki/client_req.req", "w") as f:
               f.write(data)
               f.close()
               print("client_req has been written into /home/rose/easy-rsa/pki/client_req.req")
           os.system("./signing_client.sh")
           file_size = os.path.getsize("/home/rose/easy-rsa/pki/issued/clientreq.crt")
           conn.send(str(file_size).encode())
           client_crt = open("/home/rose/easy-rsa/pki/issued/clientreq.crt", "rb")
           data = client_crt.read()
           conn.send(data)
           client_crt.close()
           print("client_crt sent")

           tc_key = open("/home/rose/easy-rsa/pki/tc.key", "rb")
           data = tc_key.read()
           conn.send(data)
           tc_key.close()
           print("tc_key sent")

           conn.close()  # close the connection
           os.system("./removing_client.sh")
         elif data == 'server':
           print("incoming connection from server")
           with open("/home/rose/easy-rsa/pki/tc.key", "wb") as f:
               data = recv_msg(conn)
               f.write(data)
               f.close()
               print("tc.key has been written into /home/rose/easy-rsa/pki/tc.key")

           ca_cert = open("/home/rose/easy-rsa/pki/ca.crt", "r")
           data = ca_cert.read()
           conn.send(data.encode())
           ca_cert.close()
           print("ca_cert sent")

           data = conn.recv(4096).decode()
           with open("/home/rose/easy-rsa/pki/server_req.req", "w") as f:
               f.write(data)
               f.close()
               print("server_req has been written into /home/rose/easy-rsa/pki/server_req.req")
           os.system("./signing_server.sh")
           file_size = os.path.getsize("/home/rose/easy-rsa/pki/issued/serverreq.crt")
           conn.send(str(file_size).encode())
           server_crt = open("/home/rose/easy-rsa/pki/issued/serverreq.crt", "rb")
           data = server_crt.read()
           conn.send(data)
           server_crt.close()
           print("server crt sent")
           conn.close()
           os.system("./removing_server.sh")
    conn.close()


if __name__ == '__main__':
    server_program()
import socket
import sys
import os

client_setting = 'client\ndev tun\nproto udp\nremote 178.79.190.212 443\nresolv-retry ' \
                 'infinite\nnobind\npersist-key\npersist-tun\nremote-cert-tls server\nauth SHA512\ncipher ' \
                 'AES-256-CBC\nignore-unknown-option block-outside-dns\nverb 3'



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

    message = "client"

    client_socket.send(message.encode())  # send message, default encoding encoding="utf-8", errors="strict"
    data = client_socket.recv(4096).decode()  # receive response
    try:
        with open(r'.\ca_cert.txt', 'w') as f:
            f.write(data)
            f.close()
            print("ca.cert has been written into ca_cert.txt")
    except FileNotFoundError:
        print("The directory does not exist")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    middle_path = '\\easy-rsa\\EasyRSA-3.1.2\\pki\\reqs'
    file_list = os.listdir(path=(dir_path + middle_path))[0]
    client_req = open(dir_path+middle_path+'\\'+file_list, "r")
    data = client_req.read();
    client_socket.send(data.encode())
    client_req.close()
    data = client_socket.recv(1024).decode()
    cert_size = int(data)
    print("cert has a size of " + str(cert_size) + " bytes")
    try:
        with open(r'.\client_cert.txt', 'wb') as f:
            while True:
                data = client_socket.recv(cert_size)
                if not data:
                    break
                f.write(data)
        print("client_req.crt has been written into client_cert.txt")
        f.close()
    except FileNotFoundError:
        print("The directory does not exist")

    try:
        with open(r'.\tc_key.key', 'wb') as f:
            while True:
                f_data = client_socket.recv(4096)
                print(f_data)
                if not f_data:
                    break
                f.write(f_data)
        print("tls_crypt.crt has been written into tc_key.key")
        f.close()
    except FileNotFoundError:
        print("The directory does not exist")
    client_socket.close()  # close the connection

    with open(r".\client.ovpn", "w") as f:
        f.write(client_setting)
        contents = open(r'.\ca_cert.txt').read()
        f.write("\n<ca>\n")
        f.write(contents[contents.index("-----BEGIN CERTIFICATE-----"):contents.index("-----END CERTIFICATE-----")])
        f.write("-----END CERTIFICATE-----")
        f.write("\n</ca>")
        contents = open(r'.\client_cert.txt').read()
        f.write("\n<cert>\n")
        f.write(contents[contents.index("-----BEGIN CERTIFICATE-----"):contents.index("-----END CERTIFICATE-----")])
        f.write("-----END CERTIFICATE-----")
        f.write("\n</cert>")
        middle_path = '\\easy-rsa\\EasyRSA-3.1.2\\pki\\private'
        file_list = os.listdir(path=(dir_path + middle_path))[0]
        contents = open(dir_path + middle_path + '\\' + file_list).read()
        f.write("\n<key>\n")
        f.write(contents[contents.index("-----BEGIN PRIVATE KEY-----"):contents.index("-----END PRIVATE KEY-----")])
        f.write("-----END PRIVATE KEY-----")
        f.write("\n</key>")
        contents = open(r'.\client_cert.txt').read()
        f.write("\n<tls-crypt>\n")
        f.write(contents[contents.index("-----BEGIN OpenVPN Static key V1-----"):contents.index("-----END OpenVPN Static key V1-----")])
        f.write("-----END OpenVPN Static key V1-----")
        f.write("\n</tls-crypt>\n")
        print("write complete")
        f.close()
        os.remove("ca_cert.txt")
        os.remove("client_cert.txt")
        os.remove("tc_key.key")


if __name__ == '__main__':
    client_program()
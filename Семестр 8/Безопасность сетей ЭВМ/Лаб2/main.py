import socket

sock = socket.socket()
sock.connect(("192.168.136.131", 21))

print(sock.recv(1024).decode())
sock.send(b"USER WIN-JPEUI0UM53J\\FTP\r\n")
print(sock.recv(1024).decode())
sock.send(b"PASS Fktrcfylh.2000\r\n")
print(sock.recv(1024).decode())
sock.send(b"PASV\r\n")
data = sock.recv(1024)
x = data[27:-4].decode("UTF-8").split(',')
port = (int(x[4]) << 8) + int(x[5])
sock.send(b"RETR db.txt\r\n")
data = sock.recv(1024)
print(data)

data_sock = socket.socket()
data_sock.connect(("192.168.136.131", port))
data = data_sock.recv(10240).decode("UTF-8")
print(data)

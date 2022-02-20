import socket


class FTP:
    __ALL = 10240

    __socket = None
    __IP = None
    __user = None
    __password = None
    __port = None
    __data_socket = None

    def __init__(self):
        self.__socket = socket.socket()

    def __load_data(self, size: int) -> bytes:
        self.__data_socket = socket.socket()
        self.__data_socket.connect((self.__IP, self.__port))
        data = self.__data_socket.recv(size)
        self.__data_socket.close()
        return data

    def __send_data(self, data: bytes) -> bytes:
        self.__data_socket = socket.socket()
        self.__data_socket.connect((self.__IP, self.__port))
        self.__data_socket.send(data)
        self.__data_socket.close()
        return data

    def __open_data_connection(self):
        self.__socket.send(b"PASV\r\n")
        ret = ['']
        while ret == ['']:
            ret = self.__socket.recv(self.__ALL)[27:-4].decode("UTF-8").split(',')
        self.__port = (int(ret[4]) << 8) + int(ret[5])

    def connect(self, ip: str, user: str, password: str) -> bool:
        try:
            self.__IP = ip
            self.__user = user
            self.__password = password
            self.__socket.connect((self.__IP, 21))

            self.__socket.recv(self.__ALL)
            self.__socket.send(bytes("USER " + self.__user + "\r\n", encoding="UTF-8"))
            self.__socket.recv(self.__ALL)
            self.__socket.send(bytes("PASS " + self.__password + "\r\n", encoding="UTF-8"))
            ret = self.__socket.recv(self.__ALL).split(b" ")[0]
            if ret == b"230":
                return True
            return False
        except:
            return False

    def list_dir(self):
        self.__open_data_connection()
        self.__socket.send(bytes("LIST\r\n", encoding="UTF-8"))
        data = self.__load_data(self.__ALL).decode('utf-8')
        print(data)
        self.__socket.recv(self.__ALL)

    def change_dir(self, dir: str):
        if dir == '..':
            self.__socket.send(bytes("CDUP\r\n", encoding="UTF-8"))
        else:
            self.__socket.send(bytes("CWD " + dir + "\r\n", encoding="UTF-8"))
        self.__socket.recv(self.__ALL)

    def load_file(self, filename: str):
        self.__open_data_connection()

        self.__socket.send(bytes("SIZE " + filename + "\r\n", encoding="UTF-8"))
        size = (int(self.__socket.recv(self.__ALL).decode("UTF-8").split(' ')[1]))

        self.__socket.send(bytes("RETR " + filename + "\r\n", encoding="UTF-8"))
        data = self.__load_data(size)
        self.__socket.recv(self.__ALL)
        self.__socket.recv(self.__ALL)

        with open(filename, 'wb') as file:
            file.write(data)

    def send_file(self, filename: str):
        self.__open_data_connection()

        self.__socket.send(bytes("STOR " + filename + "\r\n", encoding="UTF-8"))

        data = b""
        with open(filename, "rb") as file:
            data = file.read()
        self.__send_data(data)
        self.__socket.recv(self.__ALL)
        self.__socket.recv(self.__ALL)

    def get_dir(self) -> str:
        self.__open_data_connection()
        self.__socket.send(bytes("PWD\r\n", encoding="UTF-8"))
        data = self.__socket.recv(self.__ALL)[5:-25]
        return data.decode(encoding="UTF-8")

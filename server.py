import socket
import os
from Global import get_massage


class Server:
    server = 0
    client_socket = 0
    address = 0

    def __init__(self):
        # init server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), 1234))
        self.server.listen(5)
        self.handler()

    def init_client_socket(self):
        self.client_socket, self.address = self.server.accept()
        print(f"connection formm {self.address} has been established")

    def handler(self):
        # handle the server side

        self.init_client_socket()

        while True:
            data = get_massage(self.client_socket)

            if data == "upload":
                self.receive_file()

            elif data == "download":
                self.send_file()

            elif data == "close":
                self.client_socket.close()
                print("client disconnected")
                exit()

    def send_file(self):
        # the path that the sever send files to the client
        filename = self.choose_file_from_list()
        file_path = ".\\recive\\" + filename

        # sending the file
        with open(file_path, "rb") as f:
            self.client_socket.send(str(os.path.getsize(file_path)).encode())
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.client_socket.sendall(data)

        print("file sent")

    def choose_file_from_list(self):

        # the path that the sever send files to the client
        file_list_path = ".\\recive"
        dir_list = os.listdir(file_list_path)
        files_list = "Current file list:\n"

        # prints the file list
        for file in dir_list:
            files_list +=str(file) + "\n"
        self.client_socket.send(files_list.encode())
        filename = get_massage(self.client_socket)
        return filename

    def receive_file(self):
        # the path that the sever store the file that the client sent
        file_path = ".\\recive"
        filename = get_massage(self.client_socket)
        file_size = int(get_massage(self.client_socket))
        file_path = file_path + filename

        # read the file from client and store it
        with open(file_path, 'wb') as f:
            while file_size > 0:
                data = get_massage(self.client_socket)
                if not data:
                    break
                file_size -= len(data)
                f.write(data)
            print("download completed: ", filename)


s = Server()
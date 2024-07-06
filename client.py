import socket
import os


class Client:
    client = 0

    def __init__(self):
        # init client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((socket.gethostname(), 1234))
        self.handler()

    def handler(self):
        # handle the client side

        while True:
            client_input = input("choose input: upload, download or close: ")
            self.client.send(client_input.encode())

            # if the user write close
            if client_input == "close":
                self.client.close()
                print("disconnecting...")
                print("bye!")
                break

            # if the user write upload
            elif client_input == "upload":
                self.send_file()

            # if the user write download
            elif client_input == "download":
                self.download_file()
            else:
                print("\033[38;2;224;108;117mChoose one of the options above ↑\033[0m")

    def choose_file_to_download(self):
        # get from user the file name
        files = self.client.recv(1024).decode()
        print(files)
        filename = input("enter file name(example: text.txt): ")

        # if user input file is not found
        while filename not in files:
            print("no such file, try again")
            filename = input("enter file name(example: text.txt): ")
        self.client.send(filename.encode())
        return filename

    def download_file(self):

        filename = self.choose_file_to_download()
        file_path = "D:\\Downloads\\"
        file_size = int(self.client.recv(1024).decode())
        file_path = file_path + filename

        with open(file_path, 'wb') as f:
            while file_size > 0:
                data = self.client.recv(1024)
                if not data:
                    break
                file_size -= len(data)
                f.write(data)
            print("download completed: ", filename)

    def send_file(self):
        # get path
        path = input("enter file path to download(exemple: .\\image\\fileName.txt): ")

        # if path is not valid
        while not os.path.isfile(path):
            print("file not found, Try again")
            path = input("enter file path to download(exemple: .\\image\\fileName.txt): ")
        self.client.send(path.split("\\")[-1].encode())

        # send the file
        with open(path, "rb") as f:
            self.client.send(str(os.path.getsize(path)).encode())
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.client.sendall(data)

        print('upload was successful!')


c = Client()
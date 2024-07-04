
def get_massage(socket):
    try:
        data = socket.recv(1024)
        return data.decode()
    except ConnectionError:
        print("Error")

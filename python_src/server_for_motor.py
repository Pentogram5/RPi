import socket
import threading

import SC_move

class RobotControlServer:
    def __init__(self, host='0.0.0.0', port=8888):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Сервер запущен на {host}:{port}")

    def handle_client(self, client_socket):
        while True:
            command = client_socket.recv(1024).decode('utf-8')
            if not command:
                break
            print(f"Получена команда: {command}")
            self.execute_command(command)
        client_socket.close()

    def execute_command(self, command):
        direction = int(command[0])
        speed = int(command[1]) 
        setDirection(direction, speed)


    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Подключено к {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":

    server = RobotControlServer()
    server.start()
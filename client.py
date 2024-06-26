import socket
import regex as re
import threading

SERVER = 'localhost'
PORT = 8888

class Client:
    def __init__(self, SERVER, PORT):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect((SERVER, PORT))
            print(f"Connecté au serveur sur {SERVER}:{PORT}")  
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            return

        self.client_connect = True
                   
        client_receiver = threading.Thread(target=self.receive_from_server)
        client_receiver.start()
        self.send_to_server()
    
    def send_to_server(self):
        while self.client_connect:
            message = input('>')
            if message:
                self.client_socket.send(message.encode('utf-8'))
                if message == "exit":
                    self.client_connect = False
                    break

    def receive_from_server(self):
        while self.client_connect:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                if message in ["", "end"]:
                    self.client_connect = False
                    break
                print("\n", message)
            except Exception as e:
                print(f"Erreurs lors de la récupération du message : {e}")
                self.client_connect = False # a modifier pour que ça se fasse que si la connexion est coupé
    
    def __del__(self):
        self.client_socket.close()

client = Client(SERVER, PORT)


import socket
import threading

HOST = 'localhost'
PORT = 8888


class Server:
    def __init__(self, HOST, PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)
        
        self.lock_buff = threading.Lock()
        self.buff_message = []

        print(f"Serveur démarré sur {HOST}:{PORT}")

        self.lock_liste_cl = threading.Lock()
        self.clients = []
       
        self.running = True
        
        send = threading.Thread(target=self.send_to_all)
        send.start()

        self.run()
    
    def run(self):
        while self.running:
            
            try:
                client_socket, addr = self.server_socket.accept()
                with self.lock_liste_cl:
                    self.clients.append(client_socket)
                print(f"Nouvelle connexion : {addr}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, ))
                client_handler.start()
            except KeyboardInterrupt:
                print("Arrêt du serveur par l'utilisateur.")
                self.__del__()

    def handle_client(self, client_socket):
        state = True
        while state and self.running:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                elif message in ["", "exit"]:
                    state = False
                    with self.lock_liste_cl:
                        self.clients.remove(client_socket)
                    break
                else:

                    print(message)
                    with self.lock_buff:
                        self.buff_message.append(message)
            except Exception as e:
                print(f"Erreur lors de la réception du message : {e}")
                break
        client_socket.close()

    def send_to_all(self):
        while self.running:
            with self.lock_buff:
                if self.buff_message:

                    with self.lock_liste_cl:
                        for socket in self.clients:
                            try:
                                socket.send(self.buff_message[0].encode('utf-8'))
                            except Exception as e:
                                print(e)
                        self.buff_message.clear()
            
        

    def __del__(self):
        self.server_cocket.close()

if __name__ == "__main__":
    server = Server(HOST, PORT)

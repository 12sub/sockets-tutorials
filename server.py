import socket
import threading

HEADER = 64
PORT = 5500
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#Starting a new thread using handle_client function 
#used to handle individual connection between the client and the server
#so that when a new connection occurs, the threading functions passes the connection to handle_client
#and give the target AKA handle_client the arguments we are passing to the function
def handle_client(conn, addr):
    #This function runs for each thread concurrently
    print(f"[NEW CLIENT] {addr} connected")
    
    #Receives information from the client
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            #Printing the address and the message
            if msg == DISCONNECT_MESSAGE:
                break
            print(f"[{addr}] {msg}")
    conn.close()
#Handling new connections to the server
def start():
    #Listens for connection to client
    server.listen()
    #Printing what ip address the server is running on
    print(f"[LISTENING] Server is listening on {SERVER}")
    #Runs an infinite loop until the clients connects to the server
    while True:
        conn, addr = server.accept()
        #running the threads | passing the target which is the handle_client and the arguments
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #This shows us how many active threads are in the process/server
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
print("Starting server....")
start()
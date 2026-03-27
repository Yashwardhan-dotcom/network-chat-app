import socket
import threading

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

name = input("Enter your name: ")

# Receive messages
def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "NAME":
                client.send(name.encode())
            else:
                print(message)
        except:
            print("Error! Disconnected.")
            client.close()
            break

# Send messages
def write():
    while True:
        msg = input("")
        message = f"{name}: {msg}"
        client.send(message.encode())

# Run threads
threading.Thread(target=receive).start()
threading.Thread(target=write).start()

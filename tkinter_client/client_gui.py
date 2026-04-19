import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatClient:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        self.root = tk.Tk()
        self.root.title("Chat App")

        self.name = simpledialog.askstring("Name", "Enter your name:", parent=self.root)

        # Chat area
        self.chat_area = scrolledtext.ScrolledText(self.root)
        self.chat_area.pack(padx=20, pady=10)
        self.chat_area.config(state='disabled')

        # Message input
        self.msg_entry = tk.Entry(self.root, width=50)
        self.msg_entry.pack(padx=20, pady=5)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.write)
        self.send_button.pack(pady=5)

        # Enter key support
        self.root.bind('<Return>', lambda event: self.write())

        # Start receiving thread
        threading.Thread(target=self.receive).start()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.mainloop()

    def write(self):
        message = f"{self.name}: {self.msg_entry.get()}"
        self.client.send(message.encode())
        self.msg_entry.delete(0, tk.END)

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode()

                if message == "NAME":
                    self.client.send(self.name.encode())
                else:
                    self.chat_area.config(state='normal')
                    self.chat_area.insert(tk.END, message + "\n")
                    self.chat_area.yview(tk.END)
                    self.chat_area.config(state='disabled')
            except:
                break

    def close(self):
        self.client.close()
        self.root.destroy()


# Run client
ChatClient("127.0.0.1", 12345)

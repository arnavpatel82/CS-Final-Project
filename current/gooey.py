import tkinter as tk
import socket
import threading

class ChatGUI:
    def __init__(self, server_address, server_port):
        # Initialize the GUI
        self.root = tk.Tk()
        self.root.title("Chat Client")

        # Create the login form
        self.login_frame = tk.Frame(self.root)
        tk.Label(self.login_frame, text="Username: ").grid(row=0, column=0)
        self.username_input = tk.Entry(self.login_frame)
        self.username_input.grid(row=0, column=1)
        tk.Label(self.login_frame, text="Password: ").grid(row=1, column=0)
        self.password_input = tk.Entry(self.login_frame, show="*")
        self.password_input.grid(row=1, column=1)
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2)

        # Create the registration form
        self.registration_frame = tk.Frame(self.root)
        tk.Label(self.registration_frame, text="Username: ").grid(row=0, column=0)
        self.new_username_input = tk.Entry(self.registration_frame)
        self.new_username_input.grid(row=0, column=1)
        tk.Label(self.registration_frame, text="Password: ").grid(row=1, column=0)
        self.new_password_input = tk.Entry(self.registration_frame, show="*")
        self.new_password_input.grid(row=1, column=1)
        tk.Label(self.registration_frame, text="Confirm Password: ").grid(row=2, column=0)
        self.confirm_password_input = tk.Entry(self.registration_frame, show="*")
        self.confirm_password_input.grid(row=2, column=1)
        self.register_button = tk.Button(self.registration_frame, text="Register", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2)

        # Show the login frame by default
        self.login_frame.pack()

        # Create the chat log
        self.chat_log = tk.Text(self.root, state=tk.DISABLED)
        self.chat_log.pack(expand=True, fill=tk.BOTH)

        # Create the message input field
        self.message_input = tk.Entry(self.root)
        self.message_input.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.message_input.bind("<Return>", self.send_message)

        # Create the send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message, state=tk.DISABLED)
        self.send_button.pack(side=tk.RIGHT)

        # Create the socket connection to the chat server
        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logout_button = Button(self.Window, text="Logout", command=self.logout)
        self.logout_button.place(relx=0.9, rely=0.008, relheight=0.06, relwidth=0.1)

    def logout(self):
        # Send a "LOGOUT" message to the chat server
        self.send(json.dumps({"action": "logout"}))
        response = json.loads(self.recv())
        if response["status"] == 'ok':
            # Logout successful, destroy the chat window and show the login window
            self.Window.destroy()
            self.login()
        else:
            # Logout failed, show an error message
            tk.messagebox.showerror("Logout Error", "Failed to logout")

    def login(self):
        # Get the username and password from the input fields
        username = self.username_input.get()
        password = self.password_input.get()

        # Authenticate the user with the server
        self.socket.connect((self.server_address, self.server_port))
        self.socket.sendall(f"LOGIN {username} {password}".encode())
        response = self.socket.recv(1024).decode()

        if response == "OK":
            # Authentication successful, show the chat UI
            self.login_frame.pack_forget()
            self.registration_frame.pack_forget()
            self.send_button.config(state=tk.NORMAL)
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
        else:
            # Authentication failed, show an error message
            tk.messagebox.showerror("Login Error", "Invalid username or password")

    def register(self):
        # Get the username and password from the input fields
        new_username = self.new_username_input.get()
        new_password = self.new_password_input.get()
        confirm_password = self.confirm_password_input.get()

        # Check that the passwords match
        if new_password != confirm_password:
            tk.messagebox.showerror("Registration Error", "Passwords do not match")
            return

        # Create a new user account on the server
        self.socket.connect((self.server_address, self.server_port))
        self.socket.sendall(f"REGISTER {new_username} {new_password}".encode())
        response = self.socket.recv(1024).decode()

        if response == "OK":
            # Registration successful, show the login form
            self.registration_frame.pack_forget()
            self.login_frame.pack()
            tk.messagebox.showinfo("Registration Success", "Account created successfully")
        else:
            # Registration failed, show an error message
            tk.messagebox.showerror("Registration Error", "Username already taken")

    def send_message(self, event=None):
        # Get the message from the input field
        message = self.message_input.get()

        # Clear the input field
        self.message_input.delete(0, tk.END)

        # Send the message to the server
        self.socket.sendall(message.encode())

        # Add the message to the chat log
        self.add_message("Me: " + message)

    def receive_messages(self):
        while True:
            # Receive a message from the server
            message = self.socket.recv(1024).decode()

            # Add the message to the chat log
            self.add_message(message)

    def add_message(self, message):
        # Add the message to the chat log
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)


    def run(self):
        # Start the GUI event loop
        self.root.mainloop()

# Example usage
if __name__ == "__main__":
    chat_gui = ChatGUI("localhost", 8000)
    chat_gui.run()

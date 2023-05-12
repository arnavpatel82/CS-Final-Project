import random

def flip_bits(msg):
    """
    Emulate a "noisy location" by randomly flipping bits of the message
    """
    flipped_msg = ""
    for i in range(len(msg)):
        if random.random() < 0.05:  # flip bits with 5% probability
            flipped_msg += "0" if msg[i] == "1" else "1"
        else:
            flipped_msg += msg[i]
    return flipped_msg

class ChatClient:
    """
    A client that sends and receives messages in a chatroom
    """
    def __init__(self, server, name):
        self.server = server
        self.name = name
        self.sent_msgs = {}  # stores the checksums of sent messages

    def send_msg(self, msg):
        """
        Send a message to the server
        """
        checksum = self.compute_checksum(msg)
        self.sent_msgs[checksum] = msg  # store the original message with its checksum
        self.server.receive_msg(self.name, flip_bits



# Server code
import random

def receive_message(message):
    # Randomly flip some bits of the message
    for i in range(len(message)):
        if random.random() < 0.1: # 10% chance
            message[i] = '1' if message[i] == '0' else '0'
            
    return message

# Client code

import zlib   

def send_message(message):  
    # Calculate checksum of message
    checksum = zlib.adler32(message.encode())
    
    # Send message and checksum to server    
    send(message)   
    send(checksum) 

def receive_message():    
    message = receive()   
    checksum = receive()
    
    # Calculate checksum of received message   
    received_checksum = zlib.adler32(message.encode())
    
    # Compare checksums and request retransmission if different    
    if checksum != received_checksum:
        send("retransmit")   
        return receive_message()   
    else:
        return message

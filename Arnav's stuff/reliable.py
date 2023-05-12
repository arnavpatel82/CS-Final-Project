import reedsolo
import random
import base64

class MessageSender:
    def __init__(self, message, checksum_size=100):
        self.message = message
        self.checksum_size = checksum_size
    
    def generate_noisy_message(self, noise_simulator, error_rate):
        # Compute the checksum of the message
        checksum = reedsolo.RSCodec(noise_simulator.checksum_size).encode(self.message)[-noise_simulator.checksum_size:]

        # Send the message and its checksum to the noise simulator
        noisy_message = self.message + checksum
        # print("Noisy message (before error correction):", noisy_message)

        # Simulate noise and add redundancy to the message
        noisy_message = noise_simulator.simulate_noise(noisy_message, error_rate)
        redundant_message = noise_simulator.add_redundancy(noisy_message)
        # print("Noisy message (after error correction):", noisy_message)
        # print("Redundant message:", redundant_message)

        # Base64 encode the message for JSON serialization
        encoded_message = base64.b64encode(redundant_message).decode('utf-8')

        return encoded_message

class NoiseSimulator:
    def __init__(self, packet_size=512, error_rate=0.1, checksum_size=100):
        self.packet_size = packet_size
        self.error_rate = error_rate
        self.checksum_size = checksum_size

    def simulate_noise(self, message, error_rate):
        # Generate a list of random errors
        error_list = [1 if random.random() < error_rate else 0 for _ in range(len(message))]
        
        # Apply the errors to the message
        noisy_message = bytearray(message)
        for i in range(len(noisy_message)):
            noisy_message[i] ^= error_list[i]

        return bytes(noisy_message)

    def add_redundancy(self, message):
        # Add a Reed-Solomon error correction code to the message
        redundant_message = reedsolo.RSCodec(self.checksum_size).encode(message)

        return redundant_message

class MessageReceiver:
    def __init__(self, received_message, checksum_size=100):
        self.received_message = received_message
        self.checksum_size = checksum_size
    
    def correct_errors(self):
        # Receive the encoded message from the noise simulator
        encoded_message = self.received_message

        # Base64 decode the message
        redundant_message = base64.b64decode(encoded_message)

        # Verify the checksum of the received message
        checksum = redundant_message[-self.checksum_size:]
        received_checksum = self.received_message[-self.checksum_size:]
        decoded_redundant_message = redundant_message[:-self.checksum_size]
        computed_checksum = reedsolo.RSCodec(self.checksum_size).decode(decoded_redundant_message)[-self.checksum_size:]
        if received_checksum != computed_checksum:
            # Handle the error by correcting the errors in the redundant data
            try:
                decoded_redundant_message, _, _ = reedsolo.RSCodec(self.checksum_size).decode(redundant_message)
            except reedsolo.ReedSolomonError:
                # Unable to correct errors in the message
                return ""

        # Decrypt the corrected data to recover the original message
        decoded_message = decoded_redundant_message[:-self.checksum_size]
        original_message = decoded_message.decode('utf-8')
        # print("Received message (after error correction):", decoded_redundant_message)
        # print("Decrypted message:", original_message)

        return original_message
    
if __name__ == "__main__":
    message = b"hello world"
    noise_simulator = NoiseSimulator()
    sender = MessageSender(message)
    noisy_message = sender.generate_noisy_message(noise_simulator, 0.2)
    print(noisy_message)
    receiver = MessageReceiver(noisy_message)
    received_message = receiver.correct_errors()
    print(received_message)
import reedsolo
import random

# Sender (1.py)

# Generate the message
message = b"hello world"
print("Original message:", message.decode('utf-8'))

# Compute the checksum of the message
checksum = reedsolo.RSCodec(10).encode(message)[-10:]

# Send the message and its checksum to the noise simulator
noisy_message = message + checksum
print("Noisy message (before error correction):", noisy_message.decode('utf-8'))

# Noise simulator (2.py)

# Simulate noise by flipping some bits in the message
def simulate_noise(message, error_rate):
    noisy_message = bytearray(message)
    for i in range(len(noisy_message)):
        if random.random() < error_rate:
            noisy_message[i] ^= 1
    return bytes(noisy_message)

# Add redundancy to the message using an error correction code
def add_redundancy(message):
    return reedsolo.RSCodec(10).encode(message)

# Simulate noise and add redundancy to the message
error_rate = 0.1
noisy_message = simulate_noise(noisy_message, error_rate)
redundant_message = add_redundancy(noisy_message)
print("Noisy message (after error correction):", noisy_message.decode('utf-8'))
print("Redundant message:", redundant_message.decode('utf-8'))

# Receiver (3.py)

# Receive the redundant message and its checksum from the noise simulator
received_message = redundant_message
checksum = received_message[-10:]
print("Received message (before error correction):", received_message.decode('utf-8'))

# Verify the checksum of the received message
received_checksum = received_message[-10:]
decoded_redundant_message = received_message[:-10]
computed_checksum = reedsolo.RSCodec(10).decode(decoded_redundant_message)[-10:]
if received_checksum != computed_checksum:
    # Handle the error by correcting the errors in the redundant data
    decoded_redundant_message = reedsolo.RSCodec(10).decode(received_message)

# Decrypt the corrected data to recover the original message
decoded_message = decoded_redundant_message[:-10]
original_message = decoded_message.decode('utf-8')
print("Received message (after error correction):", decoded_redundant_message.decode('utf-8'))
print("Decrypted message:", original_message)
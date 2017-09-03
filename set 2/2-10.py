import base64
import pprint
import sys
from Crypto.Cipher import AES

with open('10.txt', 'r') as input_file:
    input_text = input_file.read()
    
input = base64.b64decode(input_text)
key = b'YELLOW SUBMARINE'
iv = b'\x00' * 16

def pad_input(input, length, pad_char=b'\x04'):
    if len(input) >= length:
        return input
    pad_length = length - len(input)
    padded = bytearray(input) + (pad_char * pad_length)
    return bytes(padded)

def decrypt_AES_ECB(key, text):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(text)
    return decrypted
    
def encrypt_AES_ECB(key, text):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(text)
    return encrypted
    
def decrypt_AES_CBC(key, iv, text):
    broken = [text[i:i+16] for i in range(0, len(text), 16)]
    decrypted = b''

    for index, block in enumerate(broken):
        if index == 0:
            prev_block = iv
        else:
            prev_block = broken[index-1]
        step1 = decrypt_AES_ECB(key, block)
        plaintext_int = int.from_bytes(step1, sys.byteorder) ^ int.from_bytes(prev_block, sys.byteorder)
        plaintext = plaintext_int.to_bytes(16, sys.byteorder)
        decrypted += plaintext
    
    decrypted = decrypted.rstrip(b'\x04')
    return decrypted
    
def encrypt_AES_CBC(key, iv, text):
    if (len(text)) % 16 != 0:
        padding = 16 - (len(text) % 16)
    else:
        padding = 0
        
    padded_text = pad_input(text, len(text)+padding)
    broken = [padded_text[i:i+16] for i in range(0, len(padded_text), 16)]
    encrypted = b''

    prev_block = iv
    for index, block in enumerate(broken):
        step1_int = int.from_bytes(prev_block, sys.byteorder) ^ int.from_bytes(block, sys.byteorder)
        step1 = step1_int.to_bytes(16, sys.byteorder)
        ciphertext = encrypt_AES_ECB(key, step1)
        encrypted += ciphertext
        prev_block = ciphertext
        
    return encrypted
    
result = decrypt_AES_CBC(key, iv, input)
print(result.decode())

encrypt_me = b'bonerbonerbonerbonerboner'
encrypted = encrypt_AES_CBC(key, iv, encrypt_me)
print(encrypted)
decrypted = decrypt_AES_CBC(key, iv, encrypted)
print(decrypted)
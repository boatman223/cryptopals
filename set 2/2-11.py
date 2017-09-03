import sys
import secrets
from Crypto.Cipher import AES

def pad_input(input, length, pad_char=b'\x04'):
    if len(input) >= length:
        return input
    pad_length = length - len(input)
    padded = bytearray(input) + (pad_char * pad_length)
    return bytes(padded)

def encrypt_AES_ECB(key, text):
    if (len(text)) % 16 != 0:
        padding = 16 - (len(text) % 16)
    else:
        padding = 0
        
    padded_text = pad_input(text, len(text)+padding)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(padded_text)
    return encrypted

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
    
def is_ECB(text):
    broken = [text[i:i+16] for i in range(0, len(text), 16)]
    for segment in broken:
        if broken.count(segment) > 1:
           return True
    return False
    
def encryption_oracle(text):
    prepend = secrets.token_bytes(5+secrets.randbelow(6))
    append = secrets.token_bytes(5+secrets.randbelow(6))
    step1 = prepend + text + append
    
    methods = ('ECB', 'CBC')
    method = methods[secrets.randbelow(2)]

    key = secrets.token_bytes(16)
    if method == 'CBC':
        iv = secrets.token_bytes(16)
        encrypted = encrypt_AES_CBC(key, iv, step1)
    elif method == 'ECB':
        encrypted = encrypt_AES_ECB(key, step1)
        
    return encrypted, method

input = b'0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
for i in range(10):
    encrypted, method = encryption_oracle(input)

    if is_ECB(encrypted):
        detected_method = 'ECB'
    else:
        detected_method = 'CBC'
        
    print('method used: {}\nmethod detected: {}\n'.format(method, detected_method))
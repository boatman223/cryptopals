import base64
from Crypto.Cipher import AES

with open('7.txt', 'r') as input_file:
    input_text = input_file.read()
    
ciphertext = base64.b64decode(input_text)
key = b'YELLOW SUBMARINE'

def decrypt_AES_ECB(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext
    
result = decrypt_AES_ECB(key, ciphertext)
print(result.decode())
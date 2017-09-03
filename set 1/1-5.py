import binascii
import sys

input = 'Burning \'em, if you ain\'t quick and nimble I go crazy when I hear a cymbal'
key = 'ICE'

def encrypt_repeating_key(input, key):
    result = ''
    for index, letter in enumerate(input):
        key_letter = key[(index+3) % (len(key))]
        result_letter = ord(key_letter) ^ ord(letter)
        binary_letter = result_letter.to_bytes(1, sys.byteorder)
        hex_letter = binascii.hexlify(binary_letter)
        result += hex_letter.decode('utf-8')
        
    return result
            
result = encrypt_repeating_key(input, key)
print(result)
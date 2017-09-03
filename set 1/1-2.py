import binascii
import sys

input = '1c0111001f010100061a024b53535009181c'
key = '686974207468652062756c6c277320657965'

def xor_hex_values(input, key):
    input = binascii.unhexlify(input)
    key = binascii.unhexlify(key)
    int_result = int.from_bytes(input, sys.byteorder) ^ int.from_bytes(key, sys.byteorder)
    binary_result = int_result.to_bytes(len(input), sys.byteorder)
    result = binascii.hexlify(binary_result)
    return result
    
result = xor_hex_values(input, key)
print(result)

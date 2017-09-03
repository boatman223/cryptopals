input = b'YELLOW SUBMARINE'

def pad_input(input, length, pad_char=b'\x04'):
    if len(input) >= length:
        return input
    pad_length = length - len(input)
    padded = bytearray(input) + (pad_char * pad_length)
    return bytes(padded)
    
result = pad_input(input, 20)
print(result)
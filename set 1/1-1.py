import binascii

convert_me = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

def hex_to_base64(hex_string):
    binary_date = binascii.unhexlify(hex_string)
    base64_string = binascii.b2a_base64(binary_date).strip(b'\n')
    return base64_string
    
base64_string = hex_to_base64(convert_me)
print(base64_string)
import pprint
import base64
import string
import sys

def hamming_distance(bytes1, bytes2):
    binary_string1 = ''
    for byte in bytes1:
        binary_string1 += '{0:b}'.format(byte).zfill(8)
        
    binary_string2 = ''
    for byte in bytes2:
        binary_string2 += '{0:b}'.format(byte).zfill(8)

    distance = 0
    for index, bit in enumerate(binary_string1):
        if bit != binary_string2[index]:
            distance += 1

    return distance
   
def decrypt_xor(input):
    possible_results = {}
    
    for letter in string.printable:
        key = ''.join(letter*len(input))
        binary_key = key.encode()
        int_result = int.from_bytes(input, sys.byteorder) ^ int.from_bytes(binary_key, sys.byteorder)
        binary_result = int_result.to_bytes(len(input), sys.byteorder)
        possible_results[letter] = binary_result.decode('utf-8', errors='ignore')
        
    scored_results = score_input(possible_results)
    sorted_results = []
    
    for letter in sorted(scored_results, key=scored_results.get, reverse=True):
        sorted_results.append(letter)
        
    highest_score = sorted_results[0]
    
    return highest_score
    
def score_input(input):
    scored_results = {}
    
    for key, value in input.items():
        score = 0
        for letter in value:
            if letter in string.printable:
                if letter in string.ascii_letters: score += english_freq.index(letter.lower())
            else:
                score -= 50
        scored_results[key] = score

    return scored_results
    
def decrypt_repeating_key(input, key):
    result = ''
    for index, letter in enumerate(input):
        key_letter = key[(index+len(key)) % (len(key))]
        result_letter = ord(key_letter) ^ letter
        binary_letter = result_letter.to_bytes(1, sys.byteorder)
        result += binary_letter.decode('utf-8')
        
    return result
    
def calculate_keysize(input): 
    keysizes = {}
    for i in range(2, 41):
        broken = [input[x:x+i] for x in range(0, len(input), i)][:-1]
        distance = [(hamming_distance(broken[0], block) / i) for block in broken[1:]]
        avg_distance = (sum(distance)) / len(distance)
        keysizes[i] = avg_distance
        
    keysize = min(keysizes.items(), key=lambda x: x[1])[0]
    
    return keysize

def transpose_blocks(input, keysize):
    broken = [input[x:x+keysize] for x in range(0, len(input), keysize)][:-1]
    transposed = [bytearray(b'') for k in range(keysize)]
    for block in broken:
        for j in range(keysize):
            transposed[j].append(block[j])
    
    return transposed
    
def determine_key(transposed):
    key = ''
    for block in transposed:
        key += decrypt_xor(block)
        
    return key
    
english_freq = 'etaoinshrdlcumwfgypbvkjxqz'
english_freq = list(english_freq)[::-1]

with open('6.txt', 'r') as input_file:
    input_text = input_file.read()
    
decrypt_me = base64.b64decode(input_text)

    
keysize = calculate_keysize(decrypt_me)
transposed = transpose_blocks(decrypt_me, keysize)
key = determine_key(transposed)
result = decrypt_repeating_key(decrypt_me, key)

print('base64:\n{}'.format(input_text))
print('keysize: {}\n'.format(keysize))
print('key: {}\n'.format(key))
print('decrypted message:\n{}'.format(result))
    

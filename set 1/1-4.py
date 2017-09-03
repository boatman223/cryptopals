import binascii
import sys
import string
import pprint

english_freq = 'etaoinshrdlcumwfgypbvkjxqz'
english_freq = list(english_freq)[::-1]

with open('4.txt', 'r') as input_file:
    dirty_input_text = input_file.readlines()
    
input_text = []
for entry in dirty_input_text:
    input_text.append(entry.strip('\n'))

def decrypt_xor(input):
    possible_results = {}
    input_length = len(input)/2
    binary_input = binascii.unhexlify(input)
    
    for letter in string.printable:
        key = ''.join(letter*int(input_length))
        binary_key = key.encode()
        int_result = int.from_bytes(binary_input, sys.byteorder) ^ int.from_bytes(binary_key, sys.byteorder)
        binary_result = int_result.to_bytes(len(binary_input), sys.byteorder)
        possible_results[letter] = binary_result.decode('utf-8', errors='ignore')
        
    scored_results = score_input(possible_results)
    sorted_results = []
    
    for letter in sorted(scored_results, key=scored_results.get, reverse=True):
        sorted_results.append(letter)
        
    highest_score = sorted_results[0]
    
    return {(possible_results[highest_score], highest_score, input):scored_results[highest_score]}
    
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
    
results = {}
for entry in input_text:
    results.update(decrypt_xor(entry))

for key in sorted(results, key=results.get, reverse=True):
    print('input text: {}\ncipher key: {}\ndecrypted text: {}'.format(key[2], key[1], key[0]))
    break
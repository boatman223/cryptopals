import binascii
import sys
import string
import pprint

english_freq = 'etaoinshrdlcumwfgypbvkjxqz'
english_freq = list(english_freq)[::-1]

input = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

def decrypt_xor(input):
    possible_results = {}
    input_length = len(input)/2
    binary_input = binascii.unhexlify(input)
    
    for letter in string.ascii_letters:
        key = ''.join(letter*int(input_length))
        binary_key = key.encode()
        int_result = int.from_bytes(binary_input, sys.byteorder) ^ int.from_bytes(binary_key, sys.byteorder)
        binary_result = int_result.to_bytes(len(binary_input), sys.byteorder)
        possible_results[letter] = binary_result.decode('utf-8')
        
    scored_results = score_input(possible_results)
    sorted_results = []
    
    for letter in sorted(scored_results, key=scored_results.get, reverse=True):
        sorted_results.append(letter)
        
    return sorted_results[0], possible_results
    
def score_input(input):
    scored_results = {}
    
    for key, value in input.items():
        score = 0
        for letter in value.replace(' ', ''):
            if letter in string.ascii_letters:
                score += english_freq.index(letter.lower())
            else:
                score -= 10           
        scored_results[key] = score

    return scored_results

result, result_dict = decrypt_xor(input)
print('cipher key: {}\nresult: {}'.format(result, result_dict[result]))
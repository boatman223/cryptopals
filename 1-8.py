from Crypto.Cipher import AES
import codecs
import pprint

with open('8.txt', 'r') as input_file:
    input_text = input_file.readlines()
    
ciphertexts = []
for entry in input_text:
    entry = entry.strip('\n')
    ciphertexts.append(codecs.decode(entry, 'hex'))
    
result = ''
for entry in ciphertexts:
    broken = [entry[i:i+16] for i in range(0, len(entry), 16)]
    for segment in broken:
        if broken.count(segment) > 1:
           result = entry
           break
    if result: break
    
pprint.pprint(result)

            
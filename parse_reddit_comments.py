import re
import json

fname = 'comments.json'
write_to = 'words_dict.json'

stop_words = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 
    'for', 'if', 'in', 'is', 'it', 'of', 'on', 'or', 'so', 
    'that', 'the', 'to', 'was', 'with', 'you', 'like', 's', 
    't', 'm', 're', 've', 'd', 'll', 'don', 'won', 'i', 
    'me', 'my', 'he', 'she', 'his', 'her', 'they', 'them', 'their',
    'this', 'not', 'it', 'its', 'all', 'just', 'been', 'being', 'get',
    'https'
}

words = dict()

with open(fname, 'r', encoding='utf-8') as f:
    for line in f:
        word_ls = re.findall(r'[a-z]+', line)
        for w in word_ls:
            valid = w.lower() not in stop_words and len(w) > 2
            init = w.lower() not in words
            if valid:
                if init:
                    words[w.lower()] = 1
                words[w.lower()] += 1

print(words)
print(len(words))

with open(write_to, 'w', encoding='utf-8') as f:
    json.dump(words, f, indent = 4)

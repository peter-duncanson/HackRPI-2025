fname = 'words_dict.json'
write_to = 'filtered_words.json'

filtered_words = dict()

with open(fname, 'r', encoding='utf-8') as f:
    for line in f:
        line.values()
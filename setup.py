def filter_words(in_file_name, out_file_name):
    words_to_keep = []
    with open(in_file_name, 'r') as in_file:
        for word in in_file:
            word = word.strip()
            if len(word) == 5:
                words_to_keep.append(word)
    
    with open(out_file_name, 'w') as out_file:
        out_file.writelines(words_to_keep)


with open('words.txt', 'r') as f:
    words = [word.strip() for word in f.readlines()]


if __name__ == '__main__':
    filter_words('words_all.txt', 'words.txt')
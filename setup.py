
with open('words.txt', 'r') as f:
    words = [word.strip() for word in f.readlines()]
num_words = len(words)


N = 5
alpha = string.ascii_lowercase


def filter_words(in_file_name, out_file_name):
    words_to_keep = []
    with open(in_file_name, 'r') as in_file:
        for word in in_file:
            if len(word) == 6:
                words_to_keep.append(word)
    with open(out_file_name, 'w') as out_file:
        print(len(words_to_keep))
        out_file.writelines(words_to_keep)


if __name__ == '__main__':
    filter_words('words_all.txt', 'words.txt')
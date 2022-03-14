from collections import Counter


def get_len(key):
    return len(key[0])


def median_words_count(size_of_sent):
    size_of_sent.sort()
    counts_len = len(size_of_sent)
    if counts_len % 2 == 0:
        return (size_of_sent[counts_len // 2 - 1]
                + size_of_sent[counts_len // 2]) / 2
    return size_of_sent[counts_len // 2]


def average_words_count(my_dict, count_of_sent):
    return float('{:.2}'.format(len(my_dict.keys()) / count_of_sent))


def clear_text(text_from_file):
    text_from_file = text_from_file.replace('?', '.')
    text_from_file = text_from_file.replace('!', '.')
    return text_from_file


def sentence_size(text_from_file):
    size_of_sent = []
    sentence = text_from_file.split(".")
    for i in range(0, len(sentence) - 2):
        size_of_sent.append(len(sentence[i].split(" ")) - 1)
    return size_of_sent


def get_text():
    file = open("testText", "r")
    text_from_file = file.read()
    text_from_file = clear_text(text_from_file)
    return text_from_file


def get_dict(text_from_file):
    word_list = []
    for word in text_from_file.split():
        clear_word = ""
        for letter in word:
            if letter.isalpha():
                clear_word += letter.lower()
        word_list.append(clear_word)
    my_dict = dict(Counter(word_list))
    return my_dict


def print_counts(my_dict, size_of_sent):
    median_count = median_words_count(size_of_sent)
    print('-' * 14)
    print("average word count ---->", median_count)
    average_count = average_words_count(my_dict, len(size_of_sent))
    print("median word count  ---->", average_count)
    print('-' * 14)
    for key, value in my_dict.items():
        print("{0}: {1}".format(key, value))
    print('-' * 14)


def sort_list(my_dict):
    items_my_dict = list(my_dict.items())
    items_my_dict.sort(key=get_len)
    res = {ele[0]: ele[1] for ele in items_my_dict}
    to_print_list = list(res.keys())
    return to_print_list


def start_analyze(n_symbol, m_top):
    if not n_symbol:
        n_symbol = 10
    if not m_top:
        m_top = 4
    text_from_file = get_text()
    my_dict = get_dict(text_from_file)
    size_of_sent = sentence_size(text_from_file)
    print_counts(my_dict, size_of_sent)
    to_print_list = sort_list(my_dict)

    for i in range(len(to_print_list), 0, -1):
        if int(m_top) > 0 and len(to_print_list[i - 1]) >= int(n_symbol):
            for j in range(0, int(n_symbol)):
                print(to_print_list[i - 1][j], end="")
            print("")
            m_top -= 1
    print('-' * 14)


def start_program():
    n_symbol = int(input("n-grams count: "))
    m_top = int(input("top-m count: "))
    start_analyze(n_symbol, m_top)
    return 0


if __name__ == "__main__":
    start_program()

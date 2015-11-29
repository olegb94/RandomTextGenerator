import pickle
import sys
import random
from collections import Counter
from collections import defaultdict


tab = ' ' * 3


def get_random_from_counter(counter):
    probability = random.random()
    total = sum(counter.values())
    for key in counter:
        if probability > counter[key] / total:
            probability -= counter[key] / total
        else:
            return key
    return ''


def get_first_words(first_words_dist):
    first_words = '.'
    while '.' in first_words:
        first_words = get_random_from_counter(first_words_dist)
    return first_words


def get_third_word(previous, third_words_dist):
    last_two = tuple(previous[-2:])
    return get_random_from_counter(third_words_dist[last_two])


def check_sentence_end(previous):
    if previous[-1] != '.':
        return False
    previous.pop()
    previous[-1] += '.'
    if random.random() < 0.1:
        previous[-1] += '\n' + tab
    return True


def form_result(words):
    if words[-1][-1] != '.':
        words[-1] += '.'
    return ' '.join(words)


def generate(number_of_words, first_words_dist, third_words_dist):
    state = 'first'
    result = [tab]
    for i in range(number_of_words):
        if state == 'first':
            state = 'second'

        elif state == 'second':
            words = get_first_words(first_words_dist)
            result.append(words[0])
            result.append(words[1])
            state = 'third'

        elif state == 'third':
            result.append(get_third_word(result, third_words_dist))

        if state == 'third' and check_sentence_end(result):
            state = 'first'

    return form_result(result)


def main(args):
    if len(args) != 4:
        print("Usage: learn.py <path to dictionary> <pass to result> <number of words>.")
        return
    dict_filename = args[1]
    output_filename = args[2]
    number_of_words = int(args[3])

    dictionary = open(dict_filename, 'rb')
    first_words_dist, third_words_dist = pickle.load(dictionary)
    dictionary.close()

    with open(output_filename, 'w') as out_file:
        out_file.write(generate(number_of_words, first_words_dist, third_words_dist))


if __name__ == '__main__':
    main(sys.argv)

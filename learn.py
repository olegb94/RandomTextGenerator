import glob
import pickle
import os
import sys
import string
from collections import Counter
from collections import defaultdict


def read_and_clear(path):
    with open(path) as file:
        text = file.read()
    punctuation = string.punctuation
    punctuation += '\n\t”“„'
    translate_dict = dict.fromkeys(map(ord, punctuation), ' ')
    translate_dict[ord('.')] = ' . '
    clear_text = text.translate(translate_dict)
    return clear_text.split(' ')


def read_all_texts(dir):
    list_pathes = glob.glob(os.path.join(dir, '*.txt'))
    list_pathes += glob.glob(os.path.join(dir, '**/*.txt'))
    words = []
    for path in list_pathes:
        if os.path.isdir(path):
            continue
        words += read_and_clear(path)
    return words
    

def learn_new_word(word, state, previous, first_words_dist, third_words_dist):
    if word == '':
        return state
    new_state = state

    if state == 'first':
        if word == '.':
            return state
        new_state = 'second'
        
    elif state == 'second':
        first = previous[-1]
        first_words_dist[(first, word)] += 1
        new_state = 'third'
        
    elif state == 'third':
        last_two = tuple(previous[-2:])
        third_words_dist[last_two][word] += 1

    if word == '.':
        new_state = 'first'

    previous.append(word)
    return new_state


def learn(words):
    first_words_dist = Counter()
    third_words_dist = defaultdict(Counter)
    last_words = []
    state = 'first'
    for word in words:
        state = learn_new_word(word, state, last_words, first_words_dist, third_words_dist)
        if state == 'first':
            last_words = []

    return first_words_dist, third_words_dist


def main(args):
    if len(args) != 3:
        print("Usage: learn.py <path to corpus> <pass to result>.")
        return

    learned_data = learn(read_all_texts(args[1]))

    with open(args[2], 'wb') as out_file:
        pickle.dump(learned_data, out_file)


if __name__ == '__main__':
    main(sys.argv)
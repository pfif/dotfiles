from collections import defaultdict
from copy import deepcopy
from functools import partial
import csv
import json
import webbrowser

PRIORITIES = {"i": 5, "p": 4, "n": 3, "o": 2, "b": 1}
SAVE_FILE = ".english_vocabulary_state"
VOCABULARY_FILE = "vocabulary.txt"
CSV_FILE = "memrise.csv"


def write_state_to_file(
        filename,
        words=None,
        sentences=None):
    if sentences is None:
        sentences = []

    file_ = open(filename, "w")
    state = {
        "words": words,
        "sentences": sentences,
    }
    json.dump(state, file_, indent=4)
    file_.close()


def load_state_from_file(filename):
    try:
        file_ = open(filename, "r")
        state = json.load(file_)
    except FileNotFoundError:
        state = defaultdict(lambda: None)

    words = state["words"]
    sentences = state["sentences"]
    return words, sentences


local_write_state = partial(write_state_to_file, SAVE_FILE)


def load_sentence_list(vocabulary_file):
    vocabulary_file = open(vocabulary_file, "r")
    return vocabulary_file.readlines()


def select_words_from_sentences(write_state, sentences, words=None):
    sentences = deepcopy(sentences)
    if words is None:
        words = []
    else:
        words = deepcopy(words)

    while sentences:
        print("%s sentences remaining..." % len(sentences))
        new_words, sentences = select_words_from_sentence(sentences)
        words.extend(new_words)
        write_state(words, sentences)

    return words


def select_words_from_sentence(sentences):
    sentence = sentences[0]
    words = []

    while True:
        print("Current sentence: %s" % sentence)
        print("(c)omplete sentence or (s)elect word")
        action = input("select your action? ")
        if action == "c":
            break
        elif action == "s":
            words.append(select_word(sentence))

    words = [
        {"sentence": sentence, "word": word}
        for word in words
    ]
    return words, sentences[1:]


def select_word(sentence):
    while True:
        word = input("please input a word : ")
        if word not in sentence:
            print("word not in sentence")
        else:
            return word


# Sort words from most important to least important
def sort_list(write_state, words):
    words_sorted_and_prioritized = deepcopy(words)

    for i, word in enumerate(words_sorted_and_prioritized):
        if "priority" not in word:
            print("\n%s words remaining..." % (len(words) - i))
            word["priority"] = input_word_priority(word)
            write_state(words_sorted_and_prioritized)

    return sort_words_according_to_priority(words_sorted_and_prioritized)


def input_word_priority(word):
    print(word["sentence"])
    print("What is the priority for the word '%s'" % word["word"])
    while True:
        answer = input("(i)ndispensable, im(p)ortant, (n)ice, (o)ptional, (b)oring [(m)erriam-webster] : ")
        if answer in PRIORITIES.keys():
            return PRIORITIES[answer]
        if answer is "m":
            merriam_webster(word["word"])


def merriam_webster(word):
    webbrowser.open("https://www.merriam-webster.com/dictionary/%s" % word)


def vocabulary_com(word):
    webbrowser.open("https://www.vocabulary.com/dictionary/%s" % word)


def google(word):
    webbrowser.open("https://www.google.co.uk/search?q=%s" % word)


def sort_words_according_to_priority(words):
    highest_priority = max(PRIORITIES.values())
    words_sorted = []
    for priority in range(highest_priority, 0, -1):
        words_sorted.extend(
            [word for word in words if word["priority"] == priority]
        )
    return words_sorted


def limit_list(words):
    return words[:50]


def hide_words_from_sentences(write_state, words):
    new_words = list(map(hide_word_from_sentence, words))
    write_state(words=new_words)
    return new_words


def hide_word_from_sentence(word):
    word = deepcopy(word)
    word_string = word["word"]
    if "__" not in word["sentence"]:
        while word_string not in word["sentence"]:
            print(word["sentence"])
            word_string = input("%s is not in this sentence. What should be replace instead ? " % word_string)
        word["sentence"] = word["sentence"].replace(word_string, "__")
    return word


def input_definition_for_words(write_state, words, input_definition_for_word):
    words = deepcopy(words)
    for i, word in enumerate(words):
        if "definition" not in word:
            print("%s words remaining..." % (len(words) - i))
            word["word"], word["definition"], extra_fields = input_definition_for_word(word)
            word.update(extra_fields)
            write_state(words)
    return words


def input_definition_for_word_english(word):
    word_string = word["word"]
    print(word["sentence"])
    print(word["word"])
    definitions = []
    while True:
        answer = input("(i)nput definition, (c)hange word, (m)erriam-webster, (v)ocabulary.com, (g)oogle, (d)one : ")
        if answer == "i":
            definitions.append(input("definition: "))
        elif answer == "c":
            word_string = input("word: ")
        elif answer == "m":
            merriam_webster(word_string)
        elif answer == "v":
            vocabulary_com(word_string)
        elif answer == "g":
            google(word_string)
        elif answer == "d":
            definition_string = make_definition_string(definitions)
            print("Definitions : %s" % definition_string)
            print("\n")
            return word_string, definition_string


def make_definition_string(definitions):
    if len(definitions) > 1:
        return " - ".join([
            "%s. %s" % (i + 1, definition) for i, definition in enumerate(definitions)
        ])
    else:
        return definitions[0]


def export_words_to_csv(words, csv_filename, extra_fields=None):
    if extra_fields is None:
        extra_fields = []
    fields = ["word", "definition", "sentence"]
    fields.update(fields)

    print("Exporting to CSV...")
    with open(csv_filename, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fields, extrasaction="ignore")

        for word in words:
            writer.writerow(word)


def get_word_and_sentence(save_file, vocabulary_file):
    words, sentences = load_state_from_file(save_file)

    if words is None:
        sentences = load_sentence_list(vocabulary_file)

    return words, sentences


words, sentences = get_word_and_sentence(SAVE_FILE, VOCABULARY_FILE)
words = select_words_from_sentences(local_write_state, sentences, words)
words = sort_list(local_write_state, words)
words = limit_list(words)
words = input_definition_for_words(local_write_state, words, input_definition_for_word_english)
words = hide_words_from_sentences(local_write_state, words)
export_words_to_csv(words, CSV_FILE)

from collections import defaultdict
from copy import deepcopy
import csv
import json
import webbrowser

PRIORITIES = {"i": 5, "p": 4, "n": 3, "o": 2, "b": 1}


def write_state_to_file(
        words=None,
        sentences=None):
    if sentences is None:
        sentences = []

    file_ = open(".vocabulary_state", "w")
    state = {
        "words": words,
        "sentences": sentences,
    }
    json.dump(state, file_, indent=4)
    file_.close()


def load_state_from_file():
    try:
        file_ = open(".vocabulary_state", "r")
        state = json.load(file_)
    except FileNotFoundError:
        state = defaultdict(lambda: None)

    words = state["words"]
    sentences = state["sentences"]
    return words, sentences


def load_sentence_list():
    vocabulary_file = open("vocabulary.txt", "r")
    return vocabulary_file.readlines()


def select_words_from_sentences(sentences, words=None):
    sentences = deepcopy(sentences)
    if words is None:
        words = []
    else:
        words = deepcopy(words)

    while sentences:
        print("%s sentences remaining..." % len(sentences))
        new_words, sentences = select_words_from_sentence(sentences)
        words.extend(new_words)
        write_state_to_file(words, sentences)

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
def sort_list(words):
    words_sorted_and_prioritized = deepcopy(words)

    for i, word in enumerate(words_sorted_and_prioritized):
        if "priority" not in word:
            print("\n%s words remaining..." % (len(words) - i))
            word["priority"] = input_word_priority(word)
            write_state_to_file(words_sorted_and_prioritized)

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


def hide_words_from_sentences(words):
    new_words = list(map(hide_word_from_sentence, words))
    write_state_to_file(words=new_words)
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


def input_definition_for_words(words):
    words = deepcopy(words)
    for i, word in enumerate(words):
        if "definition" not in word:
            print("%s words remaining..." % (len(words) - i))
            word["word"], word["definition"] = input_definition_for_word(word)
            write_state_to_file(words)
    return words


def input_definition_for_word(word):
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
            if len(definitions) > 1:
                definition_string = " - ".join([
                    "%s. %s" % (i + 1, definition) for i, definition in enumerate(definitions)
                ])
            else:
                definition_string = definitions[0]
            print("Definitions : %s" % definition_string)
            print("\n")
            return word_string, definition_string


def export_words_to_csv(words):
    print("Exporting to CSV...")
    with open("memrise.csv", "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, ["word", "definition", "sentence"], extrasaction="ignore")

        for word in words:
            writer.writerow(word)


words, sentences = load_state_from_file()

if words is None:
    sentences = load_sentence_list()

words = select_words_from_sentences(sentences, words)
words = sort_list(words)
words = limit_list(words)
words = input_definition_for_words(words)
words = hide_words_from_sentences(words)
export_words_to_csv(words)

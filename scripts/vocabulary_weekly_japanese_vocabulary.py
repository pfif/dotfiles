from functools import partial
import webbrowser

from vocabulary_weekly import (
    get_word_and_sentence,
    write_state_to_file,
    select_words_from_sentences,
    input_definition_for_words,
    hide_words_from_sentences,
    export_words_to_csv,
    make_definition_string
)


def jisho(word):
    webbrowser.open("http://jisho.org/search/%s" % word)


SAVE_FILE = ".japanese_vocabulary_state"
VOCABULARY_FILE = "vocabulary_japanese.txt"

local_write_state = partial(write_state_to_file, SAVE_FILE)


def input_definition_for_word_japanese(word):
    word_string = word["word"]
    print(word["sentence"])
    print(word["word"])

    definitions = []
    furigana = None

    while True:
        answer = input("(i)nput definition, input (f)urigana, (c)hange word, (j)isho, (d)one : ")
        if answer == "i":
            definitions.append(input("definition: "))
        elif answer == "f":
            furigana = input("furigana: ")
        elif answer == "c":
            word_string = input("word: ")
        elif answer == "j":
            jisho(word_string)
        elif answer == "d":
            if definitions and furigana:
                definition_string = make_definition_string(definitions)
                print("Definitions : %s" % definition_string)
                print("Furigana : %s" % furigana)
                print("\n")
                return word_string, definition_string
            else:
                print("Either the definitions or the furigana are missing")


words, sentences = get_word_and_sentence(SAVE_FILE, VOCABULARY_FILE)
words = select_words_from_sentences(local_write_state, sentences, words)
words = input_definition_for_words(local_write_state, words, input_definition_for_word_japanese)
words = hide_words_from_sentences(local_write_state, words)
export_words_to_csv(words)

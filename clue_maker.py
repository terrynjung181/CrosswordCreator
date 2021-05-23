import json
import requests
import random
from layout_solver.word_slot import WordSlot

def definition(word):
    dict_json = open('theme_classifier/dictionary.json')
    data = json.load(dict_json)
    word_def = data[word]
    dict_json.close()
    return word_def

def remove_num(word_def):
    numless_def = ""
    start_ind = 0
    i = 0
    while i < len(word_def):
        if word_def[i:i+2].isdigit():
            numless_def += word_def[start_ind:i]+"; "
            start_ind = i+4
            i += 2
        elif word_def[i:i+1].isdigit():
            numless_def += word_def[start_ind:i]+"; "
            start_ind = i+3
            i += 1
        elif i == len(word_def)-1:
            numless_def += word_def[start_ind:i+1]
            i += 1
        else:
            i += 1
    return numless_def


def split_def(def_string):
    def_list = def_string.split("; ")
    return def_list

def clean_list(def_list):
    i = 0
    while i < len(def_list):
        if '.' in def_list[i]:
            del def_list[i]
        elif def_list[i] == '':
            del def_list[i]
        else:
            i += 1
    return def_list

def replace_syn(def_string, word):
    if word in def_string:
        synonym_url = "https://api.datamuse.com/words?rel_syn=" + word + "&md"
        synonym_data = requests.get(synonym_url)
        synonym_json = json.loads(synonym_data.text)
        if len(synonym_json) == 0: 
            return None
        else:
            synonym_list = []
            counter = 0
            while (counter<len(synonym_json)):
                synonym_list.append(synonym_json[counter]["word"])
                counter += 1

            rand_syn = random.randint(0, counter-1)
            syn = synonym_list[rand_syn]
        def_string = def_string.replace(word, syn)

    return def_string


def find_clue(word):
    def_list = definition(word)
    def_list = remove_num(def_list)
    def_list = split_def(def_list)
    def_list = clean_list(def_list)
    word_clue = None
    while word_clue is None:
        temp_clue = def_list[random.randint(0, len(def_list)-1)]
        word_clue = replace_syn(temp_clue, word)
    return word_clue

def generate_clues(word_slots):
    for i in range(len(word_slots)):
        word = word_slots[i].get_best_word()
        clue = find_clue(word)
        word_slots[i].set_clue(clue)


# # trying out the simpler version first: 
# # maps to 20th synonym, 
# # or the last one if <20

# def generate_clues(word_slots):
#     """
#     Finds a clue for the inputted word.
#     word:       [word] - a String, the word

#     Output:     [clue] - a String, the clue for the inputted word
#     """

#     # we pull the list of synonyms for the inputted word
#     for i in range(len(word_slots)):
#         word = word_slots[i].get_best_word()
#         synonym_url = "https://api.datamuse.com/words?rel_syn=" + word + "&md=d"
#         synonym_data = requests.get(synonym_url)
#         synonym_json = json.loads(synonym_data.text)

#         if len(synonym_json) == 0: 
#             word_slots[i].set_clue("NO CLUE")
        
#         else:

#             synonym_list = []
#             counter = 0
#             # clean up the data and make it into a list of synonyms
#             while (counter<len(synonym_json)):
#                 synonym_list.append(synonym_json[counter]["defs"][0])
#                 counter += 1

#             rand_syn = random.randint(0, counter-1)
#             clue = synonym_list[rand_syn]

#             # Separate clue from PoS
#             clue = clue.split('\t', 1)[1].strip()
#             clue_mult = clue.split(';')
#             rand_clue_mult = random.randint(0, len(clue_mult)-1)
#             clue = clue_mult[rand_clue_mult].strip()
            
#             word_slots[i].set_clue(clue)
        
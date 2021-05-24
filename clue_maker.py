import json
import requests
import random
from layout_solver.word_slot import WordSlot

# trying out the simpler version first: 
# maps to 20th synonym, 
# or the last one if <20

def generate_clues_with_api(word):
    """
    Finds a clue for the inputted word.
    word:       [word] - a String, the word

    Output:     [clue] - a String, the clue for the inputted word
    """

    # we pull the list of synonyms for the inputted word
    synonym_url = "https://api.datamuse.com/words?rel_syn=" + word + "&md=d"
    synonym_data = requests.get(synonym_url)
    synonym_json = json.loads(synonym_data.text)

    if len(synonym_json) == 0: 
        return "NO CLUE"        
    else:
        synonym_list = []
        counter = 0
        # clean up the data and make it into a list of synonyms
        while (counter<len(synonym_json)):
            synonym_list.append(synonym_json[counter]["defs"][0])
            counter += 1

        rand_syn = random.randint(0, counter-1)
        clue = synonym_list[rand_syn]

        # Separate clue from PoS
        clue = clue.split('\t', 1)[1].strip()
        clue_mult = clue.split(';')
        rand_clue_mult = random.randint(0, len(clue_mult)-1)
        return clue_mult[rand_clue_mult].strip()


def definition(word):
    dict_json = open('theme_classifier/dictionary.json')
    data = json.load(dict_json)
    word_def = data[word]
    dict_json.close()
    return word_def

def insert_semicolon(word_def):
    semicol_def = ""
    start_ind = 0
    i = 0
    while i < len(word_def):
        if word_def[i:i+2].isdigit() and i != len(word_def)-2:
            semicol_def += word_def[start_ind:i]+"; "
            start_ind = i+4
            i += 2
        elif word_def[i:i+1].isdigit() and i != len(word_def)-1:
            semicol_def += word_def[start_ind:i]+"; "
            start_ind = i+3
            i += 1
        elif word_def[i:i+2]=="--" and i != len(word_def)-2:
            semicol_def += word_def[start_ind:i]+"; "
            start_ind = i+4
            i += 2
        elif i == len(word_def)-1:
            semicol_def += word_def[start_ind:i+1]
            i += 1
        else:
            i += 1
    return semicol_def


def split_def(def_string):
    def_list = def_string.split("; ")
    return def_list

def clean_list(def_list):
    i = 0
    while i < len(def_list):
        def_word = def_list[i]
        if ". See" in def_word:
            see_ind = def_word.find(". See")
            def_list[i] = def_word[:see_ind]
            i += 1
        elif "See" in def_word:
            see_ind = def_word.find("See")
            def_list[i] = def_word[see_ind+3:]
            i += 1
        elif ". [" in def_word:
            brac_ind = def_word.find(". [")
            def_list[i] = def_word[:brac_ind]
            i += 1
        elif "\n" in def_word:
            n_ind = def_word.find("\n")
            def_list[i] = def_word[:n_ind]
            i += 1           
        elif '.' in def_word and def_word[-1]!= '.' and len(def_list) != 1:
            del def_list[i]
        elif def_word == '':
            del def_list[i]
        elif def_word[0:2]=='--':
            def_list[i] = def_word[2:]
            i += 1
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
    def_list = insert_semicolon(def_list)
    def_list = split_def(def_list)
    def_list = clean_list(def_list)
    word_clue = None
    if len(def_list) == 0:
        return generate_clues_with_api(word)
    while word_clue is None:
        temp_clue = def_list[random.randint(0, len(def_list)-1)]
        word_clue = replace_syn(temp_clue, word)
    return word_clue.capitalize()


def generate_clues(word_slots):
    for i in range(len(word_slots)):
        word = word_slots[i].get_best_word()
        clue = find_clue(word)
        word_slots[i].set_clue(clue)

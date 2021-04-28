import analyze_layout
import generate_words
import json
import requests
import random

# trying out the simpler version first: 
# maps to 20th synonym, 
# or the last one if <20

def generate_clue_v1(word):
    """
    Finds a clue for the inputted word.
    word:       [word] - a String, the word

    Output:     [clue] - a String, the clue for the inputted word
    """

    # we pull the list of synonyms for the inputted word
    synonym_url = "https://api.datamuse.com/words?rel_syn=" + word
    synonym_data = requests.get(synonym_url)
    synonym_json = json.loads(synonym_data.text)
    # print(synonym_json)

    if len(synonym_json) == 0: raise NameError('WORD HAS 0 SYNONYMS, CHOOSE NEW WORD')

    synonym_list = []
    counter = 0
    # clean up the data and make it into a list of synonyms
    while (counter<len(synonym_json)):
        synonym_list.append(synonym_json[counter]["word"])
        counter += 1

    # return the 20th synonym or the last one if <20
    if len(synonym_list)>=20: 
        print(synonym_list[19])
        return synonym_list[19]
    else:
        print(synonym_list[-1]) 
        return synonym_list[-1]

generate_clue_v1("happy")
generate_clue_v1("excavate")
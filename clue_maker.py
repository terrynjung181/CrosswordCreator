import analyze_layout
import generate_words
import json
import requests
import random

# trying out the simpler version first: 
# maps to 20th synonym, 
# or the last one if <20

def generate_clue(word):
    """
    Finds a clue for the inputted word.
    word:       [word] - a String, the word

    Output:     [clue] - a String, the clue for the inputted word
    """

    # we pull the list of synonyms for the inputted word
    synonym_url = "https://api.datamuse.com/words?rel_syn=" + word + "&md=d"
    synonym_data = requests.get(synonym_url)
    synonym_json = json.loads(synonym_data.text)

    if len(synonym_json) == 0: raise NameError('WORD HAS 0 SYNONYMS, CHOOSE NEW WORD')

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
    clue = clue_mult[rand_clue_mult].strip()
    
    return clue

generate_clue("happy")
generate_clue("excavate")
import json
import requests
import random
from word_slot import WordSlot


def create_crossword(word_slots, layout_cols, layout_rows):
    """
    Given an ordered dictionary of WordSlot objects, the function will return
    a filled out layout with words from DataMuse.

    Input:  [word_slots] - Dictionary of {id: WordSlot} pairs that need to be
                        defined/filled out
            [layout_cols] - Integer for number of columns in given layout
            [layout_rows] - Integer for number of rows in given layout

    Ouput:  [filled_layout] - 2D matrix with slots defined by word_slots filled
                            with legitimate words
    """
    filled_layout = [["?"] * layout_cols for _ in range(layout_rows)]
    for key in word_slots:
        start_row, start_col = word_slots[key].get_start()
        word_len = word_slots[key].get_length()
        direction = word_slots[key].get_direction()
        row, col = start_row, start_col
        partial_str = ""
        for i in range(word_len):
            partial_str += filled_layout[row][col]
            if direction == "ACROSS":
                col += 1
            else:
                row += 1
        
        word_url = "https://api.datamuse.com/words?sp=" + partial_str + "&md=d"
        word_data = requests.get(word_url)
        word_json = json.loads(word_data.text)

        # JSON shows either no results or word without definition of requested
        # word is not a real word
        if len(word_json) == 0:
            print(partial_str)
            print("NO RESULT")
            exit(0)
        rand_word = word_json[random.randint(0, len(word_json)-1)]
        if "defs" not in rand_word:
            print(partial_str)
            print("NO DEF")
            exit(0)
            
        word_slots[key].set_word(rand_word["word"])
        word_slots[key].set_definition(rand_word["defs"])

        row = start_row
        col = start_col
        for i in range(len(rand_word["word"])):
            filled_layout[row][col] = rand_word["word"][i]
            if direction == "ACROSS":
                col += 1
            else:
                row += 1
        
    return filled_layout

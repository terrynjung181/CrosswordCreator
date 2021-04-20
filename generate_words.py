import json
import requests
import random
from word_slot import WordSlot

def write_word(layout, word_obj):
    """
    Writes a chosen word to our current crossword layout
    Input:      [layout] - the 2D matrix containing the current crossword layout
                [word_obj] - The WordSlot object whose chosen word will be written

    """
    # Get word to write, word length, and direction from word_obj
    word_to_write = word_obj.get_words()[-1] #Chosen word is always last word
    start_row, start_col = word_obj.get_start()
    word_len = word_obj.get_length()
    direction = word_obj.get_direction()
    row = start_row
    col = start_col
    # Iterate over layout and write each character
    for j in range(len(word_to_write["word"])):
        layout[row][col] = word_to_write["word"][j]
        if direction == "ACROSS":
            col += 1
        else:
            row += 1

def erase_word(layout, word_id, word_slots):
    """
    Selectively erases parts of a word from the crossword layout when bactracking.
    Input:      [layout] - the 2D matrix containing the current crossword layout
                [word_id] - the index of the WordSlot object in question from the WordSlot array
                [word_slots] - the WordSlot array
    """
    # Get start location, length, direction of word to remove
    word_obj = word_slots[word_id]
    start_row, start_col = word_obj.get_start()
    word_len = word_obj.get_length()
    direction = word_obj.get_direction()
    row = start_row
    col = start_col
    for j in range(word_len):
        # When removing a word, we can only remove the characters that aren't in overlap
        # with other currently existing words in the layout (otherwise we are mutilating those words).
        # At a particular (row, col), we first make sure that location doesn't have overlap with
        # any other word that is already in the layout.
        erase = True
        for o_id, o_row, o_col in word_obj.get_overlap():
            if o_id < word_id and o_row == row and o_col == col:
                erase = False
                break
        if erase:
            layout[row][col] = "?"
        if direction == "ACROSS":
            col += 1
        else:
            row += 1


def create_crossword(word_slots, layout_cols, layout_rows):
    """
    Given an ordered dictionary of WordSlot objects, the function will return
    a filled out layout with words from DataMuse.

    Input:  [word_slots] - List of WordSlot objects that need to be
                        defined/filled out
            [layout_cols] - Integer for number of columns in given layout
            [layout_rows] - Integer for number of rows in given layout

    Ouput:  [filled_layout] - 2D matrix with slots defined by word_slots filled
                            with legitimate words
    """
    seen_words = set() # This ensures that no word is written on the crossword twice
    # (this only keeps track of the words that are currently IN USE in the crossword)
    filled_layout = [["?"] * layout_cols for _ in range(layout_rows)]
    i = 0
    # We iterate through the WordSlot array and fill every WordSlot object 
    # with a set of legitimate words that fit all constraints.
    while i < len(word_slots):
        restart = False
        # Get info on current WordSlot
        start_row, start_col = word_slots[i].get_start()
        word_len = word_slots[i].get_length()
        direction = word_slots[i].get_direction()
        row, col = start_row, start_col
        
        # If words is None, we need to query the dictionary to get a set of words
        if word_slots[i].get_words() is None:
            # Read the current layout to get set of characters that already exist
            # where our word has to be -- this defines the character constraints our
            # words must have at this location
            partial_str = ""
            for j in range(word_len):
                partial_str += filled_layout[row][col]
                if direction == "ACROSS":
                    col += 1
                else:
                    row += 1

            # Now, we query dictionary based on the character constraints defined above
            word_url = "https://api.datamuse.com/words?sp=" + partial_str + "&md=d"
            word_data = requests.get(word_url)
            word_json = json.loads(word_data.text)
            j = 0
            # The DataMuse API returns a list of python dictionaries; each dictionary is a single word,
            # along with all of its definitions. Unfortunately, some words have no definitions, so
            # we simply remove them. Additionally, we remove all words that are already on the crossword layout
            while j < len(word_json):
                if "defs" not in word_json[j] or word_json[j]["word"] in seen_words:
                    del word_json[j]
                else:
                    j += 1
            # Our list of word dictionaries at this point will be ~80 words; we sample at most 20 of them 
            # to store in our word list for the WordSlot object (for speed)
            final_list = random.sample(word_json, min(20, len(word_json)))
            word_slots[i].set_words(final_list)
            # This sets a list of at most 20 words that can fit the current crossword at a particular WordSlot

        # Get current words from WordSlot objects
        cur_words = word_slots[i].get_words()

        # If the words is empty (DIFFERENT from None) then there are simply no words that fit the 
        # current character constraints -- we need to go backward and change words
        if cur_words == []:
            # Set the words to be None (so it will be re-initialized later)
            word_slots[i].set_words(None)

            # We go "backwards" by picking a WordSlot that overlaps with the current WordSlot 
            # that also has alternative words to pick. Once this is found, we reset every
            # WordSlot after this overlapped WordSlot.
            word_overlaps = word_slots[i].get_overlap()
            j = len(word_overlaps) - 1
            found_overlap = False
            while j >= 0 and found_overlap == False:
                cur_overlap = word_overlaps[j][0]
                cur_words = word_slots[cur_overlap].get_words()
                if cur_overlap < i and cur_words is not None and len(cur_words) >= 2:
                    for k in range(cur_overlap + 1, i):
                        seen_words.remove(word_slots[k].get_words()[-1]["word"])
                        erase_word(filled_layout, k, word_slots)
                        word_slots[k].set_words(None)
                    i = cur_overlap
                    found_overlap = True
                j -= 1
                
            # If no overlap with alternatives have been found, we just start over from the beginning.
            if found_overlap == False:
                print("No solution found, restarting... \n")
                restart = True
                i = -1
                for j in range(len(word_slots)):
                    word_slots[j].set_words(None)
                seen_words = set()
                filled_layout = [["?"] * layout_cols for _ in range(layout_rows)]
            # The current word in use is always the last word picked, so we pop it off the list
            # and erase that word from both seen_words (not used anymore) and from the crossword layout
            else:
                removed_word = cur_words.pop()
                seen_words.remove(removed_word["word"])
                word_slots[i].set_words(cur_words)
        if restart == False:
            # Pick a word; by convention, we always pick the last word in the wordlist for a WordSlot object,
            # write it to the layout, and add to seen_words
            rand_word = cur_words[-1]
            write_word(filled_layout, word_slots[i])
            seen_words.add(rand_word["word"])
        i += 1
        
    return filled_layout

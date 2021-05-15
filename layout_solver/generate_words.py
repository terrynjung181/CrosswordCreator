import json
import requests
import random
from re import match
from word_slot import WordSlot

def find_next_slot(layout, done_slots, word_slots, seen_words, theme_words):
    """
    Decides next WordSlot to fill in our current layout
    Input:      [layout] - the 2D matrix containing the current crossword layout
                [done_slots] - the list of WordSlot ids that have already been filled
                [seen_words] - the set of words that have already been placed

    Output:     [cur_min_ind] - the WordSlot id to fill in next
                [cur_min] - the number of word possibilities for the WordSlot with id cur_min_ind
    """

    # We always want to fill the most constrained WordSlot next. To do this, we simply 
    # loop over every unfilled WordSlot and see how many words can be placed in each one, with our 
    # current crossword layout. We return the WordSlot with minimum number of words
    cur_min_ind = 0
    cur_min = 1000
    for i in range(len(word_slots)):
        if i not in done_slots:
            num_words = len(fetch_words(word_slots[i], layout, seen_words,theme_words))
            if num_words < cur_min:
                cur_min_ind = i
                cur_min = num_words

    return cur_min_ind, cur_min
    

def write_word(layout, word_obj, word_to_write):
    """
    Writes a chosen word to our current crossword layout
    Input:      [layout] - the 2D matrix containing the current crossword layout
                [word_obj] - The WordSlot object whose chosen word will be written

    """
    # Get word to write, word length, and direction from word_obj
    start_row, start_col = word_obj.get_start()
    word_len = word_obj.get_length()
    direction = word_obj.get_direction()
    row = start_row
    col = start_col
    # Iterate over layout and write each character
    for j in range(len(word_to_write)):
        layout[row][col] = word_to_write[j]
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

def fetch_words(wordslot, layout, seen_words, theme_dict):
    """
    Fetch all words possible for a particular WordSlot object in the current crossword layout.
    Input:      [wordslot] - the WordSlot object to fill words for
                [layout] - the 2D matrix containing the current crossword layout
                [seen_words] - the set of words that have already been placed    

    Output:     [final_list] - A 2D list describing the set of words that can fit this WordSlot.
                               Each entry is in the form [word, score], where word is a python dictionary
                               describing the actual word and its definitions, and score is the current 
                               numerical score of that word (all scores are set to 0, 
                               they will be populated later).
    """

    # First, we gather relevant information on the current WordSlot and pick up its partial string
    # in the curren layout
    start_row, start_col = wordslot.get_start()
    word_len = wordslot.get_length()
    direction = wordslot.get_direction()
    row, col = start_row, start_col
    partial_str = ""
    for j in range(word_len):
        partial_str += layout[row][col]
        if direction == "ACROSS":
            col += 1
        else:
            row += 1

    # # Now, we query dictionary based on the character constraints defined above
    # word_url = "https://api.datamuse.com/words?sp=" + partial_str + "&md=d"
    # word_data = requests.get(word_url)
    # word_json = json.loads(word_data.text)
    # j = 0
    regex_str = "^("
    for char in partial_str:
        if char == "?":
            regex_str += "[a-z]"
        else:
            regex_str += char
    regex_str += ")$"

    available_words = list(filter(lambda v: match(regex_str, v), theme_dict))
    available_words = [i for i in available_words if i not in seen_words]


    # The DataMuse API returns a list of python dictionaries; each dictionary is a single word,
    # along with all of its definitions. Unfortunately, some words have no definitions, so
    # we simply remove them. Additionally, we remove all words that are already on the crossword layout.
    # Finally, DataMuse does not count spaces in its word length, (e.g. "et al" is considered a word with
    # 4 letters). Thus, we strip whitespace from every legal word to make sure word lengths are aligned.
    # while j < len(word_json):
    #     if "defs" not in word_json[j] or word_json[j]["word"] in seen_words:
    #         del word_json[j]
    #     else:
    #         word_json[j]["word"] = word_json[j]["word"].replace(" ", "")
    #         j += 1

    # Our list of word dictionaries at this point will be ~80 words; we sample at most 10 of them 
    # to store in our word list for the WordSlot object (for speed).
    # The number 10 is basically a magic number, but this was the number recommended by this paper:
    # https://www.aaai.org/Papers/AAAI/1990/AAAI90-032.pdf
    cur_list = random.sample(available_words, min(10, len(available_words)))
    final_list = []

    # Set scores for each word initially set to 0
    for word in cur_list:
        final_list.append([word, 0])
    return final_list


def create_crossword(word_slots, layout_cols, layout_rows, theme_words):
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
    # (Not that this only keeps track of the words that are currently IN USE in the crossword)

    done_slots = [] # Keeps track of WordSlots who have valid words currently written to the crossword layout
    filled_layout = [["?"] * layout_cols for _ in range(layout_rows)]

    # We keep iterating until every WordSlot has a legal word that can be placed in the layout
    while len(done_slots) < len(word_slots):
        i, _ = find_next_slot(filled_layout, done_slots, word_slots, seen_words, theme_words)
        restart = False

        # If words is None, we need to query the dictionary to get a set of words for this WordSlot
        if word_slots[i].get_words() is None:

            final_list = fetch_words(word_slots[i], filled_layout, seen_words, theme_words)
            # final_list gives the set of words with uninitialized scores; we now "look ahead"
            # to assign numerical scores for each word in final_list (heuristic #2)
            for j in range(len(final_list)):
                write_word(filled_layout, word_slots[i], final_list[j][0])
                done_slots.append(i)
                _, score = find_next_slot(filled_layout, done_slots, word_slots, seen_words, theme_words)
                final_list[j][1] = score
                erase_word(filled_layout, i, word_slots)
                done_slots.pop()
            # Sort the list by score, ascending order (last word is always most optimal word to pick)
            final_list.sort(key=lambda x:x[1])
            
            # This sets a list of at most 20 words that can fit the current crossword at a particular WordSlot
            word_slots[i].set_words(final_list)

        # At this point, the WordSlot object has at least attempted to find words (words is not None)
        cur_words = word_slots[i].get_words()
        # If the words is empty (DIFFERENT from None) then there are simply no words that fit the 
        # current character constraints -- we need to go backward and change words
        if cur_words == []:

            # Set the words to be None (so it will be re-initialized later)
            word_slots[i].set_words(None)

            # We go "backwards" by picking a WordSlot that overlaps with the current WordSlot 
            # that also has alternative words to pick. Once this is found, we reset every
            # WordSlot after this overlapped WordSlot and erase those words from the layout.
            word_overlaps = word_slots[i].get_overlap()
            j = len(word_overlaps) - 1
            found_overlap = False

            # Iterate through all overlaps
            while j >= 0 and found_overlap == False:
                cur_overlap = word_overlaps[j][0]
                cur_words = word_slots[cur_overlap].get_words()
                if cur_overlap in done_slots and cur_words is not None and len(cur_words) >= 2:
                    # We found a suitable overlap; erase everything beyond that overlap
                    overlap_ind = done_slots.index(cur_overlap)
                    for k in range(overlap_ind, len(done_slots)):
                        seen_words.remove(word_slots[done_slots[k]].get_best_word())
                        erase_word(filled_layout, done_slots[k], word_slots)
                        word_slots[done_slots[k]].set_words(None)
                    del done_slots[overlap_ind:]
                    i = cur_overlap
                    found_overlap = True
                j -= 1
                
            # If no overlap with alternatives have been found, we just start over from the beginning.
            if found_overlap == False:
                print("No solution found, restarting... \n")
                restart = True
                for j in range(len(word_slots)):
                    word_slots[j].set_words(None)
                seen_words = set()
                done_slots = []
                filled_layout = [["?"] * layout_cols for _ in range(layout_rows)]

            # If an alternative has been found, note that current word in use is always the last word 
            # picked, so we pop it off the list and erase that word from both seen_words 
            # (not used anymore) and from the crossword layout
            else:
                removed_word = cur_words.pop()
                word_slots[i].set_words(cur_words)

        if restart == False:
            # If we are not restarting, then we pick a word to write (always the last word),
            # in the wordlist for a WordSlot object, write it to the layout, and add to seen_words.
            # Then, we can add this WordSlot id to done_slots
            best_word = word_slots[i].get_best_word()
            write_word(filled_layout, word_slots[i], best_word)
            seen_words.add(best_word)
            done_slots.append(i)
        
    return filled_layout

from calendar import c
import random
from re import match
from word_slot import WordSlot

def find_next_slot(layout, done_slots, word_slots, seen_words, theme_words, choice_optimize):
    """
    Decides next WordSlot to fill in our current layout
    Input:      [layout] - the 2D matrix containing the current crossword layout
                [done_slots] - the list of WordSlot ids that have already been filled
                [seen_words] - the set of words that have already been placed

    Output:     [cur_min_ind] - the WordSlot id to fill in next
                [cur_min] - the number of word possibilities for the WordSlot with id cur_min_ind
    """

    if choice_optimize == 1:
        # We fill the most constrained WordSlot next. To do this, we simply 
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
    else:
        # Otherwise, we simply go through WordSlots in order
        if done_slots == []:
            return 0, len(fetch_words(word_slots[0], layout, seen_words,theme_words))
        else:
            ind = done_slots[-1] + 1
            return ind, len(fetch_words(word_slots[ind], layout, seen_words,theme_words))

def write_word(layout, word_obj, word_to_write):
    """
    Writes a chosen word to our current crossword layout
    Input:      [layout] - the 2D matrix containing the current crossword layout
                [word_obj] - The WordSlot object whose chosen word will be written

    """
    # Get word to write, word length, and direction from word_obj
    start_row, start_col = word_obj.get_start()
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

def erase_word(layout, word_obj, done_slots):
    """
    Selectively erases parts of a word from the crossword layout when bactracking.
    Input:      [layout] - the 2D matrix containing the current crossword layout
                [word_id] - the index of the WordSlot object in question from the WordSlot array
                [word_slots] - the WordSlot array
    """
    # Get start location, length, direction of word to remove
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
            if o_id in done_slots and o_row == row and o_col == col:
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

    regex_str = "^("
    for char in partial_str:
        if char == "?":
            regex_str += "[a-z]"
        else:
            regex_str += char
    regex_str += ")$"

    available_words = list(filter(lambda v: match(regex_str, v), theme_dict))
    available_words = [i for i in available_words if i not in seen_words]

    final_list = []

    # Set scores for each word initially set to 0
    for word in available_words:
        final_list.append([word, 0])
    return final_list

def check_theme(cur_theme, word_list):

    for word in word_list:
        cur_len = word.get_length()
        len_words = [i for i in cur_theme if len(i) == cur_len]
        if len(len_words) < 200:
            return False
    return True


def create_crossword(word_slots, layout_cols, layout_rows, all_theme_words, choice_optimize, instantiate_optimize, backtrack_optimize):
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

    # Pick a valid theme for this crossword layout
    theme_viable = False
    theme_names = list(all_theme_words.keys())
    theme_names = [i for i in theme_names if i != 'all_themes']
    while theme_viable == False and theme_names != []:
        cur_theme_name = random.choice(theme_names)
        cur_theme = [i[0] for i in all_theme_words[cur_theme_name]]
        if not check_theme(cur_theme, word_slots):
            theme_names.remove(cur_theme_name)
        else:
            theme_viable = True
            theme_words = cur_theme
            if cur_theme_name == 'sci.med':
                cur_theme_name = "Medicine"
            if cur_theme_name == 'sci.electronics':
                cur_theme_name = "Electronics"
            if cur_theme_name == 'talk.religion.misc':
                cur_theme_name = "Religion"
            if cur_theme_name == 'talk.politics.misc':
                cur_theme_name = "Politics"
            if cur_theme_name == 'misc.forsale':
                cur_theme_name = "Sales Items"
    if theme_viable == False:
        theme_words = [i[0] for i in all_theme_words['all_themes']]
        cur_theme_name = "Miscellaneous"

    # We keep iterating until every WordSlot has a legal word that can be placed in the layout
    while len(done_slots) < len(word_slots):

        i, _ = find_next_slot(filled_layout, done_slots, word_slots, seen_words, theme_words, choice_optimize)
        restart = False

        # If words is None, we need to query the dictionary to get a set of words for this WordSlot
        if word_slots[i].get_words() is None:

            cur_list = fetch_words(word_slots[i], filled_layout, seen_words, theme_words)
            final_list = random.sample(cur_list, min(10, len(cur_list)))

            # If instantiate is not naie we need to sort these word candidates in some way
            if instantiate_optimize == 2 or instantiate_optimize == 1:
                done_slots.append(i)
                for j in range(len(final_list)):
                    write_word(filled_layout, word_slots[i], final_list[j][0])
                    seen_words.add(final_list[j][0])
                    if instantiate_optimize == 2:
                        # Score by "product overlap" heuristic
                        total_score = 1
                        for overlap, _, _ in word_slots[i].get_overlap():
                            score = len(fetch_words(word_slots[overlap], filled_layout, seen_words, theme_words))
                            total_score = total_score * score
                        final_list[j][1] = total_score
                    else:
                        # score by "lookahead" heuristic
                        _, score = find_next_slot(filled_layout, done_slots, word_slots, seen_words, theme_words)
                        final_list[j][1] = score
                        
                    erase_word(filled_layout, word_slots[i], done_slots)
                    seen_words.remove(final_list[j][0])
                done_slots.pop()

            # Sort the list by score, ascending order (last word is always most optimal word to pick)
            final_list.sort(key=lambda x:x[1])
            word_slots[i].set_words(final_list)



        # At this point, the WordSlot object has at least attempted to find words (words is not None)
        cur_words = word_slots[i].get_words()

        # If the words is empty (DIFFERENT from None) then there are simply no words that fit the 
        # current character constraints -- we need to go backward and change words
        if cur_words == []:

            # Set the words to be None (so it will be re-initialized later)
            word_slots[i].set_words(None)

            if backtrack_optimize == 1:
                # We go "backwards" by picking a WordSlot that overlaps with the current WordSlot 
                # that also has alternative words to pick. Once this is found, we reset every
                # WordSlot after this overlapped WordSlot and erase those words from the layout.
                word_overlaps = word_slots[i].get_overlap()
                j = len(word_overlaps) - 1
                found_overlap = False

                # Iterate through all overlaps
                while j >= 0 and found_overlap == False:
                    cur_overlap = word_overlaps[j][0]
                    cur_overlap_words = word_slots[cur_overlap].get_words()
                    if cur_overlap in done_slots and cur_overlap_words is not None and len(cur_overlap_words) >= 2:
                        # We found a suitable overlap; erase everything beyond that overlap
                        overlap_ind = done_slots.index(cur_overlap)
                        k = overlap_ind + 1
                        while k < len(done_slots):
                            done_slots_ind = done_slots[k]
                            del done_slots[k]
                            seen_words.remove(word_slots[done_slots_ind].get_best_word())
                            erase_word(filled_layout, word_slots[done_slots_ind], done_slots)
                            word_slots[done_slots_ind].set_words(None)
                        i = cur_overlap
                        found_overlap = True
                    j -= 1
                    
                # If no overlap with alternatives have been found, we just start over from the beginning.
                if found_overlap == False:
                    restart = True

                # If an alternative has been found, note that current word in use is always the last word 
                # picked, so we pop it off the list and erase that word from both seen_words 
                # (not used anymore) and from the crossword layout
                else:
                    erase_word(filled_layout, word_slots[i], done_slots)
                    removed_word = cur_overlap_words.pop()
                    
                    seen_words.remove(removed_word[0])
                    done_slots.pop()
                    word_slots[i].set_words(cur_overlap_words)
    
            else:
                # Otherwise, we simply back up to the first WordSlot that has alternatives, and go from there.
                if done_slots == []:
                    restart = True
                else:
                    found_replacement = False
                    while found_replacement == False and done_slots != []:
                        i = done_slots.pop()
                        erase_word(filled_layout, word_slots[i], done_slots)
                        word_set = word_slots[i].get_words()
                        removed_word = word_set.pop()
                        seen_words.remove(removed_word[0])
                        if word_set == []:
                            word_slots[i].set_words(None)
                        else:
                            word_slots[i].set_words(word_set)
                            found_replacement = True
                
                    if found_replacement == False:
                        restart = True
        if restart == False:
            # If we are not restarting, then we pick a word to write (always the last word),
            # in the wordlist for a WordSlot object, write it to the layout, and add to seen_words.
            # Then, we can add this WordSlot id to done_slots
            best_word = word_slots[i].get_best_word()
            write_word(filled_layout, word_slots[i], best_word)
            seen_words.add(best_word)
            done_slots.append(i)
        else:
            print("No solution found, restarting... \n")
            for j in range(len(word_slots)):
                word_slots[j].set_words(None)
            seen_words = set()
            done_slots = []
            filled_layout = [["?"] * layout_cols for _ in range(layout_rows)]

        
        
    return filled_layout, cur_theme_name

import json
import requests
import random
from collections import OrderedDict
from word_slot import WordSlot
    

def find_word(row, col, mat, direction):
    """
    Detects the empty slot starting from index [row][col] in the given
    orientation.

    Input:  [row] - Row index integer of where slot starts
            [col] - Column index integer of where slot starts
            [mat] - 2D matrix describing the crossword layout
            [direction] - Orientation of to-be-detected slot
                          Either "ACROSS" or "DOWN"

    Output: [slot_len] - Integer representing length of detected slot
    """
    slot_len = 0
    # Check for length of slot while index is not out of bounds
    while row != len(mat) and col != len(mat[0]) and mat[row][col] != 0: 
        mat[row][col] -= 1
        if direction == "ACROSS":
            col += 1
        else:
            row += 1
        slot_len += 1
    return slot_len


def find_overlap(slot_id, word_slots):
    """
    Finds other slots that overlap with the slot associated with slot_id.
    Input:  [slot_id] - id of slot we are trying to detect overlaps for
            [word_slots] - Dictionary of {id: WordSlot} pairs that need to be
                        defined/filled out
    """
    # slot_id information
    start_row = word_slots[slot_id].get_start(0)
    end_row = start_row + word_slots[slot_id].get_length() - 1
    word_col = word_slots[slot_id].get_start(1)

    # Check every horizontal slot in word_slots if it overlaps with slot_id
    for key in word_slots:
        slot = word_slots[key]
        if slot.get_direction() == "ACROSS":
            # Current horizontal slot information
            start_col = slot.get_start(1)
            end_col = start_col + slot.get_length() - 1
            dict_row = slot.get_start(0)
            if word_col >= start_col and word_col <= end_col:
                if dict_row >= start_row and dict_row <= end_row:
                    word_slots[slot_id].add_overlap(key)
                    word_slots[key].add_overlap(slot_id)


def analyze_layout(layout):
    """
    Input:  [layout] - 2D matrix describing the crossword layout
                       1 represents white spaces, 0 represents black spaces
            Example: [[1,0,0,0], [1,0,0,0], [1,0,0,0], [1,0,0,0]]
                    [[1,1,1,1], [1,0,1,0], [1,0,1,0], [1,0,1,0]]

    Ouput:  [word_slots] - Dictionary of {id: WordSlot} pairs that need to be
                        defined/filled out
    """
    num_rows, num_cols = len(layout), len(layout[0])
    word_slots = OrderedDict()
    id_count = 0
    # Find all horizontal/"across" word slots in the layout
    mode = "ACROSS"
    temp_array = [row[:] for row in layout] # Copy of layout
    for i in range(num_rows):
        j = 0
        while j < num_cols:
            if temp_array[i][j] > 0: # Start index of word detected
                slot_len = find_word(i, j, temp_array, mode)
                if slot_len > 1:
                    word_slots[id_count] = WordSlot((i, j), mode, slot_len)
                    id_count += 1
                j += max(1, slot_len + 1)
            else:
                j += 1
    # Find all vertical/"down" word slots in the layout
    mode = "DOWN"
    temp_array = [row[:] for row in layout] # Copy of layout
    for i in range(num_cols):
        j = 0
        while j < num_rows:
            if temp_array[j][i] > 0: # Start index of word detected
                slot_len = find_word(j, i, temp_array, mode)
                if slot_len > 1:
                    word_slots[id_count] = WordSlot((j, i), mode, slot_len)
                    find_overlap(id_count, word_slots)
                    id_count += 1
                j += max(1, slot_len + 1)
            else:
                j += 1
    return word_slots


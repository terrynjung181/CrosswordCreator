import json
import requests
import random
from collections import OrderedDict


def find_overlap(word_id, word_dict):
    start_row = word_dict[word_id]["start"][0]
    end_row = start_row + word_dict[word_id]["length"] - 1
    word_col = word_dict[word_id]["start"][1]
    for key in word_dict:
        if word_dict[key]["direction"] == "ACROSS":
            start_col = word_dict[key]["start"][1]
            end_col = start_col + word_dict[key]["length"] - 1
            dict_row = word_dict[key]["start"][0]
            if word_col >= start_col and word_col <= end_col:
                if dict_row >= start_row and dict_row <= end_row:
                    word_dict[word_id]["overlap"].append(key)
                    word_dict[key]["overlap"].append(word_id)



def analyze_layout(layout):
    # Takes in a 2D matrix describing the crossword layout,
    # returns dictionary of words we need to define

    num_rows = len(layout)
    num_cols = len(layout[0])
    word_dict = OrderedDict()
    id_count = 0

    temp_array = [row[:] for row in layout]
    mode = "ACROSS"
    for i in range(num_rows):
        j = 0
        while j < num_cols:
            if temp_array[i][j] > 0:
                word_len = find_word(i, j, temp_array, mode)
                if word_len > 1:
                    word_dict[id_count] = {"start": (i, j), "length": word_len, "direction": mode, "overlap": []}
                    id_count += 1
                j += max(1, word_len + 1)
            else:
                j += 1
    
    temp_array = [row[:] for row in layout]
    mode = "DOWN"
    for i in range(num_cols):
        j = 0
        while j < num_rows:
            if temp_array[j][i] > 0:
                word_len = find_word(j, i, temp_array, mode)
                if word_len > 1:
                    word_dict[id_count] = {"start": (j, i), "length": word_len, "direction": mode, "overlap": []}
                    find_overlap(id_count, word_dict)
                    id_count += 1
                j += max(1, word_len + 1)
            else:
                j += 1

        
    return word_dict

def find_word(start_row, start_col, mat, direction):
    row = start_row
    col = start_col
    word_len = 0
    while row != len(mat) and col != len(mat[0]) and mat[row][col] != 0: 
        mat[row][col] -= 1
        if direction == "ACROSS":
            col += 1
        else:
            row += 1
        word_len += 1
    return word_len

def create_crossword(word_dict, layout_cols, layout_rows):
    filled_layout = [["?"] * layout_cols for _ in range(layout_rows)]
    for key in word_dict:
        start_row, start_col = word_dict[key]["start"]
        word_len = word_dict[key]["length"]
        direction = word_dict[key]["direction"]
        row = start_row
        col = start_col
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
        if len(word_json) == 0:
            print(partial_str)
            print("NO RESULT")
            exit(0)
        rand_word = word_json[random.randint(0, len(word_json)-1)]
        if "defs" not in rand_word:
            print(partial_str)
            print("NO DEF")
            exit(0)
        word_dict[key]["word"] = rand_word["word"]
        
        word_dict[key]["definition"] = rand_word["defs"]

        row = start_row
        col = start_col
        for i in range(len(rand_word["word"])):
            filled_layout[row][col] = rand_word["word"][i]
            if direction == "ACROSS":
                col += 1
            else:
                row += 1
        
    return filled_layout


# test_mat = [[1,0,0,0], [1,0,0,0], [1,0,0,0], [1,0,0,0]]
# word_dict = analyze_layout(test_mat)
# new_layout = create_crossword(word_dict,len(test_mat[0]), len(test_mat))
# print(word_dict)
# print(new_layout)
# print("\n")

# test_mat = [[1,1,1,1], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
# word_dict = analyze_layout(test_mat)
# new_layout = create_crossword(word_dict,len(test_mat[0]), len(test_mat))
# print(word_dict)
# print(new_layout)
# print("\n")

test_mat = [[1,1,1,1], [1,0,1,0], [1,0,1,0], [1,0,1,0]]
word_dict = analyze_layout(test_mat)
#new_layout = create_crossword(word_dict, len(test_mat[0]), len(test_mat))
print(word_dict)
#print(new_layout)
print("\n")

test_mat = [[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]]
word_dict = analyze_layout(test_mat)
#new_layout = create_crossword(word_dict, len(test_mat[0]), len(test_mat))
print(word_dict)
#print(new_layout)
print("\n")

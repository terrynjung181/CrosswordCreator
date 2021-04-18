import json
import requests


def create_crossword(word_dict, layout_cols, layout_rows):
    filled_layout = [["?"] * layout_cols] * layout_rows
    for key in word_dict:
        start_row, start_col = word_dict[key]["start"]
        word_len = word_dict[key]["length"]
        direction = word_dict[key]["direction"]
        if direction == "ACROSS":
            partial_str = "".join(filled_layout[start_row][start_col:start_col + word_len])
        else:
            partial_str = "".join(filled_layout[start_row:start_row + word_len][start_col])
        
        word_url = "https://api.datamuse.com/words?sp=" + partial_str + "&md=d"
        word_data = requests.get(word_url)
        print(word_data)
        word_json = json.loads(word_data.text)

        if word_data == []:
            print("NO WORD FOUND WITH PARTIAL STRING " + partial_str)
            exit(0)
        else:
            first_word = word_data[0]
            word_dict[key]["word"] = first_word["word"]
            word_dict[key]["definition"] = first_word["defs"][0]

    return word_dict
            



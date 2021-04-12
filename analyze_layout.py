def analyze_layout(layout):
    # Takes in a 2D matrix describing the crossword layout,
    # returns dictionary of words we need to define

    num_rows = len(layout)
    num_cols = len(layout[0])
    word_dict = {}
    id_count = 0

    temp_array = [row[:] for row in layout]
    mode = "ACROSS"
    for i in range(num_rows):
        j = 0
        while j < num_cols:
            if temp_array[i][j] > 0:
                word_len = find_word(i, j, temp_array, mode)
                if word_len > 1:
                    word_dict[id_count] = [(i, j), word_len, mode]
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
                    word_dict[id_count] = [(j, i), word_len, mode]
                    id_count += 1
                j += max(1, word_len + 1)
            else:
                j += 1

        
    print(word_dict)
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


test_mat = [[1,0,0,0], [1,0,0,0], [1,0,0,0], [1,0,0,0]]
analyze_layout(test_mat)

test_mat = [[1,1,1,1], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
analyze_layout(test_mat)

test_mat = [[1,1,1,1], [1,0,1,0], [1,0,1,0], [1,0,1,0]]
analyze_layout(test_mat)

test_mat = [[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]]
analyze_layout(test_mat)



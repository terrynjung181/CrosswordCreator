import analyze_layout
import generate_words

# test_mat = [[1,0,0,0], [1,0,0,0], [1,0,0,0], [1,0,0,0]]
# word_dict = analyze_layout.analyze_layout(test_mat)
# new_layout = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat))
# print(word_dict)
# print(new_layout)
# print("\n")

# test_mat = [[1,1,1,1], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
# word_dict = analyze_layout.analyze_layout(test_mat)
# new_layout = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat))
# print(word_dict)
# print(new_layout)
# print("\n")

# test_mat = [[1,1,1,1], [1,0,1,0], [1,0,1,0], [1,0,1,0]]
# word_dict = analyze_layout.analyze_layout(test_mat)
# new_layout = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat))
# print(word_dict)
# print(new_layout)
# print("\n")


test_mat = [[1,1,1], [1,1,1], [1,1,1]]
word_dict = analyze_layout.analyze_layout(test_mat)
new_layout = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat))
print(word_dict)
print(new_layout)
print("\n")


# test_mat = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
#             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#             [1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
#             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#             [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
#             [1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
#             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# word_dict = analyze_layout.analyze_layout(test_mat)
# new_layout = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat))
# print(word_dict)
# print(new_layout)
# print("\n")


# test_mat = [[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]]
# word_dict = analyze_layout.analyze_layout(test_mat)
# new_layout = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat))
# print(word_dict)
# print(new_layout)
# print("\n")
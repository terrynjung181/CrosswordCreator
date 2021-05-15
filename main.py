import os
import sys
import pickle
sys.path.append("layout_solver")
sys.path.append("theme_classifier")
from layout_solver import analyze_layout, generate_words
from theme_classifier import theme_extractor 

#test_mat = [[1,0,0,0], [1,0,0,0], [1,0,0,0], [1,0,0,0]]
#test_mat = [[1,1,1,1], [1,0,1,0], [1,0,1,0], [1,0,1,0]]
test_mat = [[1,1,1], [1,1,1], [1,1,1]]
word_dict = analyze_layout.analyze_layout(test_mat)
with open(os.path.join("theme_classifier", "pkl_storage", "theme_dictionary.pkl"), "rb") as f:
    themed_words = pickle.load(f)
cur_theme_words = themed_words['rec.sport.baseball']
# for key in themed_words:
#     cur_theme_words.extend(themed_words[key])
print(len(cur_theme_words))
new_layout = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat), cur_theme_words)
print(word_dict)
print(new_layout)
print("\n")

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


# test_mat = [[1,1,1], [1,1,1], [1,1,1]]
# word_dict = analyze_layout.analyze_layout(test_mat)
# new_layout = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat))
# print(word_dict)
# print(new_layout)
# print("\n")


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

# test_mat = [[1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1]]
# word_dict = analyze_layout.analyze_layout(test_mat)
# new_layout = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat))
# print(word_dict)
# print(new_layout)
# print("\n")

# test_mat = [[1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,1,1,1]]
# word_dict = analyze_layout.analyze_layout(test_mat)
# new_layout = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat))
# print(word_dict)
# print(new_layout)
# print("\n")
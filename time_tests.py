import os
import sys
import pickle
sys.path.append("layout_solver")
sys.path.append("theme_classifier")
from layout_solver import analyze_layout, generate_words
from clue_maker import generate_clues
from gui import run_intro_gui, run_exit_gui
import time


timer_array = []
iterations = 5
with open(os.path.join("theme_classifier", "pkl_storage", "theme_dictionary.pkl"), "rb") as f:
    themed_words = pickle.load(f)

for i in range(iterations):
    tic = time.perf_counter()
    test_mat = [[1,1,1,0, 0, 0], [1,1,1,0,0,0], [1,1,1,0,0,0], [1,1,1,0,0,0], [0,0,0,0,0,0],[0,0,0,0,0,0]]
    word_dict = analyze_layout.analyze_layout(test_mat)
    if word_dict == -1:
        print("CROSSWORD LAYOUT BAD \n")
        exit(0)
    new_layout, theme_name = generate_words.create_crossword(word_dict, len(test_mat[0]), len(test_mat), themed_words, \
                                                            1, 0, 0)
    toc = time.perf_counter()
    timer_array.append(toc - tic)
    print(toc - tic)
    print(str(i) + "DONE ")

print(timer_array)
print(sum(timer_array)/len(timer_array))
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pickle
with open("theme_classifier/pkl_storage/theme_dictionary.pkl", "rb") as f:
    total_data = pickle.load(f)
for key in total_data.keys():
    print(key)
    xxx = [x[0] for x in total_data[key]]
    word_lens = [len(x) for x in xxx]
    max_bin = max(word_lens)
    plt.hist(word_lens, max_bin)
    plt.savefig(key + ".png")
    plt.clf()
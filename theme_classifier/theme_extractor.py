import json
import os
import pickle
from naive_bayes import NaiveBayes
from sklearn.datasets import fetch_20newsgroups

def theme_extractor(dictionary_file, nb_pkl):
    with open(dictionary_file,"rb") as f:
        words_dict = json.load(f)

    with open(nb_pkl, "rb") as f:
            nb = pickle.load(f)

    categories=['sci.med', 'sci.electronics', 'talk.religion.misc', 'talk.politics.misc', 'misc.forsale']

    newsgroups_train = fetch_20newsgroups(subset='train', categories=categories)
    sorted_categories = newsgroups_train.target_names
    print(sorted_categories)
    themes = {i: [] for i in categories}

    for word in words_dict.keys():
        definition = words_dict[word]
        if len(definition.split()) > 5:
            ind_max = nb.infer(definition)
            themes[sorted_categories[ind_max]].append(word)

    theme_counts = []
    for key in themes:
        theme_counts.append([key, len(themes[key])])
    print(theme_counts)
    with open(os.path.join("pkl_storage", "theme_dictionary.pkl"), "wb") as f:
        pickle.dump(themes, f)

if __name__ == "__main__":
    theme_extractor("dictionary.json", "pkl_storage/trained_nb.pkl")
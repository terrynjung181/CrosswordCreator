import pickle
import os
import json
from sklearn.datasets import fetch_20newsgroups
import wikipediaapi
import time
from naive_bayes import NaiveBayes

def theme_extractor(categories, dictionary_file, nb_pkl):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    with open(dictionary_file,"rb") as f:
        words_dict = json.load(f)

    with open(nb_pkl, "rb") as f:
        nb = pickle.load(f)

    # themes = {i: [] for i in categories}
    with open(os.path.join("pkl_storage", "theme_dictionary.pkl"), "rb") as f:
        themes = pickle.load(f)
    offset = 0
    for i in themes:
        offset += len(themes[i])
    print(categories)
    word_list = list(words_dict.keys())
    print(offset)
    for i in range(offset, len(word_list)):
        word = word_list[i]
        definition = words_dict[word]
        page_py = wiki_wiki.page(word)
        if page_py.exists():
            probs, ind_max = nb.infer_probs(page_py.summary)
        else:
            probs, ind_max = nb.infer_probs(definition)
        themes[categories[ind_max]].append([word, max(probs)])

        if i > 0 and i % 100 == 0:
            print("Checkpoint..." + str(i))
            with open(os.path.join("pkl_storage", "theme_dictionary.pkl"), "wb") as f:
                pickle.dump(themes, f)
            time.sleep(1)
            
    print(themes)
    theme_counts = []
    for key in themes:
        theme_counts.append([key, len(themes[key])])
    print(theme_counts)
    with open(os.path.join("pkl_storage", "theme_dictionary.pkl"), "wb") as f:
        pickle.dump(themes, f)


def train_nb(filename):
    categories=['sci.med', 'sci.electronics', 'talk.religion.misc', 'talk.politics.misc', 'misc.forsale']
    newsgroups_train = fetch_20newsgroups(subset='train', categories=categories)
    sorted_categories = newsgroups_train.target_names
    # ['comp.windows.x', 'rec.autos', 'rec.sport.baseball', 'sci.space', 'talk.politics.misc', 'talk.religion.misc']
    print(sorted_categories)
    train_data = newsgroups_train.data
    train_labels = newsgroups_train.target

    # count = len(set(train_labels))
    # nb = NaiveBayes(count)

    # nb.train(train_data, train_labels)

    # with open(os.path.join("pkl_storage", filename), "wb") as f:
    #     pickle.dump(nb, f)

    theme_extractor(sorted_categories, "dictionary.json", os.path.join("pkl_storage", filename))


if __name__ == "__main__":
    train_nb("trained_nb.pkl")
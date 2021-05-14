import json
import os
import pickle
from naive_bayes import NaiveBayes

with open("dictionary.json","rb") as f:
    words_dict = json.load(f)

with open(os.path.join("..", "trained_models", "trained_nb.pkl"), "rb") as f:
        nb = pickle.load(f)

categories=['sci.space', 'sci.electronics', 'talk.politics.guns', 'sci.med', 'comp.graphics',
                'rec.sport.baseball', 'talk.religion.misc', 'rec.autos', 'misc.forsale', 'talk.politics.misc']
themes = {i: [] for i in categories}

for word in words_dict.keys():
    definition = words_dict[word]
    ind_max = nb.infer(definition)
    themes[categories[ind_max]].append(word)

    done = True
    for i in themes:
        if len(themes[i]) < 1000:
            done = False

    if done:
        print(themes)
        break
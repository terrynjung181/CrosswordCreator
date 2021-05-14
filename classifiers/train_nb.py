import pickle
import os
from sklearn.datasets import fetch_20newsgroups
from naive_bayes import NaiveBayes

def train_nb(filename):
    categories=['sci.space', 'sci.electronics', 'talk.politics.guns', 'sci.med', 'comp.graphics',
                'rec.sport.baseball', 'talk.religion.misc', 'rec.autos', 'misc.forsale', 'talk.politics.misc']
    newsgroups_train = fetch_20newsgroups(subset='train', categories=categories)
    print(newsgroups_train.target_names)
    # ['comp.windows.x', 'rec.autos', 'rec.sport.baseball', 'sci.space', 'talk.politics.misc', 'talk.religion.misc']

    train_data = newsgroups_train.data
    train_labels = newsgroups_train.target

    count = len(set(train_labels))
    nb = NaiveBayes(count)

    nb.train(train_data, train_labels)

    with open(os.path.join("trained_models", filename), "wb") as f:
        pickle.dump(nb, f)

train_nb("trained_nb.pkl")

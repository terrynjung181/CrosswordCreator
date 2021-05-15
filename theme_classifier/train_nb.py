import pickle
import os
from sklearn.datasets import fetch_20newsgroups
from naive_bayes import NaiveBayes

def train_nb(filename):
    categories=['sci.med', 'sci.electronics', 'talk.religion.misc', 'talk.politics.misc', 'misc.forsale']
    newsgroups_train = fetch_20newsgroups(subset='train', categories=categories)
    print(newsgroups_train.target_names)
    # ['comp.windows.x', 'rec.autos', 'rec.sport.baseball', 'sci.space', 'talk.politics.misc', 'talk.religion.misc']

    train_data = newsgroups_train.data
    train_labels = newsgroups_train.target

    count = len(set(train_labels))
    nb = NaiveBayes(count)

    nb.train(train_data, train_labels)

    with open(os.path.join("pkl_storage", filename), "wb") as f:
        pickle.dump(nb, f)

if __name__ == "__main__":
    train_nb("trained_nb.pkl")
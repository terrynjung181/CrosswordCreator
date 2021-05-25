"""
naive_bayes.py
implementation of naive bayes classification algorithm

"""
from collections import Counter
import math
import pandas as pd

from utils import words_to_counter, words_to_clean

# questions: why use full vocab size
# why add 1 to both the numerator and denominator of proabbilities
class NaiveBayes:

    def __init__(self, num_cats):

        """
        NaiveBayes Int -> None

        constructs NaiveBayes object, sets the number of unique_classes
        equal to unique_classes

        """

        self.num_cats = num_cats

    def train(self, dataset, labels):

        """
        NaiveBayes List List -> None

        generate counters for each dataset

        """

        # initialize frequency counter dictionary and document counter
        self.occurrences_by_cat = {} # number of occurrences of each word, by category
        self.doc_occurrences = Counter() # number of documents containing each word, overall
        for i in range(self.num_cats):
            self.occurrences_by_cat[i] = Counter()

        self.total_docs = 0 # total number of documents
        self.docs_by_cat = [0] * self.num_cats # number of documents per category

        # for each article, increment global self.doc_occurrences and category-wise self.occurrences_by_cat
        for i, article in enumerate(dataset):
            article_counter, doc_counter = words_to_counter(article)
            article_cat = labels[i]
            self.occurrences_by_cat[article_cat] += article_counter
            self.doc_occurrences += doc_counter

            # increment document count fields
            self.docs_by_cat[article_cat] += 1
            self.total_docs += 1

        self.compute_priors()
        self.bows_from_frequencies()
        self.tf_idf_from_frequencies()

    def compute_priors(self):
        """
        NaiveBayes -> None
        computes prior probabilities of each class

        """
        self.prior = [(i / self.total_docs) for i in self.docs_by_cat]

    def bows_from_frequencies(self):
        """
        NaiveBayes -> None

        generate bag of words probabilities for each class and put them in dict

        """

        # initialize bags of words by category
        self.bows_by_cat = {}
        for i in range(self.num_cats):
            self.bows_by_cat[i] = {}

        self.default_bows = {} # if the word doesn't show up, what to make its default value
        for cat in self.occurrences_by_cat:
            occurrences = self.occurrences_by_cat[cat]

            total = sum(occurrences.values())  #+ 1
            length = len(self.doc_occurrences) # + 1 # len(occurrences)
            bows_scores = {key: (value + 1) / (total + length) for key, value in occurrences.items()}
            self.bows_by_cat[cat] = bows_scores
            self.default_bows[cat] = 1 / (total + length)

    def gen_idf(self):
        """
        NaiveBayes -> None
        Generate idf scores for every word in the corpus

        """
        # calculate idf for every word in the corpus
        self.idf_scores = {}
        for w in self.doc_occurrences:
            idf = math.log(self.total_docs/self.doc_occurrences[w])
            self.idf_scores[w] = idf


    def tf_idf_from_frequencies(self):
        """
        NaiveBayes -> None

        generate tf-idf scores for each class and put them in dict

        """
        # generate idf scores for every word
        self.gen_idf()

        # intialize dict of tf_idf scores for each class
        self.tf_idf_by_cat = {}
        for i in range(self.num_cats):
            self.tf_idf_by_cat[i] = {}

        self.default_tf_idf = {} # if the word doesn't show up, what to make its tf-idf score

        # generate tf_idf scores for each category
        for cat in self.occurrences_by_cat:
            occurrences = self.occurrences_by_cat[cat]

            numerator_dict = {}

            for w in occurrences:
                tf_idf_numerator = occurrences[w] * self.idf_scores[w]
                numerator_dict[w] = tf_idf_numerator

            total = sum(numerator_dict.values()) # + 1
            length = len(self.doc_occurrences) # + 1 # len(occurrences)
            tf_idf_scores = {key: (value + 1) / (total + length) for key, value in numerator_dict.items()}
            self.tf_idf_by_cat[cat] = tf_idf_scores
            self.default_tf_idf[cat] = 1 / (total + length)

    def infer(self, text, tf_idf=True):

        """
        NaiveBayes String Boolean -> Int

        Returns the index of the  of the maximum probability, using tf_idf if tf_idf
        is true, else BoW

        """
        probs, cat = self.infer_probs(text, tf_idf)

        return cat

    def infer_probs(self, text, tf_idf=True):

        """
        NaiveBayes String Boolean -> List

        Returns a list of the probabilities by category for each class

        """
        cleaned = words_to_clean(text)
        probs = []
        
        for cat in range(0, self.num_cats):
            prob = math.log(self.prior[cat])

            # add up prob of each word
            for w in cleaned:
                if tf_idf:
                    if w in self.tf_idf_by_cat[cat]:
                        prob += math.log(self.tf_idf_by_cat[cat][w])
                    else:
                        prob += math.log(self.default_tf_idf[cat])

                else:
                    if w in self.bows_by_cat[cat]:
                        w_prob = self.bows_by_cat[cat][w]
                        prob += math.log(w_prob)
                    else:
                        w_prob = self.default_bows[cat]
                        prob += math.log(w_prob)

            # append the final probability to the list
            probs.append(prob)
        ind_max = probs.index(max(probs))
        return probs, ind_max


    def test(self, dataset, labels, tf_idf=False):

        """
        NaiveBayes List List Boolean -> List Int

        Makes a prediction for each element of the dataset, and returns the list
        of the predictions, and the accuracy

        """
        correct = 0
        predictions = []

        # infer for every article
        for i, text in enumerate(dataset):
            cat = self.infer(text, tf_idf)
            predictions.append(cat)

            if cat == labels[i]:
                correct += 1

        # calculate accuracy
        accuracy = correct/len(dataset)

        return predictions, accuracy

        




if __name__ == "__main__":
    one = "love love love cake love cake love cake." # love 5 cake 3
    two = "summer love summer love summer love" # summer 3 love 3
    thr = "day summer summer day summer love" # summer 3 day 2 love 1
    # total: love 9 summer 6 cake 3 day 2

    fou = "hi hi hi bye bye hi hi hi" # hi 5 bye 2
    fiv = "love love love hi" # love 3 hi 2
    six = "cake good good bad bad hi" # hi 1 cake 1 good 2 bad 2
    # total hi 8 bye 2 love 3 good 2 bad 2 cake 1

    training_set = [one, two, thr, fou, fiv, six]
    training_lab = [0, 0, 0, 1, 1, 1]

    nb = NaiveBayes(2)

    nb.train(training_set, training_lab)

    for cat in nb.class_counters:
        for w, val in nb.class_counters[cat].items():
            print(w, val, nb.class_bows[cat][w], nb.doc_counter[w], nb.idf_scores[w], nb.class_tf_idf[cat][w])

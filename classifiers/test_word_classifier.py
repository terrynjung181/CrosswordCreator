import pickle
import os
from sklearn.datasets import fetch_20newsgroups
from naive_bayes import NaiveBayes



def test_nb(filename, test_data, test_labels):

    with open(os.path.join("trained_models", filename), "rb") as f:
        nb = pickle.load(f)
    predictions, accuracy = nb.test(test_data, test_labels, True)

    print(predictions)
    print(accuracy)
    return predictions, accuracy


test_data = ["1. Of or pertaining to a republic. The Roman emperors were republican magistrates \
    named by the senate. Macaulay. 2. Consonant with the principles of a republic; as, republican \
    sentiments or opinions; republican manners. Republican party. (U.S. Politics) (a) An earlier \
        name of the Democratic party when it was opposed to the Federal party. Thomas Jefferson \
            was its great leader. (b) One of the existing great parties. It was organized in \
                1856 by a combination of voters from other parties for the purpose of opposing \
                    the extension of slavery, and in 1860 it elected Abraham Lincoln president.\
                        \n\n1. One who favors or prefers a republican form of government. \
                        2. (U.S.Politics)  A member of the Republican party. 3. (Zoöl.) (a) \
                            The American cliff swallow. The cliff swallows build their nests side \
                                by side, many together. (b) A South African weaver bird (Philetærus \
                                    socius). These weaver birds build many nests together, under a \
                                        large rooflike shelter, which they make of straw. \
                                            Red republican. See under Red.", "God", "cars toyata honda civic"]

test_label = [4, 1, 2]
test_nb("trained_nb.pkl", test_data, test_label)

#['comp.windows.x', 'rec.autos', 'rec.sport.baseball', 'sci.space', 'talk.politics.misc', 'talk.religion.misc']
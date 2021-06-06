# Installation

To install required libraries, run the following command in a terminal shell:
pip install -r requirements.txt

(If you have pip3, replace pip with pip3)

This will be all that is needed to run the full crossword puzzle. If you want to do more analysis
with the naive-bayes classifier, open terminal and enter "python" or "python3" (depending on your
installation) to enter a python shell. Once inside, enter the following commands:

import nltk

nltk.download('stopwords')

Everything else should work as is.


# Running
To run the GUI, simply enter "python main.py" or "python3 main.py" (depending on pythong installation) and the crossword GUI will appear.

To see timed performances, enter "python time_tests.py" or "python3 time_tests.py"; this will assess the average time it takes to solve a full 3x3 crossword layout (over 5 trials) for any particular heuristic combination.

Files related to theme classification of words are in the "theme_classifier" folder; files relating to crossword solving are in the "layout_solver" folder; the file responsible for clue generation is "clue_maker.py".

Enjoy!

# Research and Findings
You can find our final report about our research and findings here: [Final Report](https://github.com/terrynjung181/CrosswordCreator/blob/main/CS%204701%20Final%20Evaluation%20Written%20Report.pdf)

-- Amit Rajesh, Terryn Jung, and Afnan Arshad

This project contains a sentiment analyzer for IMDB reviews.

To run the analyzer, run the command:
python3 driver_3.py

This will vectorize the data using unigram, bigram, unigram tfidf, and bigram tfidf models
and run stochastic gradient descent in order to train a sentiment analyzer on the IMDB
review data.

The results of the trained model run on test IMDB reviews for each text representation model
will be output in text files.

The combined data with stopwords and punctuation removed will also be output in a csv file.

#!/usr/bin/python
import numpy as np
from scipy.sparse import csr_matrix
import csv
import glob
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import linear_model
import string

train_path = "./aclImdb/train/" # source data
test_path = "./imdb_te.csv" # test data for grade evaluation 
stopFile_path = "./stopwords.en.txt"

'''Implement this module to extract
and combine text files under train_path directory into 
imdb_tr.csv. Each text file in train_path should be stored 
as a row in imdb_tr.csv. And imdb_tr.csv should have three 
columns, "row_number", "text" and label'''

def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    #Write header to file
    csvfile = open(outpath + name, 'w', encoding = 'utf-8')
    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(["row_number", "text", "polarity"])
    #Write texts to file
    categories = ["neg", "pos"]
    rowNumber = 0
    categoryNum = 0

    #Get stop words
    stopFile = open(stopFile_path, 'r')
    stopWords = set()
    for stopWord in stopFile:
        stopWords.add(stopWord)

    for category in categories:
        files = glob.glob(inpath + category + "/*.txt")
        for item in files:
            reader = open(item, 'r', encoding = 'utf-8')
            csvWriter.writerow([rowNumber, cleanStopWords(reader.read(), stopWords), categoryNum])
            rowNumber += 1
        categoryNum += 1

def cleanStopWords(text, stopwordSet):
    result = []
    removePunc = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    cleanedText = text.translate(removePunc).lower()
    for word in cleanedText.split():
        if word not in stopwordSet:
            result.append(word)
    return " ".join(result)

def testVectors(counts, labels, testCounts, outputName):
    clf = linear_model.SGDClassifier(loss='hinge',  penalty='l1')
    clf.fit(counts, labels)
    testResults = clf.predict(testCounts)

    #Write results to file
    outputFile = open(outputName, 'w')
    for result in testResults:
        outputFile.write(str(result) + "\n")

'''train a SGD classifier using unigram representation,
predict sentiments on imdb_te.csv, and write output to
unigram.output.txt'''
    
'''train a SGD classifier using bigram representation,
predict sentiments on imdb_te.csv, and write output to
unigram.output.txt'''
     
'''train a SGD classifier using unigram representation
with tf-idf, predict sentiments on imdb_te.csv, and write 
output to unigram.output.txt'''
    
'''train a SGD classifier using bigram representation
with tf-idf, predict sentiments on imdb_te.csv, and write 
output to unigram.output.txt'''
  
if __name__ == "__main__":
    imdb_data_preprocess(train_path)
    #Prepare training data
    textData = []
    dataLabels = []

    categories = ["neg", "pos"]
    categoryNum = 0

    for category in categories:
        files = glob.glob(train_path + category + "/*.txt")
        for item in files:
            reader = open(item, 'r', encoding="ISO-8859-1")
            textData.append(reader.read())
            dataLabels.append(categoryNum)
        categoryNum += 1

    unigramVectorizer = CountVectorizer(stop_words = 'english', 
        ngram_range = (1,1), 
        min_df=1)
    bigramVectorizer = CountVectorizer(stop_words = 'english', 
        ngram_range = (2,2))

    unigramCounts = unigramVectorizer.fit_transform(textData)
    unigramVocab = unigramVectorizer.vocabulary_
    bigramCounts = bigramVectorizer.fit_transform(textData)
    bigramVocab = bigramVectorizer.vocabulary_

    unigramTransformer = TfidfTransformer()
    bigramTransformer = TfidfTransformer()
    unigramTfidf = unigramTransformer.fit_transform(unigramCounts)
    bigramTfidf = bigramTransformer.fit_transform(bigramCounts)

    #Testing
    #Prepare testing data
    testingData = []
    csvfile = open(test_path, 'r', encoding="ISO-8859-1", newline='')
    next(csvfile)
    csvReader = csv.reader(csvfile)
    for row in csvReader:
        testingData.append(row[1])

    #Vectorize testing data
    unigramTestVectorizer = CountVectorizer(stop_words='english', 
        ngram_range=(1,1), 
        vocabulary=unigramVocab)
    bigramTestVectorizer = CountVectorizer(stop_words='english', 
        ngram_range=(2,2), 
        vocabulary=bigramVocab)

    unigramTest = unigramTestVectorizer.fit_transform(testingData)
    bigramTest = bigramTestVectorizer.fit_transform(testingData)

    unigramTestTransformer = TfidfTransformer()
    bigramTestTransformer = TfidfTransformer()

    unigramTfidfTest = unigramTestTransformer.fit_transform(unigramTest)
    bigramTfidfTest = bigramTestTransformer.fit_transform(bigramTest)

    #Test unigram
    testVectors(unigramCounts, dataLabels, unigramTest, "unigram.output.txt")
    #Test bigram
    testVectors(bigramCounts, dataLabels, bigramTest, "bigram.output.txt")
    #Test unigram tfidf
    testVectors(unigramTfidf, dataLabels, unigramTfidfTest, "unigramtfidf.output.txt")
    #Test bigram tfidf
    testVectors(bigramTfidf, dataLabels, bigramTfidfTest, "bigramtfidf.output.txt")










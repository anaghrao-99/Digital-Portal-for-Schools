import pandas as pd
import numpy as np
import scipy
import math
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import nltk


import csv
import gensim

from gensim.models import Word2Vec
from gensim.scripts.glove2word2vec import glove2word2vec
import tensorflow_hub as hub

STOP = set(nltk.corpus.stopwords.words("english"))


def load_sts_dataset(filename):
    # Loads a subset of the STS dataset into a DataFrame. In particular both
    # sentences and their human rated similarity score.
    sent_pairs = []
    with tf.gfile.GFile(filename, "r") as f:
        for line in f:
            ts = line.strip().split("\t")
            sent_pairs.append((ts[5], ts[6], float(ts[4])))
    return pd.DataFrame(sent_pairs, columns=["sent_1", "sent_2", "sim"])


def download_and_load_sts_data():
    sts_dataset = tf.keras.utils.get_file(
        fname="Stsbenchmark.tar.gz",
        origin="http://ixa2.si.ehu.es/stswiki/images/4/48/Stsbenchmark.tar.gz",
        extract=True)

    sts_dev = load_sts_dataset(os.path.join(os.path.dirname(sts_dataset), "stsbenchmark", "sts-dev.csv"))
    sts_test = load_sts_dataset(os.path.join(os.path.dirname(sts_dataset), "stsbenchmark", "sts-test.csv"))

    return sts_dev, sts_test





def download_sick(f): 

    response = requests.get(f).text

    lines = response.split("\n")[1:]
    lines = [l.split("\t") for l in lines if len(l) > 0]
    lines = [l for l in lines if len(l) == 5]

    df = pd.DataFrame(lines, columns=["idx", "sent_1", "sent_2", "sim", "label"])
    df['sim'] = pd.to_numeric(df['sim'])
    return df
    





class Sentence:
    
    def __init__(self, sentence):
        self.raw = sentence
        normalized_sentence = sentence.replace("‘", "'").replace("’", "'")
        self.tokens = [t.lower() for t in nltk.word_tokenize(normalized_sentence)]
        self.tokens_without_stop = [t for t in self.tokens if t not in STOP]




def read_tsv(f):
    frequencies = {}
    with open(f) as tsv:
        tsv_reader = csv.reader(tsv, delimiter="\t")
        for row in tsv_reader: 
            frequencies[row[0]] = int(row[1])
        
    return frequencies
        

def run_gse_benchmark(sentences1, sentences2):
    sts_input1 = tf.placeholder(tf.string, shape=(None))
    sts_input2 = tf.placeholder(tf.string, shape=(None))

    sts_encode1 = tf.nn.l2_normalize(embed(sts_input1))
    sts_encode2 = tf.nn.l2_normalize(embed(sts_input2))
        
    sim_scores = tf.reduce_sum(tf.multiply(sts_encode1, sts_encode2), axis=1)
    
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        session.run(tf.tables_initializer())
      
        [gse_sims] = session.run(
            [sim_scores],
            feed_dict={
                sts_input1: [sent1.raw for sent1 in sentences1],
                sts_input2: [sent2.raw for sent2 in sentences2]
            })
    return gse_sims


def main():
    # sts_dev, sts_test = download_and_load_sts_data()
    # sick_train = download_sick("https://raw.githubusercontent.com/alvations/stasis/master/SICK-data/SICK_train.txt")
    # sick_dev = download_sick("https://raw.githubusercontent.com/alvations/stasis/master/SICK-data/SICK_trial.txt")
    # sick_test = download_sick("https://raw.githubusercontent.com/alvations/stasis/master/SICK-data/SICK_test_annotated.txt")
    # sick_all = sick_train.append(sick_test).append(sick_dev)

    # PATH_TO_WORD2VEC = os.path.expanduser("D:\\sem8\\project\\nlp-notebooks-master\\data\\word2vec\\GoogleNews-vectors-negative300.bin")
    # PATH_TO_GLOVE = os.path.expanduser("D:\\sem8\\project\\nlp-notebooks-master\\data\\glove\\glove.840B.300d.txt")

    # word2vec = gensim.models.KeyedVectors.load_word2vec_format(PATH_TO_WORD2VEC, binary=True)

    # tmp_file = "D:\\sem8\\project\\nlp-notebooks-master\\tmp\\glove.840B.300d.w2v.txt"
    # glove2word2vec(PATH_TO_GLOVE, tmp_file)
    # glove = gensim.models.KeyedVectors.load_word2vec_format(tmp_file)



    # PATH_TO_FREQUENCIES_FILE = "D:\\sem8\\project\\nlp-notebooks-master\\data\\sentence_similarity\\frequencies.tsv"
    # PATH_TO_DOC_FREQUENCIES_FILE = "D:\\sem8\\project\\nlp-notebooks-master\\data\\sentence_similarity\\doc_frequencies.tsv"

    # frequencies = read_tsv(PATH_TO_FREQUENCIES_FILE)
    # doc_frequencies = read_tsv(PATH_TO_DOC_FREQUENCIES_FILE)
    # doc_frequencies["NUM_DOCS"] = 1288431

    tf.logging.set_verbosity(tf.logging.ERROR)
    embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/1")

if __name__ == '__main__':
    # print(tf.__version__)
    main()
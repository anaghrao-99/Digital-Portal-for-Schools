from absl import logging

import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
module_url = "/Users/anagh/Desktop/Digital-Portal-for-Schools/automated_correction_module/module5"  
#module_url = "./module5"
embed = hub.KerasLayer(module_url)
print("module loaded")


logging.set_verbosity(logging.ERROR)

def plot_similarity(labels, features, rotation):
  corr = np.inner(features, features)
  sns.set(font_scale=1.2)
  g = sns.heatmap(
      corr,
      xticklabels=labels,
      yticklabels=labels,
      vmin=0,
      vmax=1,
      cmap="YlOrRd")
  g.set_xticklabels(labels, rotation=rotation)
  g.set_title("Semantic Textual Similarity")
  return corr[0][1]


def run_and_plot(session_, input_tensor_, messages_, encoding_tensor):
  message_embeddings_ = session_.run(
      encoding_tensor, feed_dict={input_tensor_: messages_})
  return plot_similarity(messages_, message_embeddings_, 90)

def find_sim(messages):
    similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
    similarity_message_encodings = embed(similarity_input_placeholder)
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        session.run(tf.tables_initializer())
        return run_and_plot(session, similarity_input_placeholder, messages,
                    similarity_message_encodings)



if __name__ == '__main__':

  f = open("recognized.txt", "r")
  sent1 = f.read()
  print(sent1)

  f2 = open("answer_key.txt", "r")
  sent2 = f2.read()
  print(sent2)

  
  messages = [sent1,sent2]
  print(find_sim(messages))
  

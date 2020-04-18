from absl import logging

import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import sys
# module_url = "/Users/anagh/Desktop/Digital-Portal-for-Schools/automated_correction_module/module5"  
# module_url = "D:/sem8/module5"
module_url = "/users/anagh/Desktop/module5"
embed = hub.KerasLayer(module_url)
print("module loaded")


logging.set_verbosity(logging.ERROR)

def plot_similarity(labels, features, rotation):
  corr = np.inner(features, features)
  sns.set(font_scale=1.2)
  # g = sns.heatmap(
  #     corr,
  #     xticklabels=labels,
  #     yticklabels=labels,
  #     vmin=0,
  #     vmax=1,
  #     cmap="YlOrRd")
  # g.set_xticklabels(labels, rotation=rotation)
  # g.set_title("Semantic Textual Similarity")
  return corr


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

 
  answer_key_location = sys.argv[2]
  answer_key = open(answer_key_location, "r")
  answer_sent = answer_key.read()

  files = sys.argv[1]
  

  print(files)
  files = files[1:len(files)-1]
  file_names = files.split(',')

  messages = [answer_sent]

  for i in range(len(file_names)):
    f = open(file_names[i], 'r')
    sent = f.read()

    messages.append(sent)

  # print(messages)
  # messages = [sent1,sent2]
  print(find_sim(messages))
  
  


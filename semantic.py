from absl import logging

import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
module_url = "./module5"   #"https://tfhub.dev/google/universal-sentence-encoder/2" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]
# Import the Universal Sentence Encoder's TF Hub module
embed = hub.KerasLayer(module_url)
print("module loaded")

# Compute a representation for each message, showing various lengths supported.
# word = "Elephant"
# sentence = "I am a sentence for which I would like to get its embedding."
# paragraph = (
#     "Universal Sentence Encoder embeddings also support short paragraphs. "
#     "There is no hard limit on how long the paragraph is. Roughly, the longer "
#     "the more 'diluted' the embedding will be.")
# messages = [word, sentence, paragraph]

# Reduce logging output.
logging.set_verbosity(logging.ERROR)

# with tf.Session() as session:
#     session.run([tf.global_variables_initializer(), tf.tables_initializer()])
#     message_embeddings = session.run(embed(messages))

#     for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
#         print("Message: {}".format(messages[i]))
#         print("Embedding size: {}".format(len(message_embedding)))
#         message_embedding_snippet = ", ".join(
#             (str(x) for x in message_embedding[:3]))
#         print("Embedding: [{}, ...]\n".format(message_embedding_snippet))

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
    flag = True
    while(flag):
        sent1 = input("Enter sentence 1:")
        sent2 = input("Enter sentence 2:")
        messages = [sent1,sent2]
        print(find_sim(messages))
        while(1):
            choise = input("Do you want to continue?Y or N :")
            if(choise == "Y"):
                break
            elif(choise == "N"):
                flag = False
                break
            else:
                print("Incorrect Choice")
                continue
        



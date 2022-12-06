from contextualized_topic_models.models.kitty_classifier import Kitty
from nltk.corpus import stopwords

from pyspark.sql import SparkSession
import numpy as np
import json

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# nltk.download("stopwords")


from subset import get_data_sample

def main() -> None:
    spark = SparkSession.builder.appName("CombinedTM").getOrCreate()

    TOPICS_NUM=30

    ids, abstracts = get_data_sample(spark)

    docs = [doc.strip() for doc in abstracts]

    stop_words = set(stopwords.words('english'))

    kt = Kitty()
    kt.train(docs, topics=TOPICS_NUM, embedding_model="allenai/scibert_scivocab_uncased", stopwords_list=list(stop_words), epochs=10)

    print("Model fitted...")

    print("Current topics are (printing 10 for each cluster):")

    for i in range(TOPICS_NUM):
        print('i: ', *kt.get_word_classes(10)[i])

    print('These topics will be saved in file "topics.json".')

    with open("topics.json", 'w') as file:
        json.dump([{'cluster_num': i, 'topics': kt.get_word_classes(10)[i]} for i in range(TOPICS_NUM)], file)

    print("Please fill theme names in 'assigned_classes.json' file in format {cluster_num (int): theme (str)} and provide the path to model.")

    print("Saving the model...")

    kt.save("kitty.pkl") # saves the model in a pkl file

    print("Model saved.")



if __name__ == "__main__":
    main()
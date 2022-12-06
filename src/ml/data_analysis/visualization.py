from typing import Tuple, Callable, List, Dict
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pandas.core.series import Series
from data_processing import stopwords_list, tokenize_and_lemmatize

from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import seaborn as sns


def draw_word_cloud(
    abstracts: Series,
    ngram_range: Tuple[int, int] = (1, 1),
    max_features: int = 100,
    tokenizer: Callable = tokenize_and_lemmatize,
    stop_words: List[str] = stopwords_list,
    max_words: int = 1500
) -> None:
    tf_idf_vectorizer = TfidfVectorizer(
        analyzer="word",
        max_df=0.9,
        min_df=0.005,
        use_idf=True,
        smooth_idf=True,
        tokenizer=tokenizer,
        max_features=max_features,
        ngram_range=ngram_range,
        stop_words=stop_words
    )
    tf_idf_matrix = tf_idf_vectorizer.fit_transform(abstracts)

    df = pd.DataFrame(tf_idf_matrix.todense().tolist(),
                      columns=tf_idf_vectorizer.get_feature_names())

    wordcloud = WordCloud(
        mode="RGBA",
        background_color=None,
        width=1024,
        height=768,
        max_words=max_words,
        relative_scaling=1,
        normalize_plurals=False
    ).generate_from_frequencies(df.T.sum(axis=1))

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def draw_hbar(data: Dict[str, float], x_name: str) -> None:
    x, y = zip(*data.items())
    sns.set(rc={'figure.figsize': (11.7, 8.27)})

    sns.set_palette(["#5975a4"], n_colors=100)
    df__ = pd.DataFrame({'name': x, x_name: np.around(y, 2)}
                        ).sort_values(x_name, ascending=False)
    ax = sns.barplot(y='name', x=x_name, data=df__, orient='h')
    ax.bar_label(ax.containers[0])
    plt.show()

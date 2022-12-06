import random
import operator
from collections import Counter

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode


ADDITIVE_COMPONENT_COUNT = 1000
SOURCE_PATH = "results/fin_dataset.parquet"
TRAIN_DATA_PATH = "results/splited_data/train.parquet"
TEST_DATA_PATH = "results/splited_data/test.parquet"


def find_groups(n, adjacency_list):
    visited = [False] * n
    groups = [None] * n
    color = 0

    for i in range(n):
        if visited[i]:
            continue

        color += 1
        visited[i] = True
        groups[i] = color
        queue = [(i, color)]
        while queue:
            v, group = queue.pop()
            for to in adjacency_list[v]:
                if not visited[to]:
                    visited[to] = True
                    groups[to] = group
                    queue.append((to, group))

    return color, groups


def get_authors_links(data):
    data = data.filter('old_id is not NULL')\
        .withColumn('a_old_id', col('authors.old_id'))\
        .select(col('old_id'), explode(col('a_old_id')).alias('author'))

    data_2 = data.withColumn('author_2', col('author')).drop(col('author'))\
        .withColumn('old_id_2', col('old_id')).drop(col('old_id'))

    data = data.join(data_2, ((data['old_id'] == data_2['old_id_2'])
                              & (data['author'] > data_2['author_2'])
                              ), 'inner').drop(col('old_id_2'))

    data = data.filter(data['author'] != data['author_2'])\
        .filter('author is not NULL')\
        .filter('author_2 is not NULL')

    return data.toPandas()


def author_papers_information(authors_source_links):
    authors_to_id = {}
    author_papers = {}
    id_to_authors = {}
    links = set()

    current_author_id = 0
    for i in range(len(authors_source_links)):
        link = authors_source_links.iloc[i]

        if link['author'] in authors_to_id:
            author_l = authors_to_id[link['author']]
        else:
            authors_to_id[link['author']] = current_author_id
            author_l = current_author_id
            id_to_authors[current_author_id] = link['author']
            current_author_id += 1

        if link['author_2'] in authors_to_id:
            author_r = authors_to_id[link['author_2']]
        else:
            authors_to_id[link['author_2']] = current_author_id
            author_r = current_author_id
            id_to_authors[current_author_id] = link['author_2']
            current_author_id += 1

        links.add((author_l, author_r))

        if link['author'] not in author_papers:
            author_papers[link['author']] = []
        author_papers[link['author']].append(link['old_id'])

        if link['author_2'] not in author_papers:
            author_papers[link['author_2']] = []
        author_papers[link['author_2']].append(link['old_id'])

    return authors_to_id, links, author_papers, id_to_authors


def get_adjacency_list(authors_to_id, links):
    n, m = len(authors_to_id), len(links)
    adjacency_list = [[] for _ in range(n)]

    for link in links:
        v, u = link[0], link[1]
        adjacency_list[v].append(u)
        adjacency_list[u].append(v)

    return adjacency_list


def get_train_components(additive_component_count, component_numbers):
    cnt = Counter(component_numbers)
    cnt = sorted(cnt.items(), key=operator.itemgetter(1), reverse=True)
    print("Top30 components with count: ")
    print(cnt[:30])

    top_n_for_random = min(len(cnt) - 1, additive_component_count * 3)
    possible_indexes = list(range(1, top_n_for_random, 1))

    ids_in_cnt = [0]
    random.seed(42)
    ids_in_cnt.extend(sorted(random.sample(possible_indexes, additive_component_count)))

    train_component_ids = [cnt[x][0] for x in ids_in_cnt]
    print(f"Components for train: {train_component_ids}")

    return train_component_ids


def get_train_test_papers_ids(additive_component_count, author_papers, id_to_authors, component_numbers):
    train_component_ids = get_train_components(additive_component_count, component_numbers)

    train_papers_ids = set()
    test_papers_ids = set()
    for author_id in range(len(component_numbers)):
        if component_numbers[author_id] in train_component_ids:
            train_papers_ids.update(author_papers[id_to_authors[author_id]])
        else:
            test_papers_ids.update(author_papers[id_to_authors[author_id]])

    train_ids_df = pd.DataFrame(columns=['old_id'], data=list(train_papers_ids))
    test_ids_df = pd.DataFrame(columns=['old_id'], data=list(test_papers_ids))

    return train_ids_df, test_ids_df


def train_test_split(source_path, additive_component_count):
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("PySpark for dblpv13") \
        .config("spark.driver.memory", "18g") \
        .config("spark.executor.memory", "18g") \
        .config("spark.driver.maxResultSize", "9g") \
        .getOrCreate()
    source_data = spark.read.parquet(source_path)

    authors_source_links = get_authors_links(source_data)

    authors_to_id, links, author_papers, id_to_authors = author_papers_information(authors_source_links)

    adjacency_list = get_adjacency_list(authors_to_id, links)
    k, component_numbers = find_groups(len(authors_to_id), adjacency_list)

    train_ids_df, test_ids_df = get_train_test_papers_ids(additive_component_count,
                                                          author_papers,
                                                          id_to_authors,
                                                          component_numbers)

    print(f'Papers count. Train: {len(train_ids_df)}. Test: {len(test_ids_df)}')

    train_ids_spark_df = spark.createDataFrame(train_ids_df)
    test_ids_spark_df = spark.createDataFrame(test_ids_df)

    source_data = source_data.filter("old_id is not NULL")
    train_data = source_data.join(train_ids_spark_df, on="old_id", how="inner")
    test_data = source_data.join(test_ids_spark_df, on="old_id", how="inner")

    train_data.write.parquet(TRAIN_DATA_PATH)
    test_data.write.parquet(TEST_DATA_PATH)

    print(f"Train path: {TRAIN_DATA_PATH}")
    print(f"Test path: {TEST_DATA_PATH}")
    print("Splitted data are written")


if __name__ == "__main__":
    train_test_split(SOURCE_PATH, ADDITIVE_COMPONENT_COUNT)

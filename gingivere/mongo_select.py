from pymongo import MongoClient
import json
import ast
from random import randint, shuffle
import numpy as np
import pandas as pd
import copy

def add_int_to_collection(posts, query):
    cursor = posts.find(query)
    for i, doc in enumerate(cursor):
        doc['int_id'] = i
        posts.save(doc)
    cursor.close()

def get_all_preictals(posts):
    return posts.find(PREICTAL_QUERY)

def get_all_interictals(posts):
    return posts.find(INTERICTAL_QUERY)

def find_random_docs(posts, query, num):
    n = posts.find(query).count()
    rs = [randint(0,n-1) for i in range(num)]
    query['int_id'] = {'$in' : rs}
    rand_eles = posts.find(query)
    return rand_eles

#doesn't work
def load_name_to_post_id(path):
    with open(path) as f:
        st = f.read()
        name_to_post_id = ast.literal_eval(st[1:-1])
    return name_to_post_id

def import_vectors(query, limit=None):
    if limit:
        my_cursor = db.inventory.find(query, limit)
    else:
        my_cursor = db.inventory.find(query)
    return my_cursor

def load_random_training_set(posts, num=500):
    preictal_results = find_random_docs(posts, PREICTAL_QUERY, num)
    interictal_results = find_random_docs(posts, INTERICTAL_QUERY, num)
    preictal_df = pd.DataFrame.from_dict(preictal_results)
    interictal_df = pd.DataFrame.from_dict(interictal_results)
    return preictal_df, interictal_df

    # preictal_X = [i['data'] for i in preictal_results]
    # interictal_X = [i['data'] for i in interictal_results]
    # preictal_y = [1 for i in preictal_results]
    # interictal_y = [0 for i in interictal_results]
    # preictal_names =
    # preictal_names =
    # combined = zip(preictal_X+interictal_X, preictal_y + interictal_y)
    # random.shuffle(combined)
    # shuffled_X, shuffled_Y =




def main():
    # name_to_post_id = load_name_to_post_id("posts.json")
    pass

INTERICTAL_QUERY = {}
INTERICTAL_QUERY['state'] = 'interictal'
PREICTAL_QUERY = {}
PREICTAL_QUERY['state'] = 'preictal'

if __name__ == "__main__":
    client = MongoClient()
    db = client['gingivere']
    posts = db.posts
    # print(posts.find_one())
    # interictal = {}
    # interictal['state'] = 'interictal'
    # # print(posts.find(interictal).count())
    # # results = find_random_docs(posts, interictal, 50)
    # # print(len(results))
    # preictal_df, interictal_df = load_random_training_set(posts)
    add_int_to_collection(posts, INTERICTAL_QUERY)
    add_int_to_collection(posts, PREICTAL_QUERY)

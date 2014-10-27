from pymongo import MongoClient
import shelve_api
import load_raw_data
import copy
import json
import shelve
import pandas as pd
import collections

def insert_patient(patient):
    name_to_post_id = {}
    client = MongoClient()
    db = client['gingivere']
    posts = db[patient]

    d = collections.defaultdict(list)

    for data in load_raw_data.walk_training_mats(patient):
        post_item = copy.deepcopy(data)
        del post_item['data']
        for i, item in enumerate(data['data']):
            post_item['data'] = item.tolist()
            name = "%02d_%s" % (i, data['file'])
            post_id = posts.insert(post_item)
            d['name'].append(name)
            d['_id'].append(str(post_id))
            d['state'].append(post_item['state'])
            print("Just posted: " + name)
            del post_item['_id']

    df = pd.DataFrame(d)
    shelve_api.insert(df)

if __name__ == "__main__":
    insert_patient('Dog_2')
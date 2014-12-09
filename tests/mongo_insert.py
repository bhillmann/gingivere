import copy
import collections

import pandas as pd

from pymongo import MongoClient
import load_raw_data
from tests import shelve_api


def insert_patient(patient):
    name_to_post_id = {}
    client = MongoClient()
    db = client['gingivere']
    collection = db[patient]

    d = collections.defaultdict(list)

    for data in load_raw_data.walk_training_mats(patient):
        post_item = copy.deepcopy(data)
        channels = post_item['channels']
        del post_item['data']
        del post_item['channels']
        for i, item in enumerate(data['data']):
            post_item['data'] = item.tolist()
            post_item['channel'] = channels[i]
            name = "%02d_%s" % (i, data['file'])
            post_id = collection.insert(post_item)
            d['name'].append(name)
            d['_id'].append(str(post_id))
            d['state'].append(post_item['state'])
            d['channel'].append(channels[i])
            print("Just posted: " + name)
            del post_item['_id']

    df = pd.DataFrame(d)
    shelve_api.insert(df, "labeled_" + patient)

if __name__ == "__main__":
    insert_patient('Dog_1')

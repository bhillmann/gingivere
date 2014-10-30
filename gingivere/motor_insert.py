from __future__ import print_function

import load_raw_data
from collections import defaultdict

import pandas as pd
import shelve_api

import tornado.ioloop
from tornado import gen
import motor
import copy

def insert_patient(patient):
    count = 0
    for data in load_raw_data.walk_training_mats(patient):
        insert_item = copy.deepcopy(data)
        channels = insert_item['channels']
        del insert_item['data']
        del insert_item['channels']
        for i, item in enumerate(data['data']):
            print(channels)
            insert_item['channel'] = channels[i]
            insert_item['_id'] = count
            count += 1
            yield insert_item

def shelve(result, error):
    if error:
        print('error getting user!', error)
    else:
        name = "%02d_%s" % (i, result['file'])
        d['name'].append(name)
        d['_id'].append(result['_id'])
        d['state'].append(result['state'])
        d['channel'].append(result['channel'])
        print("Just posted: " + name)


@gen.coroutine
def bulk_write():
    global d
    d = defaultdict(list)
    collection.insert((i for i in insert_patient('Dog_2')), callback=shelve)


if __name__ == "__main__":
    client = motor.MotorClient()
    db = motor.MotorDatabase(client, 'gingivere')
    collection = motor.MotorCollection(db, 'Dog_1')
    tornado.ioloop.IOLoop.current().run_sync(bulk_write)
    df = pd.DataFrame(d)
    shelve_api.insert(df, 'test_dog_1')

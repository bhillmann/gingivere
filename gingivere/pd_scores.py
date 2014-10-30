from __future__ import print_function

import pandas as pd

import raw_data_clf
import mongo_select
import shelve_api
import numpy as np

from collections import defaultdict

print("Training the CLF")
clf = raw_data_clf.RawClf('Dog_2')
clf.clear_data()

print()
print("Cleared the data")
print()

d = defaultdict(list)

for item in mongo_select.get_all('Dog_2'):
    data = np.array(item['data']).astype('float32')
    prediction = clf.predict(data)
    d['pred'].append(prediction)
    del item['data']
    for key in item:
        d[key].append(item[key])
    print("Just predicted %s for %s" % (prediction[0], item['file']))


shelve_api.insert(d, 'preds')
# print("Just scored %d" % s/count)

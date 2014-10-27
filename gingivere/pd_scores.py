from __future__ import print_function

import pandas as pd

import raw_data_clf
import mongo_select

from collections import defaultdict

print("Training the CLF")
clf = raw_data_clf.RawClf('dog_2')
clf.clear_data()

print()
print("Cleared the data")
print()

d = defaultdict(list)

for item in mongo_select.get_all():
    data = item['data']
    prediction = clf.predict(data)
    d['pred'].append(prediction)
    del item['data']
    for key in item:
        d[key].append()
    print("Just predicted %d for %n" % (prediciton, item['name']))

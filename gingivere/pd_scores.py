from __future__ import print_function

import pandas as pd

import raw_data_clf
import mongo_select
import shelve_api

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
    prediction = clf.predict_proba(data)
    d['pred'].append(prediction[0])
    del item['data']
    for key in item:
        d[key].append(item[key])
    print("Just predicted %s for %s" % (prediction[0], item['file']))


shelve_api.insert(d, 'proba_p')
# print("Just scored %d" % s/count)

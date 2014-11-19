import pandas as pd
from sklearn.cross_validation import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
import random
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

import shelve_api

def yield_patient_names(name, d):
    for key in d:
        if name in key:
            yield key

new_d = {}
d = shelve_api.load('baseline')
for key in yield_patient_names('Dog_1', d):
    new_d[key] = d[key]
for key in yield_patient_names('Dog_2', d):
    new_d[key] = d[key]
for key in yield_patient_names('Dog_3', d):
    new_d[key] = d[key]
for key in yield_patient_names('Dog_4', d):
    new_d[key] = d[key]
# for key in yield_patient_names('Dog_5', d):
#     new_d[key] = d[key]


# store = pd.HDFStore("D:/gingivere/data.h5")
# data = store['baseline']
# store.close()

# mask = ['Dog_4' in name for name in data]
# df_all = data.loc[:,mask]

df_all = pd.DataFrame(new_d)

X = []
y = []
num_preictals = sum([1 if 'preictal' in name else 0 for name in df_all])
ix = random.sample(range(len(df_all.T)-num_preictals), num_preictals)

for i, label in enumerate(df_all):
    if 'interictal' in label:
        print(i, label)
        y.append(0)
        X.append(df_all[label][:-2])
    elif 'preictal' in label:
        for j in range(9):
            y.append(1)
            X.append(df_all[label][:-2])
    else:
        # print("whoops")
        continue




y = np.array(y)

X = np.array(X)

clf = KNeighborsClassifier(n_neighbors=11)
# clf = RandomForestClassifier(n_estimators=20)
# clf = SVC(gamma=0.001, kernel='rbf', C=100)

skf = StratifiedKFold(y, n_folds=2)
for train_index, test_index in skf:
    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    clf.fit(X_train, y_train)
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))
    print()
    print(roc_auc_score(y_true, y_pred))
    print()

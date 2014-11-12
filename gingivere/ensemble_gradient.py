import pandas as pd
from sklearn.cross_validation import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
import random
from sklearn.svm import SVC



store = pd.HDFStore("D:/gingivere/data.h5")
data = store['baseline']
store.close()

mask = ['Dog_4' in name for name in data]
df_all = data.loc[:,mask]

X = []
y = []
num_preictals = sum([1 if 'preictal' in name else 0 for name in df_all])
ix = random.sample(range(len(df_all.T)-num_preictals), num_preictals)

for i, label in enumerate(df_all):
    if 'interictal' in label and i in ix:
        print(i, label)
        y.append(0)
        X.append(df_all[label])
    elif 'preictal' in label:
        y.append(1)
        X.append(df_all[label])
    else:
        # print("whoops")
        continue




y = np.array(y)

X = df_all.T.values

clf = SVC(C=100, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.001, kernel='rbf', max_iter=-1, random_state=None, shrinking=True, tol=0.001, verbose=False)

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

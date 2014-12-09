import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import StratifiedKFold
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score


store = pd.HDFStore("D:/gingivere/data.h5")
df = store['master']

X = []
y = []

for name in df.file:
    if 'Dog_1' in name and not 'test' in name:
        print(name)
        name = name.split('.')[0]
        data = store[name]
        data = data.astype('float64')
        data = preprocessing.scale(data)
        for row in data:
            X = X + np.array_split(row, 6)
        if 'interictal' in name:
            y = y + [0]*6
        elif 'preictal' in name:
            y = y + [1]*6

store.close()
X = np.asarray(X)
r = (X.min(), X.max())
xx = []
for x in X:

    xx.append(np.histogram(x, density=True, range=r)[0])

    print(xx[-1])
X = np.asarray(xx)
y = np.asarray(y)

# clf = LinearRegression()
clf = RandomForestClassifier(n_estimators=20)
# clf = SVC(gamma=0.001, kernel='rbf', C=100)

skf = StratifiedKFold(y, n_folds=2)
for train_index, test_index in skf:
    print("Detailed classification report:")
    print()
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    clf.fit(X_train, y_train)
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(np.around(y_true), np.around(y_pred)))
    print()
    print(roc_auc_score(y_true, y_pred))
    print()

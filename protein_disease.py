from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import csv,numpy as np,pandas as pd
import os

data = pd.read_csv(os.path.join("protein_disease.csv"))
df = pd.DataFrame(data)
cols = df.columns
cols = cols[:-1]
X = df[cols]
y = df['prognosis']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.02, random_state=0)
gnb = GaussianNB()
clf_gnb = gnb.fit(X_train, y_train)
y_pred=gnb.predict(X_test)

indices = [i for i in range(4377)]
proteins = df.columns.values[:-1]
dictionary = dict(zip(proteins,indices))
# print(accuracy_score(y_test, y_pred)*100)


def dosomething(protein):
    user_input_proteins = protein
    user_input_label = [0 for i in range(4377)]
    for i in user_input_proteins:
        idx = dictionary[i]
        user_input_label[idx] = idx

    user_input_label = np.array(user_input_label)
    user_input_label = user_input_label.reshape((-1,1)).transpose()
    return(gnb.predict(user_input_label))

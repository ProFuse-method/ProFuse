import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
from datetime import datetime

class NaiveBayesTextModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = GaussianNB()

    def fit(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]

def load_data(csv_file, train=True):
    data = pd.read_csv(csv_file)
    X = data.iloc[:, 1:-1].values
    y = data.iloc[:, -1].values
    return X, y, data.iloc[:, 0].values  

def main():
    # 加载数据
    X_train, y_train, names_train = load_data('../path/train.csv', train=True)
    X_test, y_test, names_test = load_data('../path/test.csv', train=False)

    model = NaiveBayesTextModel()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    results = list(zip(names_test, predictions, y_test))
    results.sort(key=lambda x: x[1], reverse=True)

    with open('baseline_HTVP.csv', 'w') as f:
        f.write("name,prob,Actual\n")
        for rank, (name, prob, label) in enumerate(results, start=1):
            print(f"Rank {rank}: Program {name}, Probability = {prob:.4f}, Label = {int(label)}")
            f.write(f"{name},{prob:.4f},{int(label)}\n")

    df = pd.read_csv('baseline_HTVP.csv')
    df['Original_Index'] = df.index + 1
    bug_indices = df[df['Actual'] == 1]['Original_Index'].tolist()
    n = len(df)
    m = len(bug_indices)
    apfd = 1 - (sum(bug_indices) / (n * m)) + (1 / (2 * n))
    print("APFD Value:", apfd)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Current Time:", current_time)

if __name__ == '__main__':
    main()

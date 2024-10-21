import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('./path/test.csv', header=None)

column_names = ['Feature' + str(i) for i in range(1, len(df.columns))] + ['Label']

df.columns = column_names

features = df.iloc[:, :-1].to_numpy()

shuffled_df = df.iloc[np.random.permutation(df.index)].reset_index(drop=True)

shuffled_df.to_csv('./ramdon_features.csv', index=False)

df = pd.read_csv('./ramdon_features.csv')

df['Original_Index'] = df.index + 1  

bug_indices = df[df['Label'] == 1]['Original_Index'].tolist()  
print("Bug Indices:", bug_indices)

n = len(df)  
m = len(bug_indices)  
apfd = 1 - (sum(bug_indices) / (n * m)) + (1 / (2 * n))
print("APFD Value:", apfd)

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Current Time:", current_time)





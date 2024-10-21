import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('./path/test.csv', header=None)

column_names = ['Feature' + str(i) for i in range(1, len(df.columns))] + ['Label']

df.columns = column_names

features = df.iloc[:, :-1].to_numpy()

selected_indices = [np.random.randint(len(features))]
remaining_indices = list(set(range(len(features))) - set(selected_indices))

while remaining_indices:
    average_distances = np.zeros(len(remaining_indices))
    for idx in selected_indices:

        distances = np.sum(np.abs(features[remaining_indices] - features[idx]), axis=1)
        average_distances += distances
    average_distances /= len(selected_indices)  

    max_distance_index = np.argmax(average_distances)
    next_index = remaining_indices[max_distance_index]
    

    selected_indices.append(next_index)
    remaining_indices.remove(next_index)


print("Selected order of test cases:", selected_indices)


selected_df = df.iloc[selected_indices]
selected_df.to_csv('./TFPS_features.csv', index=False, header=True)

df = pd.read_csv('./TFPS_features.csv')

df['Original_Index'] = df.index + 1  

bug_indices = df[df['Label'] == 1]['Original_Index'].tolist()  
print("Bug Indices:", bug_indices)

n = len(df)  
m = len(bug_indices)  
apfd = 1 - (sum(bug_indices) / (n * m)) + (1 / (2 * n))
print("APFD Value:", apfd)

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Current Time:", current_time)

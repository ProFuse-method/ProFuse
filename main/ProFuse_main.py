import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
import torch.nn.functional as F
import torch.nn as nn
from torch_geometric.nn import GCNConv, global_mean_pool
from torch_geometric.data import Batch


global_scaler = StandardScaler()

class CustomDataset(Dataset):
    def __init__(self, csv_file, graph_folder, train=True):
        data = pd.read_csv(csv_file)
        X = data.iloc[:, 1:-1].values
        y = data.iloc[:, -1].values
        
        if train:
            X = global_scaler.fit_transform(X)
        else:
            X = global_scaler.transform(X)
        
        self.features = torch.tensor(X, dtype=torch.float32)

        epsilon = 0.1
        self.labels = torch.tensor((y * (1 - epsilon) + 0.5 * epsilon), dtype=torch.float32).unsqueeze(1)
        self.names = data.iloc[:, 0].values
        self.graph_folder = graph_folder

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        static_features = self.features[idx]
        graph_file = os.path.join(self.graph_folder, self.names[idx] + '.pt')
        graph_data = torch.load(graph_file)
        label = self.labels[idx]
        name = self.names[idx]
        return static_features, graph_data, label, name

class IntegratedModel(nn.Module):
    def __init__(self, num_node_features, num_static_features):
        super(IntegratedModel, self).__init__()
        self.gcn1 = GCNConv(num_node_features, 16)
        self.gcn2 = GCNConv(16, 16)
        self.fc1 = nn.Linear(num_static_features + 16, 50)
        self.bn1 = nn.BatchNorm1d(50) 
        self.fc2 = nn.Linear(50, 1)

        self.static_weight = nn.Parameter(torch.tensor(0.6))  
        self.graph_weight = nn.Parameter(torch.tensor(0.4))  

    def forward(self, x_static, data_graph):
        x, edge_index, batch = data_graph.x, data_graph.edge_index, data_graph.batch
        x = F.relu(self.gcn1(x, edge_index))
        x = F.relu(self.gcn2(x, edge_index))
        x = global_mean_pool(x, batch)
        

        weighted_static = self.static_weight * x_static
        weighted_graph = self.graph_weight * x
        

        x_combined = torch.cat((weighted_static, weighted_graph), dim=1)
        
        x = self.bn1(self.fc1(x_combined))
        x = torch.sigmoid(self.fc2(x))  
        return x


def train(model, loader, optimizer, criterion):
    model.train()
    total_loss = 0
    for static_features, graph_data, labels, names in loader:
        optimizer.zero_grad()
        outputs = model(static_features, graph_data)

        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)

def test_and_rank(model, loader):
    model.eval()
    results = []
    with torch.no_grad():
        for static_features, graph_data, labels, names in loader:
            outputs = model(static_features, graph_data)
            for output, label, name in zip(outputs, labels, names):
                results.append((name, output.item(), label.item()))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def collate_fn(batch):
    static_features, graph_data, labels, names = zip(*batch)
    return torch.stack(static_features), Batch.from_data_list(graph_data), torch.stack(labels), names

def load_and_merge_data(features_csv, labels_csv):

    features_df = pd.read_csv(features_csv)
    labels_df = pd.read_csv(labels_csv)


    merged_df = pd.merge(features_df, labels_df[['name', 'label']], on='name', how='left')

    return merged_df

def main():
    train_dataset = CustomDataset('./path/train.csv', './path/data_for_train', train=True)
    test_dataset = CustomDataset('./path/test.csv', './path/data_for_test', train=False)

    train_loader = DataLoader(train_dataset, batch_size=10, shuffle=True, collate_fn=collate_fn)
    test_loader = DataLoader(test_dataset, batch_size=10, shuffle=False, collate_fn=collate_fn)

    model = IntegratedModel(num_node_features=1, num_static_features=train_dataset.features.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCELoss()

    for epoch in range(5):
        train_loss = train(model, train_loader, optimizer, criterion)
        print(f'Epoch {epoch+1}: Train Loss: {train_loss:.4f}')

    results = test_and_rank(model, test_loader)
    with open('super_result.csv', 'a') as f:
        f.write("name,prob,Actual\n")
    for rank, (name, prob, label) in enumerate(results, start=1):
        print(f"Rank {rank}: Program {name}, Probability = {prob:.4f}, Label = {int(label)}")
        with open('super_result.csv', 'a') as f:
            f.write(f"{name},{prob:.4f},{int(label)}\n")

    merged_df = load_and_merge_data('./super_result.csv', './new_data/test.csv')

    merged_df.to_csv('merged_results.csv', index=False)
if __name__ == '__main__':
    main()

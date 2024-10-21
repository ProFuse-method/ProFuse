import pandas as pd
import numpy as np
import random
from deap import base, creator, tools, algorithms
from datetime import datetime

random.seed(42)

df = pd.read_csv('./path/test.csv', header=None)

column_names = ['Feature' + str(i) for i in range(1, len(df.columns))] + ['Label']

df.columns = column_names

df.insert(0, 'ID', range(1, 1 + len(df)))

df.to_csv('./df_ALL_features.csv', index=False, header=True)

df = pd.read_csv('./df_ALL_features.csv')
data = df.set_index('ID')  

def evaluate(individual):
    distances = []
    for i in range(len(individual) - 1):
        for j in range(i + 1, len(individual)):
            vec1 = data.loc[individual[i]].values  
            vec2 = data.loc[individual[j]].values
            cos_sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
            distances.append(1 - cos_sim)
    return (np.mean(distances),)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, data.index.tolist(), len(data.index))  
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=50)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)


population = toolbox.population()
ngen = 20
for gen in range(ngen):
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
    
    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.7:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values
        if random.random() < 0.1:
            toolbox.mutate(child1)
            toolbox.mutate(child2)
            del child1.fitness.values
            del child2.fitness.values

    population[:] = offspring

best_ind = tools.selBest(population, 1)[0]


best_df = data.loc[best_ind].reset_index()
best_df.to_csv('./SBP_features.csv', index=False)

print("save 'optimized_id_order_with_features.csv'")


df = pd.read_csv('./SBP_features.csv')


df['Original_Index'] = df.index + 1  


bug_indices = df[df['Label'] == 1]['Original_Index'].tolist()  
print("Bug Indices:", bug_indices)


n = len(df)  
m = len(bug_indices)  
apfd = 1 - (sum(bug_indices) / (n * m)) + (1 / (2 * n))
print("APFD Value:", apfd)


current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Current Time:", current_time)
import json
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

with open('./desafioBlip/spiders/output.json', 'r') as file:
    words = json.load(file)

unique_words = set()
for word_obj in words:
    unique_words.add(word_obj["word"])
    for synonym in word_obj["synonyms"]:
        unique_words.add(synonym)
    for antonym in word_obj["antonyms"]:
        unique_words.add(antonym)

word_to_index = {word: i for i, word in enumerate(unique_words)}

vectors = []
for word_obj in words:
    vector = np.zeros(len(unique_words))
    vector[word_to_index[word_obj["word"]]] = 1  
    for synonym in word_obj["synonyms"]:
        vector[word_to_index[synonym]] = 1  
    for antonym in word_obj["antonyms"]:
        vector[word_to_index[antonym]] = -1  
    vectors.append(vector)

vectors = np.array(vectors)

n_init = 10 
kmeans = KMeans(n_clusters=2, n_init=n_init, random_state=0)
clusters = kmeans.fit_predict(vectors)

G = nx.Graph()

for word_obj, cluster in zip(words, clusters):
    word = word_obj["word"]
    G.add_node(word, cluster=cluster)

for word_obj in words:
    word = word_obj["word"]
    for synonym in word_obj["synonyms"]:
        G.add_edge(word, synonym)

for word_obj in words:
    word = word_obj["word"]
    for antonym in word_obj["antonyms"]:
        G.add_edge(word, antonym)

node_colors = [cluster for _, cluster in G.nodes(data='cluster')]

pos = nx.spring_layout(G) 

nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.Set1, font_size=8)
plt.show()

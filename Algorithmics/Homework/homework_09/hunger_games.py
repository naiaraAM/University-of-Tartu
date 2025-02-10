from pyvis.network import Network
import networkx as nx

# Data
killers = {
  "Katniss Everdeen": [
    "Marvel",
    "Glimmer",
    "Cato",
    "Gloss",
    "President Alma Coin"
  ],
  "Peeta Mellark": [
    "Brutus"
  ],
  "Thresh": [
    "Clove"
  ],
  "Johanna Mason": [
    "Cashmere"
  ],
  "Cato": [
    "District 3 Male Tribute"
  ],
  "Gloss": [
    "Wiress"
  ],
  "Marvel": [
    "Rue"
  ],
  "Tracker Jackers": [
    "Glimmer"
  ],
  "Muttations": [
    "Cato"
  ],
  "Nightlock Berries": [
    "Foxface"
  ],
  "Poison Fog": [
    "Mags"
  ],
  "Capitol": [
    "Cinna",
    "Boggs",
    "Finnick Odair",
    "Primrose Everdeen"
  ],
  "Rebels": [
    "President Snow"
  ]
}


# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph with weights
for killer, victims in killers.items():
    for victim in victims:
        G.add_edge(killer, victim, weight=1)

# Create a pyvis network
net = Network(notebook=True, directed=True)

# Add nodes and edges to the pyvis network
for node in G.nodes:
    net.add_node(node)

for edge in G.edges(data=True):
    net.add_edge(edge[0], edge[1], title=f"Weight: {edge[2].get('weight', 1)}")

# Generate and save the interactive HTML file
net.show("hunger_games_kills.html")
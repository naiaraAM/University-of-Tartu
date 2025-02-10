import networkx as nx
import random
import matplotlib.pyplot as plt

from Homework.homework_09.ex_01.sample_code import characterize_graph

random.seed(0)

# Function to generate random person attributes
def generate_person_attributes(person_id):
    age = random.randint(18, 65)  # Random age between 18 and 65
    interests = random.sample(['Music', 'Sports', 'Reading', 'Gaming', 'Cooking', 'Traveling', 'Art'],
                              2)  # Random 2 interests
    location = random.choice(['New York', 'London', 'Paris', 'Berlin', 'Tokyo', 'Sydney'])  # Random location
    return {'age': age, 'interests': interests, 'location': location}


# Function to calculate similarity score between two people based on attributes
def calculate_similarity(person1, person2):
    score = 0
    # Location similarity
    if person1['location'] == person2['location']:
        score += 1
    # Interest similarity (count shared interests)
    shared_interests = len(set(person1['interests']).intersection(person2['interests']))
    score += shared_interests * 0.5  # Each shared interest adds 0.5 to the score
    # Age similarity (smaller difference gives higher score)
    age_difference = abs(person1['age'] - person2['age'])
    if age_difference <= 5:
        score += 1  # Close in age
    elif age_difference <= 10:
        score += 0.5  # Somewhat close in age
    return score


# Function to generate a social network graph based on attribute similarities
def generate_social_network_graph(num_people, similarity_threshold=1.5):
    G = nx.DiGraph()  # Directed graph
    for person_id in range(1, num_people + 1):
        G.add_node(person_id, **generate_person_attributes(person_id))

    # Add friendships (directed edges) based on similarity score
    for person_id in G.nodes:
        for friend_id in G.nodes:
            if friend_id != person_id:
                similarity_score = calculate_similarity(G.nodes[person_id], G.nodes[friend_id])
                if similarity_score >= similarity_threshold:
                    weight = round(similarity_score, 2)
                    G.add_edge(person_id, friend_id, weight=weight)

    return G


# Function to visualize the graph with city-based colors
def visualize_graph(G):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)

    # Define a unique color for each city
    locations = list(set(nx.get_node_attributes(G, 'location').values()))
    city_colors = {city: color for city, color in zip(locations, plt.cm.tab10.colors)}

    # Get node colors based on city
    node_colors = [city_colors[G.nodes[node]['location']] for node in G.nodes]

    # Drawing nodes and edges with city colors
    nx.draw(G, pos, with_labels=True, node_size=300, node_color=node_colors, edge_color='gray', font_size=10,
            font_weight='bold')

    # Draw edge weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Add legend for cities
    legend_labels = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in
                     city_colors.values()]
    plt.legend(legend_labels, city_colors.keys(), title="Cities", loc="upper left")
    plt.title("Social Network Graph with City-Based Coloring")
    plt.show()


# Generate a social network graph with similarity-based friendships
G = generate_social_network_graph(10, similarity_threshold=1.5)

# Visualize the graph
visualize_graph(G)

# Print some basic properties of the graph
print("Nodes and their attributes:")
for node, data in G.nodes(data=True):
    print(f"Person {node}: {data}")

print("\nEdges and their attributes:")
for u, v, data in G.edges(data=True):
    print(f"Person {u} -> Person {v}: Weight = {data['weight']:.2f}")

characterize_graph(G, "Personal relations")

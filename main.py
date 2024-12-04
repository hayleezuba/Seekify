from flask import Flask, request, jsonify
import pandas as pd
from AdjacencyList import AdjacencyList
from scipy.spatial.distance import cosine, pdist, squareform
import heapq

app = Flask(__name__)

# Load and preprocess the dataset
dataset = pd.read_csv("dataset.csv")
selected_features = ['valence', 'energy', 'tempo']
# Use a sample of 100,000 points for speed/save on computation
# dataset_size = len(dataset)
# sample_size = min(100000, dataset_size)
sampled_data = dataset.head(10)  # first 50 rows for testing
adjacencylist = AdjacencyList()

# Build the adjacency list
for i, row1 in sampled_data.iterrows():
    for j, row2 in sampled_data.iterrows():
        if i != j:
            similarity = 1 - cosine(row1[selected_features], row2[selected_features])
            adjacencylist.addedge(row1['track_name'], row2['track_name'], similarity)


# Flask route for getting recommendations using Dijkstra's algorithm
@app.route('/recommendation', methods=['POST'])
def get_recommendations():
    data = request.json
    search_query = data['search_query']
    if search_query not in adjacencylist.graph:
        return jsonify({"error": "Song not found"}), 404

    # Use Dijkstra's algorithm to find the most similar songs
    recommendations = search_dijkstra(search_query)

    return jsonify({
        "recommendations": [{"song_title": rec[0], "similarity_score": 1 - rec[1]} for rec in recommendations]
    })


# Dijkstra's Algorithm
def search_dijkstra(input_song_id):
    queue = [(0, input_song_id)]
    dists = {input_song_id: 0}
    visited = set()

    while queue:
        curr_dist, curr_song = heapq.heappop(queue)
        if curr_song in visited:
            continue
        visited.add(curr_song)

        # Update distances for neighbors
        for neighbor, weight in adjacencylist.getneighbors(curr_song).items():
            dist = curr_dist + (1 - weight)  # Distance is inversely related to similarity
            if neighbor not in dists or dist < dists[neighbor]:
                dists[neighbor] = dist
                heapq.heappush(queue, (dist, neighbor))

    # Return the top 5 closest songs (excluding the input song itself)
    sorted_dists = sorted(dists.items(), key=lambda x: x[1])
    return sorted_dists[1:6]  # Skip the input song


# A* Search Algorithm
def search_astar(input_song_id):
    queue = [(0, input_song_id)]
    dists = {input_song_id: 0}
    visited = set()

    while queue:
        curr_cost, curr_song = heapq.heappop(queue)
        if curr_song in visited:
            continue
        visited.add(curr_song)

        # Update distances for neighbors
        for neighbor, weight in adjacencylist.getneighbors(curr_song).items():
            dist = dists[curr_song] + (1 - weight)
            heuristic = 1 - adjacencylist.graph[input_song_id].get(neighbor, 0)  # Similarity heuristic
            cost = dist + heuristic

            if neighbor not in dists or cost < dists[neighbor]:
                dists[neighbor] = cost
                heapq.heappush(queue, (cost, neighbor))

    # Return the top 5 closest songs (excluding the input song itself)
    sorted_dists = sorted(dists.items(), key=lambda x: x[1])
    return sorted_dists[1:6]  # Skip the input song

def test(song_title):
    if song_title not in adjacencylist.graph:
        print(f"Error: Song '{song_title}' not found in the adjacency list.")
        return
    recommendations = search_dijkstra(song_title)
    print(f"Recommendations for '{song_title}':")
    for rec in recommendations:
        print(f" {rec[0]} - Similarity: {1 - rec[1]}")


if __name__ == '__main__':
    run_test = True

    if run_test:
        test_song = "Comedy"
        test(test_song)
    else:
        app.run(debug=True)

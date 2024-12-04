from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
from AdjacencyList import AdjacencyList
from scipy.spatial.distance import cosine
import heapq

# Initialize Flask app
app = Flask(__name__, static_folder='frontend', static_url_path='')

# Serve the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# Load and preprocess the dataset
dataset = pd.read_csv("dataset.csv")
selected_features = ['valence', 'energy', 'tempo']
sampled_data = dataset.head(100)  # Use the first 100 rows for testing, then scale
adjacencylist = AdjacencyList()

# Build the adjacency list
for i, row1 in sampled_data.iterrows():
    for j, row2 in sampled_data.iterrows():
        if i != j:
            similarity = 1 - cosine(row1[selected_features], row2[selected_features])
            adjacencylist.addedge(row1['track_name'], row2['track_name'], similarity)

# Recommendation endpoint
@app.route('/recommendation', methods=['POST'])
def get_recommendations():
    data = request.json
    search_query = data.get('search_query', '')

    if search_query not in adjacencylist.graph:
        return jsonify({"error": f"Song '{search_query}' not found."}), 404

    # Use Dijkstra's algorithm to find recommendations
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
            dist = curr_dist + (1 - weight)
            if neighbor not in dists or dist < dists[neighbor]:
                dists[neighbor] = dist
                heapq.heappush(queue, (dist, neighbor))

    # Return the top 5 closest songs
    sorted_dists = sorted(dists.items(), key=lambda x: x[1])
    return sorted_dists[1:6]

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

    # Return the top 5 closest songs
    sorted_dists = sorted(dists.items(), key=lambda x: x[1])
    return sorted_dists[1:6]

# test code
# def test(song_title):
#     if song_title not in adjacencylist.graph:
#         print(f"Error: Song '{song_title}' not found in the adjacency list.")
#         return
#     recommendations = search_dijkstra(song_title)
#     print(f"Recommendations for '{song_title}':")
#     for rec in recommendations:
#         print(f" {rec[0]} - Similarity: {1 - rec[1]}")

if __name__ == '__main__':
    # Enables/disables testing
    run_test = False

    if run_test:
        # test_song = "Comedy"
        # test(test_song)
        pass
    else:
        app.run(debug=True)

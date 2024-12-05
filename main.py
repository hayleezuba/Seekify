from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
from AdjacencyList import AdjacencyList
from scipy.spatial.distance import cosine
import heapq
from sklearn.preprocessing import MinMaxScaler

# Initialize Flask app
app = Flask(__name__, static_folder='frontend', static_url_path='')


# Serve the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')  # might have to change depending on your setup (ex. FrontEnd/index.html)


# Load and preprocess the dataset
dataset = pd.read_csv("dataset.csv")
selected_features = ['valence', 'energy', 'tempo']

# Normalize features to ensure the cosine similarity calculation works correctly
scaler = MinMaxScaler()
dataset[selected_features] = scaler.fit_transform(dataset[selected_features])

# Drop rows with missing feature values
dataset = dataset.dropna(subset=selected_features)

# Change to smaller number for testing (ex. 100)
sampled_data = dataset.head(10000)
adjacencylist = AdjacencyList()

# Build the adjacency list
for i, row1 in sampled_data.iterrows():
    for j, row2 in sampled_data.iterrows():
        if i != j:
            similarity = 1 - cosine(row1[selected_features], row2[selected_features])
            # Use .lower() for comparison, but keep original artist and song names for display
            adjacencylist.addedge(
                (row1['track_name'].lower(), row1.get('artists', 'Unknown Artist')),  # Lowercase for comparison
                (row2['track_name'].lower(), row2.get('artists', 'Unknown Artist')),  # Lowercase for comparison
                similarity
            )

# Recommendation endpoint for song title
@app.route('/recommendation', methods=['POST'])
def get_recommendations():
    data = request.json
    search_query = data.get('search_query', '').lower()

    # Find the song (case-insensitive)
    matched_songs = [
        song for song in adjacencylist.graph.keys()
        if song[0] == search_query
    ]

    if not matched_songs:
        return jsonify({"error": f"Song '{search_query}' not found."}), 404

    # Use the first matched song
    search_song = matched_songs[0]
    recommendations = search_dijkstra(search_song)

    return jsonify({
        "recommendations": [
            {
                "song_title": rec[0][0].title(),  # Capitalize the first letter of each word in the song title
                "artists": rec[0][1].title(),  # Capitalize the first letter of each word in the artist name
                "similarity_score": 1 - rec[1]
            }
            for rec in recommendations
        ]
    })


# Flask route for getting recommendations using artist name
@app.route('/recommendation-artist', methods=['POST'])
def get_recommendations_artist():
    data = request.json
    search_query = data['search_query']

    # Case-insensitive for artist name
    artist_data = dataset[dataset['artists'].str.lower() == search_query.lower()]

    if artist_data.empty:
        return jsonify({"error": f"Artist '{search_query}' not found."}), 404

    # Get the most popular song by the artist
    most_popular_song = artist_data.loc[artist_data['popularity'].idxmax()]
    song_title = most_popular_song['track_name']
    artists = most_popular_song['artists']

    # Perform similarity calculations for this song
    recommendations = search_dijkstra((song_title.lower(), artists))

    return jsonify({
        "recommendations": [
            {
                "song_title": rec[0][0].title(),  # Capitalize the first letter of each word in the song title
                "artists": rec[0][1].title(),  # Capitalize the first letter of each word in the artist name
                "similarity_score": 1 - rec[1]
            }
            for rec in recommendations
        ]
    })


# Dijkstra's Algorithm for finding the most similar songs
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
    return sorted_dists[1:6]  # Skip the input song itself


# A* Algorithm for finding the most similar songs
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
    return sorted_dists[1:6]  # Skip the input song


# Run the app yay
if __name__ == '__main__':
    app.run(debug=True)

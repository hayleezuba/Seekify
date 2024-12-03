# Mostly external libraries/APIs we pulled from to make this code work
from flask import Flask, request, jsonify
import pandas as pd
from scipy.spatial.distance import cosine
from AdjacencyList import AdjacencyList

# Initialize Flask app
app = Flask(__name__)

# Load the dataset
dataset = pd.read_csv("hf://datasets/vishnupriyavr/spotify-million-song-dataset/spotify_millsongdata.csv")
# Define the imporant columns we want to use to calculate similarity
featuredColumns = ['danceability', 'genre', 'tempo']
# scale values to between 0 and 1 for workability
dataset[featuredColumns] = dataset[featuredColumns].apply(
    lambda x: (x - x.min()) / (x.max() - x.min())
)

# Initalize the AdjacencyList object to store the graph
adjacencylist = AdjacencyList()

# Populate the adjacency list with songs and their similarities
# Each song is a vertex, and the edges between them are the similarity scores
for _, row in dataset.iterrows():
    song_id = row['id']
    song_features = row[featuredColumns].values

    for _, other_row in dataset.iterrows():
        other_song_id = other_row['id']
        if song_id != other_song_id:
            other_song_features = other_row[featuredColumns].values
            # Cosine is used because the characteristics of the song are changed to numerical values in vectos
            # Cosine will focus on the direction, not magnitude of the values in each vector
            # The idea for this was borrowed from https://machinelearninggeek.com/spotify-song-recommender-system-in-python/
            similarity = 1 - cosine(song_features, other_song_features)
            adjacencylist.addedge(song_id, other_song_id, similarity


# Route for getting similar songs based on user input
@app.route('/songrecommendation', methods=['POST']))
def songrecommendation():

    # Get the song name from the request's JSON data
    userInput = request.json.get('song_name', '')

    #Find the song in the dataset using the name
    inputSong = dataset[dataset['song_title'] == userInput]

    #If the song is not found in the dataset, return an error
    if inputSong.empty:
        return jsonify({'error': 'Song not found in the dataset, Please choose another song'})

    # Grab the song ID of the input song using integer location based indexing
    inputSongId = inputSong.iloc[0]['id']

    # Find the most similar song (use the adjacency list and search method)
    similarSongId, similarity = searchdijkstra(inputSongId)
    # similar

    # TODO: if no similar song is found, return one that's in the same genre

    # Get metadata of the most similar song
    similar_song = dataset[dataset['id'] == similarSongId].iloc[0]

    # Return the result as a JSON response
    return jsonify({
        'input_song': userInput,
        'similar_song': similar_song['song_title'],
        'similarity_score': round(similarity, 2)
    })

# TODO: Implement search method that uses Dijkstra's or A* to find the most similar song
def searchdijkstra(input_song_id):
            # Should implement using dijkstras algorithm

def searchastar(input_song_id):
         # Implement using A* algorithm to compare the two
if __name__ == "__main__":
    app.run(debug=True)

# Seekify 🎵  
*By Sophia Cardona Nader, Estefania Griffiths, and Haylee Zuba*  

**Seekify** bridges the gap between Spotify users and discovering new music. Listening to the same old songs can get repetitive and frustrating. Seekify provides an accessible, intuitive platform that recommends songs based on their similarity to the music you already love.  

---

## About This Project  

Seekify uses graph-based algorithms to find and recommend similar songs efficiently. Here's how it works:  
1. **Graph Data Structure**: Songs are stored in a graph where each node represents a song, and edges between nodes are weighted using a similarity metric.  
2. **Similarity Metric**: Song attributes such as tempo, energy, and valence are used to calculate similarity weights.  
3. **Dijkstra's Algorithm**: This algorithm is applied to traverse the graph and identify paths with the smallest weights, recommending songs most similar to the input track.  

Seekify uses a visually pleasing interface to create a positive user experience for finding new music.

---

## Features  

- Input a favorite song, and Seekify recommends five tracks with descending similarity scores.  
- Graph-based data storage with adjacency lists for efficient similarity calculations.  
- Backend-powered recommendation engine using Dijkstra’s Algorithm for accuracy and efficiency.   
- Utilizes a preprocessed Spotify Tracks Dataset for efficient song analysis.  

---


## Installation  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/hayleezuba/Seekify.git  
   cd Seekify

2. Install Dependencies:
     pip install -r dependencies.txt

3. Start the Flask backend:
 python app.py

4. Navigate to the local host using browser
   http://localhost:5000  

---


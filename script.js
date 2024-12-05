document.addEventListener("DOMContentLoaded", () => {
    console.log("Script loaded successfully!");

    const recommendationsList = document.querySelector(".rec-list ul");

    // Create input fields for each bubble (Song, Artist, Genre)
    const songButton = document.querySelector(".bubble:nth-child(1)"); // Song bubble
    const artistButton = document.querySelector(".bubble:nth-child(2)"); // Artist bubble
    const genreButton = document.querySelector(".bubble:nth-child(3)"); // Genre bubble

    // Create input field for Song
    const songInput = document.createElement('input');
    songInput.setAttribute('type', 'text');
    songInput.setAttribute('placeholder', 'Enter Song...');
    songButton.innerHTML = ''; // Clear existing content in the bubble
    songButton.appendChild(songInput); // Append the input field inside the bubble

    // Create input field for Artist
    const artistInput = document.createElement('input');
    artistInput.setAttribute('type', 'text');
    artistInput.setAttribute('placeholder', 'Enter Artist...');
    artistButton.innerHTML = ''; // Clear existing content in the bubble
    artistButton.appendChild(artistInput); // Append the input field inside the bubble

    // Create input field for Genre
    const genreInput = document.createElement('input');
    genreInput.setAttribute('type', 'text');
    genreInput.setAttribute('placeholder', 'Enter Genre...');
    genreButton.innerHTML = ''; // Clear existing content in the bubble
    genreButton.appendChild(genreInput); // Append the input field inside the bubble

    // Function to handle the "Enter" key press
    async function handleInputEnter(inputField, type) {
        inputField.addEventListener("keypress", async (e) => {
            if (e.key === "Enter") {
                const searchQuery = inputField.value.trim();
                if (!searchQuery) return; // Avoid sending empty queries

                // Clear previous recommendations
                recommendationsList.innerHTML = "";

                try {
                    let searchUrl = '/recommendation';
                    let searchData = { search_query: searchQuery };

                    if (type === 'artist') {
                        // Search by artist and get the first song for the artist
                        searchUrl = '/recommendation-artist';
                    } else if (type === 'genre') {
                        // Search by genre and get the first song for the genre
                        searchUrl = '/recommendation-genre';
                    }

                    // Send a POST request to the Flask backend
                    const response = await fetch(searchUrl, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(searchData),
                    });

                    if (!response.ok) throw new Error("Failed to fetch recommendations");

                    const data = await response.json();

                    // Display new recommendations
                    if (data.recommendations) {
                        data.recommendations.forEach((rec) => {
                            const li = document.createElement("li");
                            li.textContent = `${rec.song_title} by ${rec.artists} (Similarity: ${rec.similarity_score.toFixed(2)})`;
                            recommendationsList.appendChild(li);
                        });
                    } else {
                        const li = document.createElement("li");
                        li.textContent = data.error || "No recommendations found";
                        recommendationsList.appendChild(li);
                    }
                } catch (error) {
                    console.error("Error fetching recommendations:", error);
                    alert("Failed to fetch recommendations. Please try again.");
                }
            }
        });
    }

    // Attach the event listener for "Enter" key press for each input field
    handleInputEnter(songInput, 'song');
    handleInputEnter(artistInput, 'artist');
    handleInputEnter(genreInput, 'genre');

    // Modal setup for "Read" and "Learn More" buttons
    const learnMoreButtons = document.querySelectorAll(".learn-more");
    const modal = document.getElementById("modal");
    const modalText = document.getElementById("modal-text");
    const closeModal = document.querySelector(".close");

    learnMoreButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            const buttonText = event.target.innerText;

            // Set modal text based on the button clicked
            if (buttonText === "Read") {
                modalText.innerHTML = `
                    <h2>Our Mission</h2>
                    <p>
                        This project is intended to mitigate the barrier between Spotify users and finding new music.
                        Listening to the same old songs can be frustrating. Seekify aims to create an ease-of-access song
                        finder based on song similarity.
                    </p>`;
            } else if (buttonText === "Learn More") {
                modalText.innerHTML = `
                    <h2>About Us</h2>
                    <p>
                        We are Seekify, by Sophia Cardona Nader, Estefania Griffiths, and Haylee Zuba. This project is
                        accomplished by utilizing graphs to store the song data, giving each song a weight using a similarity
                        metric, then using Dijkstra's algorithm to find the path with the least weight from one song to the
                        next. We hope you enjoy!
                    </p>`;
            }

            // Show the modal
            modal.style.display = "block";
        });
    });

    // Close the modal
    if (closeModal) {
        closeModal.addEventListener("click", () => {
            modal.style.display = "none";
        });
    };

    // Close the modal when clicking outside the modal content
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});

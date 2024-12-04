// Ensure the script is working
console.log("Script loaded successfully!");

// Get modal and modal-related elements only once
const modal = document.getElementById("modal");
const modalText = document.getElementById("modal-text");
const closeModal = document.querySelector(".close");

// Ensure the "Get Recommendations" button is only declared once
let getRecommendationsButton = document.querySelector(".get-recommendations");

if (getRecommendationsButton) {
    getRecommendationsButton.addEventListener("click", () => {
        alert("Fetching your recommendations... Stay tuned!");
    });
}

// Add click event listeners to the "Read" and "Learn More" buttons
const learnMoreButtons = document.querySelectorAll(".learn-more");

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

// Close the modal when the "X" is clicked
if (closeModal) {
    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });
}

// Close the modal when clicking outside of the modal content
window.addEventListener("click", (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
});

// matchup_guide_script.js
document.getElementById("matchup-guide-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const userCharacter = document.getElementById("user-character").value;
    const opponentCharacter = document.getElementById("opponent-character").value;

    try {
        const response = await fetch("/matchup_guide", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_character: userCharacter, opponent_character: opponentCharacter }),
        });
        const recommendations = await response.json();
        displayMatchupRecommendations(recommendations);
    } catch (error) {
        console.error("Error:", error);
    }
});
    
    // Display matchup guide results in the "matchup-guide-results" div
    function displayMatchupGuideResults(results) {
        // Assuming `results` is an array of objects containing the matchup data
        const container = document.getElementById("matchup-results");
    
        // Clear the container before displaying new results
        container.innerHTML = "";
    
        results.forEach((result) => {
            const resultDiv = document.createElement("div");
            resultDiv.classList.add("matchup-result");
    
            const title = document.createElement("h3");
            title.innerText = result.title;
            resultDiv.appendChild(title);
    
            const description = document.createElement("p");
            description.innerText = result.description;
            resultDiv.appendChild(description);
    
            container.appendChild(resultDiv);
        });
    }


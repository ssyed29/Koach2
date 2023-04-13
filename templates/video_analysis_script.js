document.getElementById("video-analysis-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const game = document.getElementById("game").value;
    const videoFile = document.getElementById("video-file").files[0];
    const videoUrl = document.getElementById("video-url").value;
    const formData = new FormData();
    formData.append("video-file", videoFile);
    formData.append("video-url", videoUrl);
    formData.append("game", game);

    try {
        const response = await fetch("/upload_video", {
            method: "POST",
            body: formData
        });
        const results = await response.json();
        displayAnalysisResults(results);
    } catch (error) {
        console.error("Error:", error);
    }
});

function displayVideoAnalysisResults(results) {
    
        const videoAnalysisResults = document.getElementById("video-analysis-results");
        videoAnalysisResults.innerHTML = "";

        // Display the results based on the data format
        results.forEach(result => {
            const resultContainer = document.createElement("div");
            resultContainer.innerHTML = `<h3>${result.title}</h3><p>${result.description}</p>`;
            videoAnalysisResults.appendChild(resultContainer);
        });
      
        // Populate the rounds-summary table
        let roundsTableBody = document.getElementById("rounds-summary-table").querySelector("tbody");
        results.roundsSummary.forEach(round => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${round.number}</td>
            <td>${round.missedMoves}</td>
            <td>${round.punishersUsed}</td>
            <td>${round.healthRemaining}</td>
            <td>${round.damageDealt}</td>
            <td>${round.successfulMoves}</td>
            <td>${round.comboDamage}</td>
          `;
          roundsTableBody.appendChild(row);
        });

        // Create the list of timestamped suggestions
        let suggestionsList = document.getElementById("suggestions-list");
        results.suggestions.slice(0, 5).forEach(suggestion => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `<strong>${suggestion.timestamp}</strong>: ${suggestion.text}`;
            suggestionsList.appendChild(listItem);
        });   
}

document.getElementById("frame-data-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const game = document.getElementById("game").value;
    const character = document.getElementById("character").value;

    try {
        const response = await fetch(`/frame_data?game=${game}&character=${character}`);
        const frameData = await response.json();
        displayFrameDataResults(frameData);
    } catch (error) {
        console.error("Error:", error);
    }
});

function displayFrameDataResults(frameData) {
    const frameDataResults = document.getElementById("frame-data-results");
    frameDataResults.innerHTML = "";

    // Display the frame data based on the data format
    frameData.forEach(move => {
        const moveContainer = document.createElement("div");
        moveContainer.innerHTML = `<h3>${move.name}</h3><p>Startup: ${move.startup} | Active: ${move.active} | Recovery: ${move.recovery}</p>`;
        frameDataResults.appendChild(moveContainer);
    });
}

const zipInput = document.getElementById("zipInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const dashboard = document.getElementById("dashboard");
const statusMessage = document.getElementById("statusMessage");

analyzeBtn.addEventListener("click", fetchWeatherData);

async function fetchWeatherData() {
    const zip = zipInput.ariaValueMax.trim();

    if(!zip) {
        showStatus("Please enter a ZIP Code.", true);
        return;
    }

    showStatus("Fetching weather data....", false);
    dashboard.innerHTML = "";
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/analyze?zip=${zip}`);
        if(!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Failed to fetch data");
        }

        const data = await response.json();
        renderDashboard(data);
        showStatus("Analysis Completed Successfully.", false);
    } catch (error) {
        showStatus(error.message, true);
    }

}

function renderDashboard(data) {
    dashboard.innerHTML = "";
    Object.keys(data).forEach(task => {
        const taskData = data[task];
        const card = document.createElement("div");
        card.className = "card";
        const badgeColor = taskData.risk === "GREEN" ? "green" : taskData.risk === "YELLOW" ? "yellow" : "red";
        card.innerHTML = `
        <div class="card-header">
        <h3>${task}</h3>
        <span class="risk-badge ${badgeColor}">${taskData.risk}</span>
        </div>

        <div class="metrics">
        <div><strong>Date: </strong>${taskData.date}</div>
        <div><strong>Average Temp: </strong>${taskData.avg_temp} *F</div>
        <div><strong>Max Wind: </strong>${taskData.max_wind}</div>
        <div><strong>Rain Detected: </strong>${taskData.rain_detected ? "Yes" : "No"}</div>
        </div>
        `;
        dashboard.appendChild(card);
    })
}

function showStatus(message, isError) {
    statusMessage.textContent = message;
    statusMessage.style.color = isError ? "red" : "green";
}
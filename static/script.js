function showSection(id) {
    document.querySelectorAll("section").forEach(sec => sec.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

function drawChart(canvasId, value) {
    const ctx = document.getElementById(canvasId).getContext("2d");

    if (window.currentChart) {
        window.currentChart.destroy();
    }

    window.currentChart = new Chart(ctx, {
    type: 'line',   // changed from bar to line
    data: {
        labels: ['Input', 'Prediction'],   // X-axis labels
        datasets: [{
    label: 'Energy Output',
    data: [
        value * 0.2,
        value * 0.5,
        value * 0.75,
        value
    ],
    fill: false,
    borderWidth: 3,
    tension: 0.4,          // controls curvature
    cubicInterpolationMode: 'monotone',  // smooth curve
    pointRadius: 4
}]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Stage'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Predicted Value'
                },
                beginAtZero: true
            }
        }
    }
});
}

function predictSolar() {
    fetch("/predict_solar", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            hour: document.getElementById("solar_hour").value,
            temperature: document.getElementById("solar_temp").value,
            irradiance: document.getElementById("solar_irr").value,
            humidity: document.getElementById("solar_hum").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) { alert(data.error); return; }
        document.getElementById("solar_output").innerText =
            "Expected Solar Generation: " + data.result;
        drawChart("solarChart", data.result);
    });
}

function predictLoad() {
    fetch("/predict_load", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            date: document.getElementById("load_date").value,
            hour: document.getElementById("load_hour").value,
            temperature: document.getElementById("load_temp").value,
            humidity: document.getElementById("load_hum").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) { alert(data.error); return; }
        document.getElementById("load_output").innerText =
            "Expected Load Demand: " + data.result;
        drawChart("loadChart", data.result);
    });
}

function predictOutage() {
    fetch("/predict_outage", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            wind: document.getElementById("wind").value,
            rainfall: document.getElementById("rain").value,
            temperature: document.getElementById("out_temp").value,
            storm: document.getElementById("storm").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) { alert(data.error); return; }
        document.getElementById("outage_output").innerText =
            "Outage Probability: " + data.result;
        drawChart("outageChart", data.result);
    });
}
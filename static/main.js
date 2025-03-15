class DataChart {
    #chart;
    constructor(title) {
        const canvasContainer = document.createElement("div");
        canvasContainer.style.width = "500px";
        canvasContainer.style.height = "300px";
        const canvas = document.createElement("canvas");
        this.#chart = new Chart(canvas, {
            type: "line",
            data: {
                labels: [],
                datasets: [{
                    label: title,
                    data: [],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        canvasContainer.appendChild(canvas);
        document.querySelector("#chart-container").appendChild(canvasContainer);
    }
    addData(data) {
        this.#chart.data.labels.push(this.#chart.data.labels.length);
        this.#chart.data.datasets[0].data.push(data);
        this.#chart.update();
    }
}

const altitude = new DataChart("Altitude");
const temperature = new DataChart("Temperature");

const socket = io();
socket.on("updateData", (data) => {
    altitude.addData(data.altitude);
    temperature.addData(data.temperature);
});

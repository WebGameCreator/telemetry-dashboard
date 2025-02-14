const chart1 = new Chart(document.getElementById("chart1"), {
    type: "line",
    data: {
        labels: [0, 1, 2, 3, 4, 5],
        datasets: [{
            label: "Test Data",
            data: [12, 19, 3, 5, 2, 3],
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

const socket = io();
socket.on("updateData", ({ data }) => {
    chart1.data.labels.push(chart1.data.labels.length);
    chart1.data.datasets[0].data.push(data);
    chart1.update();
});

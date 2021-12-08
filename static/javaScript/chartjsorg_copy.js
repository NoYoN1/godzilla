var chData;
var myChart;
var number = [];
const fileUrl = "static/json/chart_copy.json";
async function load() {
  const response = await fetch(fileUrl);
  const cData = await response.json();
  chData = eval(cData);
  const trades = chData[0].length;
  const dataNumber = Object.keys(chData).length;
  for (var i = 0; i < trades; i++) {
    number[i] = i;
  }
  const labels = number;
  const label = "Trade";
  const data = {
    labels: labels,
    datasets: [],
  };
  for (var j = 0; j < dataNumber; j++) {
    const rColor = Math.floor(Math.random() * 16777215).toString(16);
    const addData = {
      label: label + (1 + j),
      data: chData[j],
      backgroundColor: "#" + rColor,
      borderColor: "#" + rColor,
      borderWidth: 1.5,
    };
    data.datasets.push(addData);
  }
  const config = {
    type: "line",
    data: data,
    options: {
      datasets: {
        line: {
          pointRadius: 0.5,
        },
      },
      elements: {
        point: {
          radius: 0.5,
        },
      },
    },
  };
  myChart = new Chart(document.getElementById("myChart"), config);
}

load();

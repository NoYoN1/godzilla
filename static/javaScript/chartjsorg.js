var chData;
var myChart;
var number = [];
const fileUrl = "static/json/chartMulti.json";
async function load() {
  //get local data
  const response = await fetch(fileUrl);
  const cData = await response.json();
  chData = eval(cData);
  //データの長さを取得
  const trades = chData[0].length;
  //データがいくつあるか取得する
  const dataNumber = Object.keys(chData).length;

  //ラベルを取得
  for (var i = 0; i < trades; i++) {
    number[i] = i;
  }
  const labels = number;
  const label = "Trade";
  //データの準備をする
  const data = {
    labels: labels,
    datasets: [],
  };
  //データを入れる
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
  //背景いろ
  const plugin = {
    beforeDraw: (chart) => {
      const ctx = chart.canvas.getContext("2d");
      ctx.save();
      ctx.fillStyle = "white";
      ctx.fillRect(0, 0, chart.width, chart.height);
      ctx.restore();
    },
  };
  //チャートの設定や表示
  const config = {
    type: "line",
    data: data,
    plugins: [plugin],
    options: {
      responsive: true,
      interaction: {
        intersect: false,
        axis: "x",
      },
      datasets: {
        line: {
          pointRadius: 0.1,
        },
      },
      elements: {
        point: {
          radius: 18,
        },
      },
    },
  };
  myChart = new Chart(document.getElementById("myChart"), config);

  //#########//
  var single = document.getElementById("bottomResult");
  var multi = document.getElementById("multi");
  if (dataNumber !== 1) {
    multi.style.display = "block";
    single.style.display = "none";
  }
  //#########//
}
load();

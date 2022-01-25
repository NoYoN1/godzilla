const chart = LightweightCharts.createChart(document.getElementById("chart"), {
  width: 1024,
  height: 500,
  timeScale: {
    timeVisible: true,
    borderColor: "#D1D4DC",
  },
  rightPriceScale: {
    borderColor: "#D1D4DC",
  },
  layout: {
    backgroundColor: "#ffffff",
    textColor: "#000",
  },
  grid: {
    horzLines: {
      color: "#F0F3FA",
    },
    vertLines: {
      color: "#F0F3FA",
    },
  },
});

var series = chart.addCandlestickSeries({
  upColor: "rgb(38,166,154)",
  downColor: "rgb(255,82,82)",
  wickUpColor: "rgb(38,166,154)",
  wickDownColor: "rgb(255,82,82)",
  borderVisible: false,
});

const fileUrlChart = "/static/json/buysell.json";
async function load() {
  var selectData = document.getElementById("selectData").value;
  var fileUrl;
  if (selectData === "EURUSD_D1") {
    fileUrl = "/static/json/EURUSD_D1.json";
  } else if (selectData === "EURJPY_D1") {
    fileUrl = "/static/json/EURJPY_D1.json";
  }

  //get local data
  const response = await fetch(fileUrl);
  const cData = await response.json();
  var data = cData;

  // const chartbs = await fetch(fileUrlChart);
  // const chData = await chartbs.json();
  // var chartData = chData;

  // console.log(chartData["buy"][0]);

  series.setData(data);
  //data.length - 19
  var datesForMarkers = [data[19], data[26], data[27], data[28]];

  var indexOfMinPrice = 0;
  for (var i = 1; i < datesForMarkers.length; i++) {
    if (datesForMarkers[i].high < datesForMarkers[indexOfMinPrice].high) {
      indexOfMinPrice = i;
    }
  }
  var markers = [];
  for (var i = 0; i < datesForMarkers.length; i++) {
    if (i !== indexOfMinPrice) {
      markers.push({
        time: datesForMarkers[i].time,
        position: "aboveBar",
        color: "#e91e63",
        shape: "arrowDown",
        text: "Sell @ " + Math.floor(datesForMarkers[i].high + 2),
      });
    } else {
      markers.push({
        time: datesForMarkers[i].time,
        position: "belowBar",
        color: "#2196F3",
        shape: "arrowUp",
        text: "Buy @ " + Math.floor(datesForMarkers[i].low - 2),
      });
    }
  }
  markers.push({
    time: data[data.length - 48].time,
    position: "aboveBar",
    color: "#f68410",
    shape: "circle",
    text: "D",
  });
  series.setMarkers(markers);
}
load();

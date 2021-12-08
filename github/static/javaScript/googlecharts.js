google.charts.load("current", { packages: ["line"] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var data = new google.visualization.DataTable();
  data.addColumn("number", "Day");
  data.addColumn("number", "TRADE " + 2);

  data.addRows([
    [1, 1000],
    [2, 990],
    [3, 1010],
    [4, 1019.99799],
    [5, 1030.1979698999999],
    [6, 1019.8959902009999],
    [7, 1009.69703029899],
    [8, 1019.7940006019799],
    [9, 1019.7940006019799],
    [10, 1019.6920212019196],
    [11, 990.0],
    [12, 999.9],
    [13, 1019.99799],
    [14, 1030.1979698999999],
  ]);

  var options = {
    chart: {
      title: "TRADES",
      //   subtitle: "(USD)",
    },
    width: 850,
    height: 460,
  };

  var chart = new google.charts.Line(document.getElementById("chart_div"));

  chart.draw(data, google.charts.Line.convertOptions(options));
}

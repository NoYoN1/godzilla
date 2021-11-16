function topMenu(page) {
  var strategy = document.getElementById("strategy");
  var riskManage = document.getElementById("risk-management");
  var margets = document.getElementById("margets");
  switch (page) {
    case 1:
      strategy.style.display = "block";
      riskManage.style.display = "none";
      margets.style.display = "none";
      break;
    case 2:
      strategy.style.display = "none";
      riskManage.style.display = "block";
      margets.style.display = "none";
      break;
    case 3:
      strategy.style.display = "none";
      riskManage.style.display = "none";
      margets.style.display = "block";
      break;
  }
}

function topMenuText() {
  if (document.getElementById("top-menu0").innerHTML === "ストラテジー") {
    document.getElementById("top-menu0").innerHTML = "STRATEGY";
  } else {
    document.getElementById("top-menu0").innerHTML = "ストラテジー";
  }
}

const myChart = new Chart(document.getElementById("myChart"), config);
const config = {
  type: "line",
  data: data,
  options: {},
};
const labels = ["January", "February", "March", "April", "May", "June"];
const data = {
  labels: labels,
  datasets: [
    {
      label: "My First dataset",
      backgroundColor: "rgb(255, 99, 132)",
      borderColor: "rgb(255, 99, 132)",
      data: [0, 10, 5, 2, 20, 30, 45],
    },
  ],
};

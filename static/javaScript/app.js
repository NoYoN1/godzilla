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

// top menu text
// function topMenuText() {
//   if (document.getElementById("top-menu0").innerHTML === "ストラテジー") {
//     document.getElementById("top-menu0").innerHTML = "STRATEGY";
//   } else {
//     document.getElementById("top-menu0").innerHTML = "ストラテジー";
//   }
// }

function riskResetValue() {
  document.getElementById("initialCash").value = "1000";
  document.getElementById("tradesRequired").value = "300";
  document.getElementById("riskPerTrade").value = "1";
  document.getElementById("profitRatio").value = "1";
  document.getElementById("winRatio").value = "50";
  document.getElementById("dataRequired").value = "dataRequired";
}
function changeLanguage(ln) {
  var language = 1;
  if (language === ln) {
    document.getElementById("normal").innerHTML = "通常用";
    document.getElementById("normal").style.color = "white";
    document.getElementById("expert").innerHTML = "専門用";
    document.getElementById("strategy-menu").innerHTML = "ストラテジー";
    document.getElementById("risk-manage").innerHTML = "リスク管理";
    document.getElementById("mrkt").innerHTML = "マーケット";
    document.getElementById("slctStr").innerHTML = "ストラテジー選択";
    document.getElementById("titleStrategy").innerHTML = "ストラテジー";
  } else {
    document.getElementById("normal").innerHTML = "NORMAL MODE";
    document.getElementById("normal").style.color = "white";
    document.getElementById("expert").innerHTML = "EXPERT MODE";
    document.getElementById("strategy-menu").innerHTML = "STRATEGY";
    document.getElementById("risk-manage").innerHTML = "RISK MANAGEMENT";
    document.getElementById("mrkt").innerHTML = "MARKET";
    document.getElementById("slctStr").innerHTML = "STRATEGY SELECT";
    document.getElementById("titleStrategy").innerHTML = "STRATEGY";
  }
}

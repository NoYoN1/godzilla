var aaa = ""
async function markets() {
  const response = await fetch("/static/json/b.json");
  const myJson = await response.json();
  main = ["Open", "Low", "Close", "Adj Close", "Volume", "trading volume"]
  color = [ "one","two","three","four","five","six"]

  // document.getElementById("market").innerHTML = myFunction();

  // function myFunction() {
  //   document.write("<table border=\"" + 1 + "\" > ")
  aaa += "<table> " + "<tr>" + "<th>Name</th>"
  for (var i = 0; i < 6; i++) {
    aaa += "<td>" + main[i] + "</td>"
  }
  //   main = ["Open", "Low", "Close", "Adj Close", "Volume", "trading volume"]
  //   document.write("<tr>" + "<th>Name</th>");
  //   for (var i = 0; i < 6; i++) {
  //     document.write("<td>" + main[i] + "</td>")
  //   }
  aaa += "</tr>"
  //   document.write("</tr>");
  for (var i = 0; i < 25; i++) {
    aaa += "<tr id ="+main[i]+">" + "<th id ="+main[i]+">" + myJson.text[i].name + "</th>"
    //     document.write("<tr>" + "<th>" + myJson.text[i].name + "</th>");
    for (var j = 0; j < 6; j++) {
      aaa += "<td id = "+color[j] + " >" + (myJson.text[i].value[j]).toFixed(4) + "</td>"
      //       // document.write();
      //       document.write("<td>" + myJson.text[i].value[j] + "</td>");
    }
    aaa += "</tr>"
    //     document.write("</tr>");
  }
  aaa += "</table>"
  //   document.write("</table>")
  // }
  document.getElementById("market").innerHTML = aaa
}
markets();
console.log("dasd" + aaa)

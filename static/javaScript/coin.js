async function markets() {
  const response = await fetch("/static/b.json");
  const myJson = await response.json();
  document.getElementById("symbol").innerHTML = myJson.name;
  document.getElementById("value").innerHTML = myJson.value[4];
}
markets();

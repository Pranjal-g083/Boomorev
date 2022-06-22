if (sessionStorage.getItem("theme") === null) {
  sessionStorage.setItem("theme", "light");
  document.getElementById("theme-toggle").checked = false;
} else {
  if (sessionStorage.getItem("theme") === "dark") {
    document.getElementById("theme-toggle").checked = true;
  } else {
    document.getElementById("theme-toggle").checked = false;
  }
}
document.body.setAttribute("theme", sessionStorage.getItem("theme"));

document.getElementById("theme-toggle").addEventListener("click", (e) => {
  sessionStorage.setItem("theme", e.target.checked ? "dark" : "light");
  document.body.setAttribute("theme", sessionStorage.getItem("theme"));
});

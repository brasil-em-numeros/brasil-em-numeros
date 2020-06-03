document.querySelectorAll("#layoutSidenav_nav .sb-sidenav a.nav-link").forEach(function toggleNavlinks(e){
    if (e.href === window.location.href) {
        e.classList.add("active");
    }
})

document.getElementById("sidebarToggle").addEventListener("click", function toggleSidebar(){
    const body = document.querySelector("body")
    const style = "sb-sidenav-toggled"

    body.classList.contains(style) ?
        body.classList.remove(style) :
        body.classList.add(style)
})

const fetchData = (url, callback) =>
  fetch(url)
    .then(response => response.json())
    .then(callback)

const graphicElement = document.getElementById('pdt-chart')
const plot_pdt = (data) => Plotly.newPlot(
    graphicElement, data,
    {margin: { t: 0 } }
);

graphicElement && fetchData("/pdt/pdt_data", plot_pdt)
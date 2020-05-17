/*!
    * Start Bootstrap - SB Admin v6.0.0 (https://startbootstrap.com/templates/sb-admin)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    (function($) {
    "use strict";

    // Add active state to sidbar nav links
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
        $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function() {
            if (this.href === path) {
                $(this).addClass("active");
            }
        });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });
})(jQuery);

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.getElementById('pdt-date');
    var instances = M.Datepicker.init(elems, {});
    elems.M_Datepicker.options.i18n.months = [
        'Janeiro', 'Fevereiro', 'Março',
        'Abril', 'Maio', 'Junho', 'Julho',
        'Agosto', 'Setembro', 'Outubro',
        'Novembro', 'Dezembro'
    ];
  });

slider = document.getElementById("pdt-slider");
slider.addEventListener("input", e => {
    fetch("/pdt", {
        method : 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(slider.value)
    }).then(
        fetch("/pdt_data").then(
            response => response.json()
        ).then(
            data => plot_pdt(data)
        )
    )
});

TESTER = document.getElementById('pdt-chart')
// TESTER.addEventListener('DOMContentLodaded', () => {
//     fetch("/pdt_data").then(
//         response => response.json()
//     ).then(
//         data => plot_pdt(data)
//     )
// })
function plot_pdt(data){
    return Plotly.newPlot(
        TESTER, data,
        {margin: { t: 0 } }
    );
};


// fetch("/pdt/pdt_data").then(
//     response => response.json()
// ).then(
//     data => plot_pdt(data)
// );

// document.addEventListener('DOMContentLoaded', function() {

//     var elems = document.querySelectorAll('select');
//     var instances = M.FormSelect.init(elems, {});
    
//     var orgao  = document.getElementById('orgao-gov');
//     var funcao = document.getElementById('funcao-gov');
    
//     orgao.addEventListener('change', update_and_load);
//     funcao.addEventListener('change', update_and_load);

// });

// function update_and_load(e){

//     var select = e.target
//     select = M.FormSelect.getInstance(select)
//     const name = select.el.id.split("-")[0]

//     fetch("/pdt/pdt", {
//         method : 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({[name] : select.getSelectedValues()})
//     }).then(
//         res => {
//             fetch("/pdt/pdt_data").then(
//                 res => res.json()
//             ).then(
//                 data => plot_pdt(data)
//             )
//         }
//     );

//     return null;
// };

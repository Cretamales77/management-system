$(document).ready(function () {
  const botonesEliminar = document.querySelectorAll(".btn-delete-producto");
  const formEliminar = document.getElementById("deleteCategoryForm");
  const inputProductoId = document.getElementById("delete-id");
  const spanNombreProducto = document.getElementById("deleteCategoryName");

  botonesEliminar.forEach(btn => {
    btn.addEventListener("click", function () {
      inputProductoId.value = this.getAttribute("data-producto-id");
      spanNombreProducto.textContent = this.getAttribute("data-producto-nombre");
      formEliminar.action = this.getAttribute("data-url");
    });
  });
});

$(document).ready(function () {
  const table = $('.datatable').DataTable({
    language: {
      info: "Mostrando _START_ de _END_ | Total _TOTAL_ producto(s)",
      infoEmpty: "Sin productos para mostrar",
      lengthMenu: "Mostrar _MENU_ productos",
      search: "🔍 Buscar:",
      zeroRecords: "No se encontraron resultados.",
      infoFiltered: "(filtrado de un total de _MAX_ producto(s))",
      paginate: {
        first: "Primero",
        last: "Último",
        next: ">",
        previous: "<"
      }
    },
    dom: 'lrtip',
    pageLength: 10,
    lengthMenu: [5, 10, 15, 25],
    columnDefs: [
      { orderable: false, targets: -1 }
    ]
  });

  $('#buscarProducto').on('keyup', function () {
    table.search(this.value).draw();
  });
});

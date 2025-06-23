$(document).ready(function () {
  const table = $('.datatable').DataTable({
    language: {
      info: "Mostrando _START_ de _END_ | Total _TOTAL_ movimiento(s)",
      infoEmpty: "Sin movimientos para mostrar",
      lengthMenu: "Mostrar _MENU_ movimientos",
      search: "🔍 Buscar:",
      zeroRecords: "No se encontraron resultados.",
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
      { orderable: false, targets: 1 }
    ]
  });

  $('#searchMovimiento').on('keyup', function () {
    table.column(0).search(this.value).draw();
  });
});

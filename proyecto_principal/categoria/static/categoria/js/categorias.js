// Modales edición y eliminación 
const editCategoryModal = document.getElementById('editCategoryModal');
const deleteCategoryModal = document.getElementById('deleteCategoryModal');

editCategoryModal.addEventListener('show.bs.modal', function (event) {
  const button = event.relatedTarget;
  const id = button.getAttribute('data-id');
  const nombre = button.getAttribute('data-nombre');
  const descripcion = button.getAttribute('data-descripcion');

  document.getElementById('edit-id').value = id;
  document.getElementById('edit-nombre').value = nombre;
  document.getElementById('edit-descripcion').value = descripcion;

  document.getElementById('editCategoryForm').action = `/categoria/editar/${id}/`;
});

deleteCategoryModal.addEventListener('show.bs.modal', function (event) {
  const button = event.relatedTarget;
  const id = button.getAttribute('data-id');
  const nombre = button.getAttribute('data-nombre');

  document.getElementById('delete-id').value = id;
  document.getElementById('delete-nombre').textContent = nombre;

  document.getElementById('deleteCategoryForm').action = `/categoria/eliminar/${id}/`;
});

$(document).ready(function () {
  const table = $('.datatable').DataTable({
    language: {
      info: "Mostrando _START_ de _END_ | Total _TOTAL_ categoría(s)",
      infoEmpty: "Sin categorías para mostrar",
      lengthMenu: "Mostrar _MENU_ categorías",
      search: "🔍 Buscar:",
      zeroRecords: "No se encontraron resultados.",
      infoFiltered: "(filtrado de un total de _MAX_ categoría(s))",
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
      { orderable: false, targets: [1, 2] }
    ]
  });

  $('#searchCategorias').on('keyup', function () {
    table.column(0).search(this.value).draw();
  });
});

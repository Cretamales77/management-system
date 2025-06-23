// Modales edición y eliminación 
const editProveedorModal = document.getElementById('editProveedorModal');
const deleteProveedorModal = document.getElementById('deleteProveedorModal');

editProveedorModal.addEventListener('show.bs.modal', function (event) {
  const button = event.relatedTarget;
  const id = button.getAttribute('data-id');
  const nombre = button.getAttribute('data-nombre');
  const telefono = button.getAttribute('data-telefono');
  const correo = button.getAttribute('data-correo');
  const direccion = button.getAttribute('data-direccion');
  const pais = button.getAttribute('data-pais');
  const ciudad = button.getAttribute('data-ciudad');
  const comuna = button.getAttribute('data-comuna');

  document.getElementById('edit-id').value = id;
  document.getElementById('edit-nombre').value = nombre;
  document.getElementById('edit-telefono').value = telefono;
  document.getElementById('edit-correo').value = correo;
  document.getElementById('edit-direccion').value = direccion;
  document.getElementById('edit-pais').value = pais;
  document.getElementById('edit-ciudad').value = ciudad;
  document.getElementById('edit-comuna').value = comuna;

  document.getElementById('editProveedorForm').action = `/proveedor/editar/${id}/`;
});

deleteProveedorModal.addEventListener('show.bs.modal', function (event) {
  const button = event.relatedTarget;
  const id = button.getAttribute('data-id');
  const nombre = button.getAttribute('data-nombre');

  document.getElementById('delete-id').value = id;
  document.getElementById('delete-nombre').textContent = nombre;
  document.getElementById('deleteProveedorForm').action = `/proveedor/eliminar/${id}/`;
});

$(document).ready(function () {
  const table = $('.datatable').DataTable({
    language: {
      info: "Mostrando _START_ de _END_ | Total _TOTAL_ proveedor(es)",
      infoEmpty: "Sin proveedores para mostrar",
      lengthMenu: "Mostrar _MENU_ proveedores",
      search: "🔍 Buscar:",
      zeroRecords: "No se encontraron resultados.",
      infoFiltered: "(filtrado de un total de _MAX_ proveedor(es))",
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
      { orderable: false, targets: [1,2,7] }
    ],
  });

  $('#searchProveedores').on('keyup', function () {
    const val = this.value;
    table.search(val).draw();
  });
});

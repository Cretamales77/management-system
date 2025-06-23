document.addEventListener('DOMContentLoaded', function() {
    // Búsqueda de productos
    const searchInput = document.getElementById('buscarProducto');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('tbody tr');
            
            tableRows.forEach(row => {
                const productName = row.querySelector('td:first-child').textContent.toLowerCase();
                const productBrand = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
                
                if (productName.includes(searchTerm) || productBrand.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Configurar modal de editar precio
    const editPriceButtons = document.querySelectorAll('.btn-edit-precio');
    editPriceButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productoId = this.getAttribute('data-producto-id');
            const productoNombre = this.getAttribute('data-producto-nombre');
            const precioActual = this.getAttribute('data-precio-actual');
            const url = this.getAttribute('data-url');
            
            document.getElementById('edit-producto-id').value = productoId;
            document.getElementById('edit-precio-proveedor').value = precioActual;
            document.getElementById('editarPrecioForm').action = url;
        });
    });

    // Configurar modal de eliminar producto
    const deleteProductButtons = document.querySelectorAll('.btn-delete-producto');
    deleteProductButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productoId = this.getAttribute('data-producto-id');
            const productoNombre = this.getAttribute('data-producto-nombre');
            const url = this.getAttribute('data-url');
            
            document.getElementById('delete-producto-id').value = productoId;
            document.getElementById('deleteProductoName').textContent = productoNombre;
            document.getElementById('deleteProductoForm').action = url;
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
  
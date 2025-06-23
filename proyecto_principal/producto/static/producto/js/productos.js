// Abrir modal Añadir producto con botón
document.getElementById('addProductoBtn').addEventListener('click', () => {
  const addModal = new bootstrap.Modal(document.getElementById('addProductModal'));
  addModal.show();
});

let scannedCode = '';
let scanActive = false;
let scanMode = '';  // 'add' o 'search'

const scanModalEl = document.getElementById('scanCodeModal');
const scanModal = new bootstrap.Modal(scanModalEl);
const scanOptions = document.getElementById('scanOptions');
const scanCodeUI = document.getElementById('scanCodeUI');
const scanMsg = document.getElementById('scanMessage');
const searchInput = document.getElementById('searchProductos');

document.getElementById('scanCodeBtn').addEventListener('click', () => {
  scannedCode = '';
  scanActive = false;
  scanMode = '';
  scanMsg.style.display = 'none';
  scanMsg.textContent = '';

  scanOptions.style.display = 'block';
  scanCodeUI.style.display = 'none';

  scanModal.show();
});

document.getElementById('btnAddScan').addEventListener('click', () => {
  startScan('add');
});

document.getElementById('btnSearchScan').addEventListener('click', () => {
  startScan('search');
});

function startScan(mode) {
  scanMode = mode;
  scannedCode = '';
  scanActive = true;

  scanOptions.style.display = 'none';
  scanCodeUI.style.display = 'block';
  scanMsg.style.display = 'none';
  scanMsg.textContent = '';

  window.addEventListener('keydown', handleScan);

  scanModalEl.addEventListener('hidden.bs.modal', () => {
    scanActive = false;
    scanMode = '';
    window.removeEventListener('keydown', handleScan);
  }, { once: true });
}

function handleScan(e) {
  if (!scanActive) return;

  if (e.key === 'Enter') {
    if (scannedCode.trim() !== '') {
      e.preventDefault();

      if (scanMode === 'add') {
        $.ajax({
          url: validarCodigoUrl,
          data: { codigo: scannedCode.trim() },
          success: function(response) {
            if (response.existe) {
              scanMsg.textContent = "⚠️ El código ya existe en la base de datos.";
              scanMsg.style.display = 'block';
              scannedCode = '';
            } else {
              scanModal.hide();
              scanActive = false;
              window.removeEventListener('keydown', handleScan);

              setTimeout(() => {
                const addModal = new bootstrap.Modal(document.getElementById('addProductModal'));
                document.getElementById('add-codigo').value = scannedCode.trim();
                addModal.show();
              }, 300);
            }
          },
          error: function() {
            alert("Error al validar el código. Intenta nuevamente.");
          }
        });
      } else if (scanMode === 'search') {
        scanModal.hide();
        scanActive = false;
        window.removeEventListener('keydown', handleScan);

        searchInput.value = scannedCode.trim();
        searchInput.dispatchEvent(new Event('input'));
      }
    }
  } else {
    if (
      e.key.length === 1 &&
      !e.ctrlKey &&
      !e.altKey &&
      !e.metaKey &&
      e.key !== 'Shift'
    ) {
      scannedCode += e.key;
    }
  }
}

// Modales edición y eliminación
const editProductModal = document.getElementById('editProductModal');
const deleteProductModal = document.getElementById('deleteProductModal');

editProductModal.addEventListener('show.bs.modal', function (event) {
  const button = event.relatedTarget;
  const id = button.getAttribute('data-id');
  const nombre = button.getAttribute('data-nombre');
  const marca = button.getAttribute('data-marca');
  const descripcion = button.getAttribute('data-descripcion');
  const precio = button.getAttribute('data-precio');
  const stock = button.getAttribute('data-stock');
  const codigo = button.getAttribute('data-codigo');

  document.getElementById('edit-id').value = id;
  document.getElementById('edit-nombre').value = nombre;
  document.getElementById('edit-marca').value = marca;
  document.getElementById('edit-descripcion').value = descripcion;
  document.getElementById('edit-precio').value = Math.round(precio);
  document.getElementById('edit-stock').value = stock;
  document.getElementById('edit-codigo').value = codigo;

  document.getElementById('editProductForm').action = `/producto/editar/${id}/`;
});

deleteProductModal.addEventListener('show.bs.modal', function (event) {
  const button = event.relatedTarget;
  const id = button.getAttribute('data-id');
  const nombre = button.getAttribute('data-nombre');

  document.getElementById('delete-id').value = id;
  document.getElementById('delete-product-name').textContent = nombre;
  document.getElementById('deleteProductForm').action = `/producto/eliminar/${id}/`;
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
      { orderable: false, targets: [2, 7] }
    ],
  });

  $('#searchProductos').on('input', function () {
    const val = this.value.toLowerCase();

    $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
      const nombre = data[0].toLowerCase();
      const marca = data[1].toLowerCase();
      const codigo = data[3].toLowerCase();
      return nombre.includes(val) || marca.includes(val) || codigo.includes(val);
    });

    table.draw();
    $.fn.dataTable.ext.search.pop();
  });
});
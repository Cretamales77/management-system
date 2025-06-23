# 🏪 MANUAL DE USUARIO
## Sistema de Gestión de Ferretería

---

## 📋 ÍNDICE

1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Panel Principal](#panel-principal)
4. [Gestión de Productos](#gestión-de-productos)
5. [Gestión de Ventas](#gestión-de-ventas)
6. [Gestión de Compras](#gestión-de-compras)
7. [Gestión de Proveedores](#gestión-de-proveedores)
8. [Gestión de Categorías](#gestión-de-categorías)
9. [Gestión de Usuarios](#gestión-de-usuarios)
10. [Reportes y Estadísticas](#reportes-y-estadísticas)
11. [Configuración del Sistema](#configuración-del-sistema)
12. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 INTRODUCCIÓN

### **¿Qué es el Sistema de Gestión de Ferretería?**

El Sistema de Gestión de Ferretería es una aplicación web diseñada para administrar todos los aspectos de una ferretería de manera eficiente y organizada. Permite controlar inventario, ventas, compras, proveedores y generar reportes.

### **¿Quién puede usar este sistema?**

- **Vendedores**: Para registrar ventas y consultar productos
- **Almacenistas**: Para gestionar inventario y compras
- **Administradores**: Para configurar el sistema y generar reportes
- **Gerentes**: Para supervisar operaciones y tomar decisiones

### **Características principales**

- ✅ Control de inventario en tiempo real
- ✅ Registro de ventas con boletas
- ✅ Gestión de compras a proveedores
- ✅ Reportes y estadísticas
- ✅ Sistema de usuarios con diferentes permisos
- ✅ Interfaz intuitiva y fácil de usar

---

## 🔐 ACCESO AL SISTEMA

### **Paso 1: Abrir el navegador**
1. Abre tu navegador web (Chrome, Firefox, Edge, etc.)
2. Ve a la dirección del sistema (ejemplo: http://localhost:8000)

### **Paso 2: Página de inicio**
- Verás la página principal del sistema
- Haz clic en "Iniciar Sesión" o "Login"

### **Paso 3: Ingresar credenciales**
- **Usuario**: Tu nombre de usuario asignado
- **Contraseña**: Tu contraseña personal
- Haz clic en "Ingresar"

### **Paso 4: Panel principal**
- Una vez autenticado, verás el panel principal
- Desde aquí podrás acceder a todas las funciones

### **Cerrar sesión**
- Haz clic en tu nombre de usuario (esquina superior derecha)
- Selecciona "Cerrar Sesión"

---

## 🏠 PANEL PRINCIPAL

### **Descripción general**
El panel principal es tu punto de entrada al sistema. Aquí encontrarás:

- **Menú de navegación**: Acceso a todas las funciones
- **Resumen rápido**: Estadísticas importantes
- **Accesos directos**: Funciones más utilizadas

### **Elementos del panel**

#### **Barra superior**
- **Logo**: Identificación del sistema
- **Nombre de usuario**: Tu nombre y opciones de perfil
- **Notificaciones**: Alertas importantes del sistema

#### **Menú lateral**
- **Inicio**: Volver al panel principal
- **Productos**: Gestión de inventario
- **Ventas**: Registro y consulta de ventas
- **Compras**: Gestión de compras a proveedores
- **Proveedores**: Catálogo de proveedores
- **Categorías**: Organización de productos
- **Usuarios**: Gestión de usuarios del sistema
- **Estadísticas**: Reportes y análisis
- **Configuración**: Ajustes del sistema

#### **Área de contenido**
- Muestra la información y funciones de cada sección
- Cambia según la opción seleccionada en el menú

---

## 📦 GESTIÓN DE PRODUCTOS

### **Ver lista de productos**
1. En el menú lateral, haz clic en "Productos"
2. Verás una tabla con todos los productos
3. Puedes buscar productos usando el campo de búsqueda
4. Usa los filtros para encontrar productos específicos

### **Agregar nuevo producto**
1. Haz clic en el botón "Agregar Producto"
2. Completa el formulario con:
   - **Nombre**: Nombre del producto
   - **Descripción**: Descripción detallada
   - **Precio**: Precio de venta
   - **Stock**: Cantidad disponible
   - **Stock mínimo**: Cantidad mínima para alertas
   - **Categoría**: Categoría del producto
   - **Proveedor**: Proveedor principal
3. Haz clic en "Guardar"

### **Editar producto**
1. En la lista de productos, haz clic en "Editar"
2. Modifica los campos necesarios
3. Haz clic en "Guardar cambios"

### **Eliminar producto**
1. En la lista de productos, haz clic en "Eliminar"
2. Confirma la eliminación
3. **Nota**: Solo elimina si el producto ya no se vende

### **Consultar stock**
- El stock se muestra en tiempo real en la lista
- Productos con stock bajo aparecen en rojo
- Puedes ver el historial de movimientos de stock

---

## 💰 GESTIÓN DE VENTAS

### **Registrar nueva venta**
1. En el menú lateral, haz clic en "Ventas"
2. Haz clic en "Nueva Venta"
3. Completa el formulario:
   - **Cliente**: Nombre del cliente (opcional)
   - **Productos**: Selecciona los productos vendidos
   - **Cantidades**: Especifica las cantidades
   - **Precios**: Los precios se calculan automáticamente
4. Haz clic en "Finalizar Venta"

### **Proceso de venta paso a paso**

#### **Paso 1: Seleccionar productos**
- Busca productos por nombre o código
- Haz clic en "Agregar" para cada producto
- Especifica la cantidad

#### **Paso 2: Revisar la venta**
- Verifica los productos y cantidades
- Revisa los precios y totales
- Aplica descuentos si es necesario

#### **Paso 3: Finalizar venta**
- Confirma los datos del cliente
- Selecciona el método de pago
- Genera la boleta o factura

### **Consultar ventas**
1. En "Ventas", haz clic en "Lista de Ventas"
2. Verás todas las ventas registradas
3. Usa filtros para buscar ventas específicas:
   - Por fecha
   - Por cliente
   - Por monto
   - Por vendedor

### **Ver detalles de venta**
1. En la lista de ventas, haz clic en "Ver Detalle"
2. Verás:
   - Productos vendidos
   - Cantidades y precios
   - Total de la venta
   - Información del cliente
   - Fecha y hora

### **Imprimir boleta**
1. En los detalles de la venta, haz clic en "Imprimir"
2. Se abrirá una nueva ventana con la boleta
3. Usa la función de impresión del navegador

### **Procesar reembolso**
1. En la lista de ventas, busca la venta a reembolsar
2. Haz clic en "Reembolso"
3. Selecciona los productos a reembolsar
4. Confirma el reembolso

---

## 🛒 GESTIÓN DE COMPRAS

### **Registrar nueva compra**
1. En el menú lateral, haz clic en "Compras"
2. Haz clic en "Nueva Compra"
3. Completa el formulario:
   - **Proveedor**: Selecciona el proveedor
   - **Fecha de entrega**: Fecha esperada de entrega
   - **Productos**: Selecciona los productos a comprar
   - **Cantidades**: Especifica las cantidades
   - **Precios de compra**: Precios acordados con el proveedor

### **Proceso de compra paso a paso**

#### **Paso 1: Seleccionar proveedor**
- Busca el proveedor en la lista
- Verifica la información de contacto
- Revisa el historial de compras

#### **Paso 2: Agregar productos**
- Busca productos por nombre o categoría
- Especifica cantidades a comprar
- Ingresa precios de compra

#### **Paso 3: Revisar y confirmar**
- Verifica todos los productos y cantidades
- Revisa los totales
- Confirma la orden de compra

### **Consultar compras**
1. En "Compras", haz clic en "Lista de Compras"
2. Verás todas las compras registradas
3. Usa filtros para buscar compras específicas:
   - Por proveedor
   - Por fecha
   - Por estado (pendiente, entregada, cancelada)

### **Recibir compra**
1. Cuando llegue la mercancía, busca la compra en la lista
2. Haz clic en "Recibir"
3. Confirma las cantidades recibidas
4. El stock se actualizará automáticamente

### **Editar compra**
- Solo se pueden editar compras pendientes
- Haz clic en "Editar" en la lista de compras
- Modifica los productos o cantidades
- Guarda los cambios

---

## 👥 GESTIÓN DE PROVEEDORES

### **Ver lista de proveedores**
1. En el menú lateral, haz clic en "Proveedores"
2. Verás una tabla con todos los proveedores
3. Puedes buscar proveedores por nombre o categoría

### **Agregar nuevo proveedor**
1. Haz clic en "Agregar Proveedor"
2. Completa el formulario:
   - **Nombre**: Nombre de la empresa
   - **Contacto**: Nombre de la persona de contacto
   - **Teléfono**: Número de teléfono
   - **Email**: Correo electrónico
   - **Dirección**: Dirección física
   - **Categorías**: Productos que vende
3. Haz clic en "Guardar"

### **Editar proveedor**
1. En la lista de proveedores, haz clic en "Editar"
2. Modifica la información necesaria
3. Haz clic en "Guardar cambios"

### **Ver productos del proveedor**
1. En la lista de proveedores, haz clic en "Ver Productos"
2. Verás todos los productos que vende ese proveedor
3. Puedes ver precios y disponibilidad

### **Historial de compras**
1. En la lista de proveedores, haz clic en "Historial"
2. Verás todas las compras realizadas a ese proveedor
3. Incluye fechas, productos y montos

---

## 📂 GESTIÓN DE CATEGORÍAS

### **Ver categorías**
1. En el menú lateral, haz clic en "Categorías"
2. Verás una lista de todas las categorías
3. Cada categoría muestra la cantidad de productos

### **Agregar nueva categoría**
1. Haz clic en "Agregar Categoría"
2. Completa el formulario:
   - **Nombre**: Nombre de la categoría
   - **Descripción**: Descripción de la categoría
3. Haz clic en "Guardar"

### **Editar categoría**
1. En la lista de categorías, haz clic en "Editar"
2. Modifica el nombre o descripción
3. Haz clic en "Guardar cambios"

### **Ver productos por categoría**
1. En la lista de categorías, haz clic en "Ver Productos"
2. Verás todos los productos de esa categoría
3. Puedes agregar, editar o eliminar productos

### **Eliminar categoría**
- Solo se pueden eliminar categorías sin productos
- Haz clic en "Eliminar" en la lista
- Confirma la eliminación

---

## 👤 GESTIÓN DE USUARIOS

### **Ver usuarios del sistema**
1. En el menú lateral, haz clic en "Usuarios"
2. Verás una lista de todos los usuarios
3. Solo administradores pueden ver esta sección

### **Agregar nuevo usuario**
1. Haz clic en "Agregar Usuario"
2. Completa el formulario:
   - **Nombre**: Nombre completo
   - **Usuario**: Nombre de usuario para login
   - **Email**: Correo electrónico
   - **Contraseña**: Contraseña temporal
   - **Perfil**: Tipo de usuario (vendedor, administrador, etc.)
3. Haz clic en "Guardar"

### **Editar usuario**
1. En la lista de usuarios, haz clic en "Editar"
2. Modifica la información necesaria
3. Haz clic en "Guardar cambios"

### **Cambiar contraseña**
1. En la lista de usuarios, haz clic en "Cambiar Contraseña"
2. Ingresa la nueva contraseña
3. Confirma la contraseña
4. Haz clic en "Guardar"

### **Desactivar usuario**
1. En la lista de usuarios, haz clic en "Desactivar"
2. Confirma la desactivación
3. El usuario no podrá acceder al sistema

---

## 📊 REPORTES Y ESTADÍSTICAS

### **Acceder a reportes**
1. En el menú lateral, haz clic en "Estadísticas"
2. Verás diferentes tipos de reportes disponibles

### **Reporte de ventas**
- **Ventas por día**: Ventas realizadas en un día específico
- **Ventas por mes**: Resumen mensual de ventas
- **Productos más vendidos**: Ranking de productos
- **Ventas por vendedor**: Rendimiento de cada vendedor

### **Reporte de inventario**
- **Stock actual**: Cantidad de cada producto
- **Productos con stock bajo**: Productos que necesitan reposición
- **Movimientos de stock**: Entradas y salidas de productos
- **Valor del inventario**: Valor total del stock

### **Reporte de compras**
- **Compras por proveedor**: Compras realizadas a cada proveedor
- **Compras por mes**: Resumen mensual de compras
- **Productos más comprados**: Productos con más compras

### **Generar reportes**
1. Selecciona el tipo de reporte
2. Define el período de tiempo
3. Aplica filtros si es necesario
4. Haz clic en "Generar Reporte"
5. Descarga o imprime el reporte

### **Exportar datos**
- Los reportes se pueden exportar en diferentes formatos:
  - **PDF**: Para imprimir o compartir
  - **Excel**: Para análisis adicionales
  - **CSV**: Para importar en otros sistemas

---

## ⚙️ CONFIGURACIÓN DEL SISTEMA

### **Configuración de boletas**
1. En el menú lateral, haz clic en "Configuración"
2. Selecciona "Configuración de Boletas"
3. Personaliza:
   - **Encabezado**: Nombre de la empresa
   - **Pie de página**: Información adicional
   - **Logo**: Logo de la empresa
   - **Información fiscal**: Datos para facturación

### **Configuración de alertas**
1. En "Configuración", selecciona "Alertas"
2. Configura:
   - **Stock mínimo**: Cantidad mínima para alertas
   - **Notificaciones por email**: Alertas automáticas
   - **Recordatorios**: Recordatorios de tareas pendientes

### **Configuración de usuarios**
1. En "Configuración", selecciona "Usuarios"
2. Configura:
   - **Permisos**: Qué puede hacer cada tipo de usuario
   - **Contraseñas**: Políticas de contraseñas
   - **Sesiones**: Tiempo de inactividad

### **Respaldo de datos**
1. En "Configuración", selecciona "Respaldo"
2. Configura:
   - **Respaldo automático**: Frecuencia de respaldos
   - **Ubicación**: Dónde guardar los respaldos
   - **Retención**: Cuánto tiempo mantener respaldos

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### **Problemas de acceso**

#### **No puedo iniciar sesión**
- Verifica que el usuario y contraseña sean correctos
- Asegúrate de que la cuenta esté activa
- Contacta al administrador si olvidaste la contraseña

#### **Sesión expirada**
- Vuelve a iniciar sesión
- El sistema te redirigirá automáticamente

#### **Error de conexión**
- Verifica tu conexión a internet
- Intenta recargar la página
- Contacta al administrador del sistema

### **Problemas con productos**

#### **No encuentro un producto**
- Usa diferentes términos de búsqueda
- Verifica la categoría del producto
- Revisa si el producto está activo

#### **Error al agregar producto**
- Verifica que todos los campos obligatorios estén completos
- Asegúrate de que el precio sea un número válido
- Revisa que la categoría y proveedor existan

#### **Stock incorrecto**
- Verifica los movimientos de stock
- Revisa si hay ventas o compras pendientes
- Contacta al administrador si persiste el problema

### **Problemas con ventas**

#### **Error al registrar venta**
- Verifica que los productos tengan stock suficiente
- Asegúrate de que los precios sean correctos
- Revisa que todos los campos obligatorios estén completos

#### **No se genera la boleta**
- Verifica la configuración de impresoras
- Intenta imprimir desde otro navegador
- Contacta al administrador si persiste el problema

#### **Error en reembolso**
- Verifica que la venta no haya sido reembolsada antes
- Asegúrate de que las cantidades sean correctas
- Revisa que el producto esté en buen estado

### **Problemas con reportes**

#### **Reporte no se genera**
- Verifica que haya datos en el período seleccionado
- Asegúrate de tener permisos para ver el reporte
- Intenta con un período de tiempo diferente

#### **Datos incorrectos en reporte**
- Verifica que los filtros estén correctos
- Revisa que los datos de entrada sean correctos
- Contacta al administrador si persiste el problema

### **Contacto para soporte**

Si tienes problemas que no se resuelven con estas soluciones:

- **Email**: soporte@ferreteria.com
- **Teléfono**: (123) 456-7890
- **Horario**: Lunes a Viernes, 8:00 AM - 6:00 PM

Al contactar soporte, incluye:
1. Descripción detallada del problema
2. Pasos que seguiste
3. Capturas de pantalla si es posible
4. Tu nombre de usuario

---

## 📋 GLOSARIO DE TÉRMINOS

### **Términos del sistema**

- **Stock**: Cantidad de productos disponibles para venta
- **Stock mínimo**: Cantidad mínima que debe haber antes de hacer una compra
- **Venta**: Transacción donde se venden productos a un cliente
- **Compra**: Transacción donde se compran productos a un proveedor
- **Proveedor**: Empresa o persona que vende productos a la ferretería
- **Categoría**: Clasificación de productos (ej: herramientas, pinturas, etc.)
- **Boleta**: Documento que se entrega al cliente con los productos comprados
- **Reembolso**: Devolución de dinero al cliente por productos devueltos
- **Reporte**: Documento con información organizada del sistema

### **Términos de usuario**

- **Usuario**: Persona que usa el sistema
- **Contraseña**: Clave secreta para acceder al sistema
- **Sesión**: Período de tiempo que estás conectado al sistema
- **Perfil**: Tipo de usuario con permisos específicos
- **Permisos**: Qué funciones puede usar cada tipo de usuario

---

## 🎯 CONSEJOS DE USO

### **Para vendedores**
- Siempre verifica el stock antes de hacer una venta
- Usa la búsqueda para encontrar productos rápidamente
- Revisa los detalles de la venta antes de finalizar
- Mantén actualizada la información del cliente

### **Para almacenistas**
- Revisa diariamente los productos con stock bajo
- Registra las compras tan pronto lleguen los productos
- Verifica las cantidades recibidas contra la orden de compra
- Mantén organizadas las categorías de productos

### **Para administradores**
- Revisa los reportes regularmente
- Mantén actualizada la información de proveedores
- Configura las alertas de stock mínimo
- Realiza respaldos periódicos del sistema

### **Buenas prácticas generales**
- Cierra sesión cuando termines de trabajar
- No compartas tu contraseña con nadie
- Reporta problemas inmediatamente
- Mantén la información actualizada

---

## 📞 CONTACTO Y AYUDA

### **Canales de soporte**
- **Soporte técnico**: Para problemas del sistema
- **Capacitación**: Para aprender a usar nuevas funciones
- **Consultas**: Para dudas sobre el uso del sistema

### **Información de contacto**
- **Email**: soporte@ferreteria.com
- **Teléfono**: (123) 456-7890
- **WhatsApp**: +1 (123) 456-7890
- **Horario**: Lunes a Viernes, 8:00 AM - 6:00 PM

### **Recursos adicionales**
- **Videos tutoriales**: Disponibles en el sistema
- **Guías rápidas**: Para funciones específicas
- **FAQ**: Preguntas frecuentes

---

## 🎉 CONCLUSIÓN

Este manual te ayudará a usar el Sistema de Gestión de Ferretería de manera eficiente y efectiva. Recuerda que el sistema está diseñado para facilitar tu trabajo y mejorar la gestión de la ferretería.

Si tienes dudas o necesitas ayuda adicional, no dudes en contactar al soporte técnico.

**¡Gracias por usar el Sistema de Gestión de Ferretería!**

---

*Última actualización: [Fecha]*
*Versión del manual: 1.0*
*Sistema: Sistema de Gestión de Ferretería v1.0* 
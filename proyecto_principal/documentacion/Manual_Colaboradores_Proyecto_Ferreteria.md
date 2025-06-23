# 📋 MANUAL PARA COLABORADORES
## Sistema de Gestión de Ferretería

---

## 📋 ÍNDICE

1. [Introducción](#introducción)
2. [Configuración Inicial](#configuración-inicial)
3. [Flujo de Trabajo con Git](#flujo-de-trabajo-con-git)
4. [Cómo Revisar Pull Requests (Para Administradores)](#cómo-revisar-pull-requests-para-administradores)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Comandos Útiles](#comandos-útiles)
7. [Solución de Problemas](#solución-de-problemas)
8. [Buenas Prácticas](#buenas-prácticas)
9. [Contacto y Soporte](#contacto-y-soporte)

---

## 🎯 INTRODUCCIÓN

Este manual está diseñado para todos los colaboradores del proyecto **Sistema de Gestión de Ferretería**. Aquí encontrarás toda la información necesaria para configurar tu entorno de trabajo, entender el flujo de desarrollo y contribuir efectivamente al proyecto.

### **¿Qué es este proyecto?**
- Sistema web para gestión integral de una ferretería
- Desarrollado en Django (Python)
- Base de datos MySQL
- Control de versiones con Git y GitHub

### **¿Por qué es importante seguir este manual?**
- Mantener la calidad del código
- Evitar conflictos entre colaboradores
- Asegurar que todos trabajen de manera consistente
- Facilitar la integración de cambios

---

## ⚙️ CONFIGURACIÓN INICIAL

### **Paso 1: Instalar Software Necesario**

#### **Python 3.8 o superior**
1. Descarga desde: https://www.python.org/downloads/
2. Durante la instalación, marca "Add Python to PATH"
3. Verifica la instalación: `python --version`

#### **Git**
1. Descarga desde: https://git-scm.com/downloads
2. Instala con configuración por defecto
3. Verifica la instalación: `git --version`

#### **MySQL Server**
1. Descarga MySQL Community Server
2. Instala con configuración por defecto
3. Anota tu contraseña de root

#### **Editor de Código**
Recomendamos Visual Studio Code:
1. Descarga desde: https://code.visualstudio.com/
2. Instala las extensiones:
   - Python
   - Django
   - GitLens

### **Paso 2: Clonar el Repositorio**

```bash
# Clonar el repositorio
git clone https://github.com/Reta-001/management-system.git

# Entrar al directorio del proyecto
cd management-system/proyecto_principal
```

### **Paso 3: Configurar Entorno Virtual**

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate
```

### **Paso 4: Instalar Dependencias**

```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

### **Paso 5: Configurar Base de Datos**

1. **Crear base de datos MySQL:**
   ```sql
   CREATE DATABASE ferreteria_db;
   ```

2. **Configurar variables de entorno:**
   - Copia el archivo `env_example.txt` a `.env`
   - Edita `.env` con tus credenciales:
   ```env
   DEBUG=True
   SECRET_KEY=tu_clave_secreta_aqui
   DATABASE_NAME=ferreteria_db
   DATABASE_USER=tu_usuario_mysql
   DATABASE_PASSWORD=tu_password_mysql
   DATABASE_HOST=localhost
   DATABASE_PORT=3306
   ```

### **Paso 6: Ejecutar Migraciones**

```bash
# Aplicar migraciones de la base de datos
python manage.py migrate
```

### **Paso 7: Crear Superusuario (Opcional)**

```bash
# Crear usuario administrador
python manage.py createsuperuser
```

### **Paso 8: Ejecutar el Proyecto**

```bash
# Iniciar servidor de desarrollo
python manage.py runserver
```

El proyecto estará disponible en: http://127.0.0.1:8000/

---

## 🔄 FLUJO DE TRABAJO CON GIT

### **Conceptos Básicos**

#### **¿Qué son las ramas?**
- **`main`**: Rama principal (código estable)
- **Ramas de desarrollo**: Para trabajar en nuevas funcionalidades
- **Pull Request**: Solicitud para fusionar cambios

#### **¿Por qué usar ramas?**
- Trabajar sin afectar el código principal
- Revisar cambios antes de integrarlos
- Mantener el historial organizado

### **Flujo de Trabajo Diario**

#### **1. Actualizar tu rama local**
```bash
# Cambiar a la rama principal
git checkout main

# Obtener últimos cambios
git pull origin main

# Cambiar a tu rama de trabajo
git checkout tu-rama-de-trabajo

# Actualizar tu rama con los cambios de main
git merge main
```

#### **2. Trabajar en tu funcionalidad**
```bash
# Ver estado de cambios
git status

# Agregar archivos modificados
git add nombre_del_archivo.py
# O agregar todos los cambios
git add .

# Hacer commit con mensaje descriptivo
git commit -m "Agregar funcionalidad de reportes de ventas"

# Subir cambios a GitHub
git push origin tu-rama-de-trabajo
```

#### **3. Crear Pull Request**
1. Ve a GitHub: https://github.com/Reta-001/management-system
2. Haz clic en "Pull requests"
3. Haz clic en "New pull request"
4. Selecciona tu rama como origen
5. Escribe descripción clara de los cambios
6. Solicita revisión a un compañero

#### **4. Revisión y Aprobación**
- Otro colaborador revisa tu código
- Puede aprobar, solicitar cambios o comentar
- Una vez aprobado, se fusiona con `main`

### **Comandos de Ramas**

```bash
# Ver todas las ramas
git branch

# Crear nueva rama
git checkout -b nombre-nueva-rama

# Cambiar de rama
git checkout nombre-rama

# Eliminar rama (después de fusionar)
git branch -d nombre-rama
```

---

## 🔍 CÓMO REVISAR PULL REQUESTS (PARA ADMINISTRADORES)

### **¿Qué es un Pull Request (PR)?**

Un Pull Request es una **solicitud** que hace un colaborador para que sus cambios sean revisados y fusionados con la rama principal (`main`). Es como decir: *"Oye, revisa estos cambios que hice y dime si están bien para agregarlos al proyecto"*.

### **¿Por qué es importante revisar PRs?**

- **Calidad**: Asegurar que el código sea bueno
- **Seguridad**: Evitar errores que rompan el sistema
- **Consistencia**: Mantener el estilo de código uniforme
- **Aprendizaje**: Ayudar a mejorar el código de otros

---

### **PASO 1: Recibir Notificación de un PR**

#### **Opción A: Por Email**
1. GitHub te enviará un email automáticamente
2. El asunto será algo como: *"Reta-001 wants to merge 2 commits into main from feature-nueva-funcionalidad"*
3. Haz clic en el enlace del email

#### **Opción B: Desde GitHub**
1. Ve a tu repositorio: https://github.com/Reta-001/management-system
2. En la página principal, verás una sección **"Pull requests"**
3. Si hay PRs pendientes, verás un número en rojo
4. Haz clic en **"Pull requests"**

---

### **PASO 2: Abrir el Pull Request**

#### **Ver la lista de PRs**
```
┌─────────────────────────────────────────────────────────┐
│ 🔍 Pull requests (3)                                    │
├─────────────────────────────────────────────────────────┤
│ 🟢 feature/nueva-funcionalidad ← main                   │
│    "Agregar sistema de reportes de ventas"              │
│    Abierto hace 2 horas por Juan Pérez                  │
│                                                         │
│ 🟡 bugfix/correccion-error ← main                       │
│    "Corregir error en cálculo de totales"               │
│    Abierto hace 1 día por María García                  │
│                                                         │
│ 🔴 feature/login-mejorado ← main                        │
│    "Mejorar interfaz de login"                          │
│    Abierto hace 3 días por Carlos López                 │
└─────────────────────────────────────────────────────────┘
```

#### **Hacer clic en el PR que quieres revisar**
- Haz clic en el título del PR (línea azul)
- Se abrirá la página de revisión

---

### **PASO 3: Entender la Página del PR**

#### **Parte Superior - Información General**
```
┌─────────────────────────────────────────────────────────┐
│ 🟢 feature/nueva-funcionalidad ← main                   │
│                                                         │
│ ✅ Able to merge                                        │
│                                                         │
│ Agregar sistema de reportes de ventas                   │
│                                                         │
│ Este PR agrega una nueva funcionalidad para generar     │
│ reportes de ventas con gráficos y estadísticas.         │
│                                                         │
│ Cambios realizados:                                     │
│ - Nuevo modelo ReporteVenta                             │
│ - Vista para generar reportes                           │
│ - Template con gráficos                                 │
│ - Tests unitarios                                       │
│                                                         │
│ Closes #123                                             │
└─────────────────────────────────────────────────────────┘
```

#### **Parte Media - Archivos Modificados**
```
┌─────────────────────────────────────────────────────────┐
│ 📁 Files changed (5)                                    │
├─────────────────────────────────────────────────────────┤
│ + estadistica/models.py                                 │
│ + estadistica/views.py                                  │
│ + estadistica/templates/estadistica/reportes.html       │
│ + estadistica/tests.py                                  │
│ + proyecto_principal/urls.py                            │
└─────────────────────────────────────────────────────────┘
```

#### **Parte Inferior - Comentarios y Discusiones**
```
┌─────────────────────────────────────────────────────────┐
│ 💬 Conversation                                         │
├─────────────────────────────────────────────────────────┤
│ Juan Pérez: "Listo para revisión"                       │
│                                                         │
│ [No hay comentarios aún]                                │
└─────────────────────────────────────────────────────────┘
```

---

### **PASO 4: Revisar los Cambios**

#### **4.1 Ver el Resumen de Cambios**
- Haz clic en **"Files changed"** (pestaña)
- Verás todos los archivos que modificó el colaborador

#### **4.2 Revisar Cada Archivo**
```
┌─────────────────────────────────────────────────────────┐
│ 📄 estadistica/models.py                                │
│                                                         │
│ + class ReporteVenta(models.Model):                     │
│ +     fecha_inicio = models.DateField()                 │
│ +     fecha_fin = models.DateField()                    │
│ +     total_ventas = models.DecimalField()              │
│ +     cantidad_productos = models.IntegerField()        │
│ +     created_at = models.DateTimeField(auto_now_add=True) │
│                                                         │
│ +     class Meta:                                       │
│ +         verbose_name = "Reporte de Venta"             │
│ +         verbose_name_plural = "Reportes de Ventas"    │
│                                                         │
│ +     def __str__(self):                                │
│ +         return f"Reporte {self.fecha_inicio} - {self.fecha_fin}" │
└─────────────────────────────────────────────────────────┘
```

**¿Qué buscar en el código?**
- ✅ **Funcionalidad**: ¿Hace lo que dice que hace?
- ✅ **Calidad**: ¿El código está bien escrito?
- ✅ **Seguridad**: ¿Hay algún problema de seguridad?
- ✅ **Estilo**: ¿Sigue las convenciones del proyecto?

---

### **PASO 5: Hacer Comentarios (Opcional)**

#### **5.1 Comentar en una Línea Específica**
1. Haz clic en el número de línea que quieres comentar
2. Aparecerá un ícono de comentario (+)
3. Haz clic en el ícono
4. Escribe tu comentario
5. Haz clic en **"Add single comment"**

#### **Ejemplo de Comentario Útil**
```
Comentario en línea 15:
"Excelente uso de verbose_name para mejorar la interfaz de admin. 
Sugiero agregar también un método para calcular el promedio de ventas."
```

#### **5.2 Comentar en Todo el Archivo**
1. Ve al final del archivo
2. Verás una caja de comentarios
3. Escribe tu comentario general
4. Haz clic en **"Add review comment"**

---

### **PASO 6: Aprobar o Solicitar Cambios**

#### **6.1 Opciones de Revisión**
En la parte superior derecha del PR, verás un botón **"Review changes"**. Al hacer clic, tienes 3 opciones:

```
┌─────────────────────────────────────────────────────────┐
│ 📝 Review changes                                       │
├─────────────────────────────────────────────────────────┤
│ 💬 Comment                                              │
│    (Aprobar sin comentarios)                            │
│                                                         │
│ ✅ Approve                                              │
│    (Aprobar los cambios)                                │
│                                                         │
│ ❌ Request changes                                       │
│    (Solicitar cambios)                                  │
└─────────────────────────────────────────────────────────┘
```

#### **6.2 ¿Cuándo usar cada opción?**

**✅ Approve (Aprobar)**
- El código está perfecto
- No necesita cambios
- Cumple con los estándares del proyecto

**💬 Comment (Comentar)**
- El código está bien, pero tienes sugerencias
- Quieres felicitar al colaborador
- Tienes preguntas sobre la implementación

**❌ Request changes (Solicitar cambios)**
- Hay errores que deben corregirse
- El código no cumple con los estándares
- Falta documentación importante
- Hay problemas de seguridad

#### **6.3 Ejemplo de Revisión Aprobatoria**
```
✅ Approve

Excelente trabajo! El código está muy bien estructurado y sigue las mejores prácticas del proyecto.

Puntos positivos:
- Buena separación de responsabilidades
- Tests incluidos
- Documentación clara
- Nombres de variables descriptivos

Listo para merge! 🚀
```

#### **6.4 Ejemplo de Solicitud de Cambios**
```
❌ Request changes

El código tiene buenas ideas, pero necesita algunos ajustes antes de poder aprobarlo:

Cambios necesarios:
1. Agregar validación de fechas en el modelo
2. Incluir docstrings en los métodos
3. Agregar más tests para casos edge
4. Corregir el error de sintaxis en línea 45

Una vez corregidos estos puntos, estaré feliz de aprobar el PR.
```

---

### **PASO 7: Fusionar el PR (Merge)**

#### **7.1 Cuándo se puede fusionar**
- ✅ El PR tiene al menos 1 aprobación
- ✅ No hay conflictos de merge
- ✅ Todos los tests pasan (si están configurados)
- ✅ No hay solicitudes de cambios pendientes

#### **7.2 Cómo fusionar**
1. Haz clic en el botón verde **"Merge pull request"**
2. Escribe un mensaje de merge (opcional)
3. Haz clic en **"Confirm merge"**
4. El PR se cerrará automáticamente

#### **7.3 Después del merge**
- Los cambios aparecen en la rama `main`
- La rama del colaborador se puede eliminar
- Se puede crear un release si es necesario

---

### **PASO 8: Comunicación con el Equipo**

#### **8.1 Notificar al Colaborador**
- GitHub notifica automáticamente al colaborador
- Puedes agregar un comentario final
- Felicita el buen trabajo si es apropiado

#### **8.2 Ejemplo de Comentario Final**
```
¡Excelente trabajo! 🎉

El PR ha sido fusionado exitosamente. Los cambios ya están disponibles en la rama main.

Próximos pasos:
- Eliminar la rama feature/nueva-funcionalidad
- Actualizar la documentación si es necesario
- Considerar crear un release para esta funcionalidad

¡Gracias por tu contribución!
```

---

### **CONSEJOS PARA REVISORES**

#### **✅ Buenos Comentarios**
- **Específicos**: "En línea 25, considera usar `get_or_create()` en lugar de `get()`"
- **Constructivos**: "Esta función podría ser más eficiente si..."
- **Educativos**: "En Django, es mejor práctica usar..."
- **Amigables**: "¡Buena idea! Solo una pequeña sugerencia..."

#### **❌ Comentarios a Evitar**
- **Vagos**: "Esto no está bien"
- **Ataques personales**: "¿Cómo no sabes esto?"
- **Sin contexto**: "Cambia esto"
- **Demasiado críticos**: "Todo está mal"

#### **🎯 Criterios de Aprobación**
- **Funcionalidad**: ¿Hace lo que debe hacer?
- **Calidad**: ¿El código es legible y mantenible?
- **Tests**: ¿Hay tests para las nuevas funcionalidades?
- **Documentación**: ¿Está documentado lo necesario?
- **Seguridad**: ¿No hay vulnerabilidades obvias?

---

### **EJEMPLOS PRÁCTICOS DE REVISIÓN**

#### **Ejemplo 1: PR Perfecto**
```
✅ Approve

Código impecable! 

✅ Funcionalidad implementada correctamente
✅ Tests incluidos y pasando
✅ Documentación actualizada
✅ Sigue las convenciones del proyecto
✅ No hay problemas de seguridad

Listo para producción! 🚀
```

#### **Ejemplo 2: PR con Mejoras Menores**
```
💬 Comment

Muy buen trabajo! El código está bien estructurado y funcional.

Sugerencias menores para futuras mejoras:
- Considerar agregar logging para debugging
- Podrías usar type hints para mejor documentación
- El nombre de la variable `x` podría ser más descriptivo

Pero en general, excelente implementación. ¡Aprobado! 👍
```

#### **Ejemplo 3: PR que Necesita Cambios**
```
❌ Request changes

El código tiene buenas ideas, pero necesita correcciones importantes:

Cambios requeridos:
1. **Error crítico**: Línea 45 - `print()` en producción debe ser `logger.info()`
2. **Seguridad**: Línea 78 - Validar input del usuario antes de procesar
3. **Tests**: Agregar tests para el caso cuando no hay datos
4. **Documentación**: Agregar docstring al método `calcular_total()`

Una vez corregidos estos puntos, estaré feliz de revisar nuevamente.

Gracias por tu trabajo! 💪
```

---

### **HERRAMIENTAS ÚTILES PARA REVISIÓN**

#### **GitHub Desktop**
- Interfaz gráfica para revisar cambios
- Más fácil para principiantes
- Descarga desde: https://desktop.github.com/

#### **Extensiones de Navegador**
- **GitHub Pull Request Manager**: Mejora la interfaz de PRs
- **Octotree**: Navegación de archivos más fácil

#### **Comandos Git Útiles**
```bash
# Ver cambios de un PR localmente
git fetch origin
git checkout -b review-pr-123 origin/feature/nueva-funcionalidad

# Probar los cambios
python manage.py test
python manage.py runserver
```

---

### **RESOLUCIÓN DE CONFLICTOS**

#### **¿Qué son los conflictos?**
Cuando dos personas modifican la misma línea del mismo archivo, Git no sabe cuál cambio mantener.

#### **Cómo resolver conflictos**
1. **GitHub te avisará** si hay conflictos
2. **No podrás hacer merge** hasta resolverlos
3. **El colaborador debe resolver** los conflictos en su rama
4. **Una vez resueltos**, podrás hacer merge

#### **Ayudar a resolver conflictos**
- Comunicarse con el colaborador
- Explicar qué cambios son más importantes
- Revisar la resolución final

---

### **MÉTRICAS DE REVISIÓN**

#### **Tiempo de Respuesta**
- **Ideal**: Responder en 24 horas
- **Máximo**: 3-5 días
- **Urgente**: Responder el mismo día

#### **Calidad de Revisión**
- **Revisar todo el código**: No solo los archivos principales
- **Probar funcionalidad**: Si es posible, ejecutar el código
- **Verificar tests**: Asegurar que los tests pasen
- **Revisar documentación**: Verificar que esté actualizada

---

### **COMUNICACIÓN EFECTIVA**

#### **Lenguaje Positivo**
- **En lugar de**: "Esto está mal"
- **Usar**: "Podríamos mejorar esto de la siguiente manera..."

#### **Ser Específico**
- **En lugar de**: "Arregla esto"
- **Usar**: "En la línea 45, cambia `x` por `total_ventas`"

#### **Reconocer el Esfuerzo**
- **Siempre**: Agradecer el trabajo del colaborador
- **Destacar**: Los puntos positivos del código
- **Motivar**: Para futuras contribuciones

---

## 📁 ESTRUCTURA DEL PROYECTO

```
proyecto_principal/
├── categoria/              # Gestión de categorías de productos
│   ├── models.py          # Modelos de categorías
│   ├── views.py           # Vistas de categorías
│   ├── urls.py            # URLs de categorías
│   └── templates/         # Plantillas HTML
│
├── compras/               # Sistema de compras a proveedores
│   ├── models.py          # Modelos de compras
│   ├── views.py           # Vistas de compras
│   ├── forms.py           # Formularios de compras
│   └── templates/         # Plantillas HTML
│
├── estadistica/           # Reportes y estadísticas
│   ├── views.py           # Vistas de reportes
│   └── templates/         # Plantillas HTML
│
├── home/                  # Página principal y modelos base
│   ├── models.py          # Modelos principales (Producto, Venta, etc.)
│   ├── views.py           # Vistas principales
│   └── templates/         # Plantillas principales
│
├── producto/              # Gestión de productos
│   ├── models.py          # Modelos de productos
│   ├── views.py           # Vistas de productos
│   └── templates/         # Plantillas HTML
│
├── proveedor/             # Gestión de proveedores
│   ├── models.py          # Modelos de proveedores
│   ├── views.py           # Vistas de proveedores
│   └── templates/         # Plantillas HTML
│
├── usuario/               # Sistema de usuarios y autenticación
│   ├── models.py          # Modelos de usuarios
│   ├── views.py           # Vistas de autenticación
│   └── templates/         # Plantillas de login
│
├── venta/                 # Sistema de ventas y boletas
│   ├── models.py          # Modelos de ventas
│   ├── views.py           # Vistas de ventas
│   └── templates/         # Plantillas HTML
│
└── proyecto_principal/    # Configuración principal de Django
    ├── settings.py        # Configuración del proyecto
    ├── urls.py            # URLs principales
    └── wsgi.py            # Configuración WSGI
```

### **Archivos Importantes**

- **`manage.py`**: Comando principal de Django
- **`requirements.txt`**: Lista de dependencias Python
- **`.env`**: Variables de entorno (no subir al repositorio)
- **`.gitignore`**: Archivos que Git debe ignorar
- **`README.md`**: Documentación del proyecto

---

## 📝 COMANDOS ÚTILES

### **Comandos de Django**

```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Crear migraciones después de cambios en modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar tests
python manage.py test

# Recolectar archivos estáticos
python manage.py collectstatic

# Shell de Django (para pruebas)
python manage.py shell
```

### **Comandos de Git**

```bash
# Ver estado del repositorio
git status

# Ver historial de commits
git log --oneline

# Ver diferencias en archivos
git diff

# Ver ramas
git branch

# Cambiar de rama
git checkout nombre-rama

# Crear nueva rama
git checkout -b nueva-rama

# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción del cambio"

# Subir cambios
git push origin nombre-rama

# Obtener cambios del repositorio
git pull origin nombre-rama

# Ver configuración de Git
git config --list
```

### **Comandos de Python**

```bash
# Ver versión de Python
python --version

# Instalar paquete
pip install nombre-paquete

# Listar paquetes instalados
pip list

# Actualizar pip
python -m pip install --upgrade pip

# Crear entorno virtual
python -m venv nombre-entorno

# Activar entorno virtual (Windows)
nombre-entorno\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source nombre-entorno/bin/activate
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### **Problemas Comunes y Soluciones**

#### **Error: "git no se reconoce como comando"**
**Solución:**
- Verificar que Git esté instalado
- Reiniciar la terminal
- Agregar Git al PATH del sistema

#### **Error: "ModuleNotFoundError"**
**Solución:**
```bash
# Activar entorno virtual
venv\Scripts\activate

# Reinstalar dependencias
pip install -r requirements.txt
```

#### **Error: "Database connection failed"**
**Solución:**
- Verificar que MySQL esté corriendo
- Revisar credenciales en `.env`
- Ejecutar `python manage.py migrate`

#### **Error: "Port already in use"**
**Solución:**
```bash
# Usar puerto diferente
python manage.py runserver 8001

# O matar proceso en puerto 8000
netstat -ano | findstr :8000
taskkill /PID numero_proceso /F
```

#### **Error: "Permission denied"**
**Solución:**
- Ejecutar terminal como administrador
- Verificar permisos de archivos
- Cambiar permisos si es necesario

#### **Error: "Merge conflict"**
**Solución:**
1. Abrir archivos con conflictos
2. Buscar marcadores `<<<<<<<`, `=======`, `>>>>>>>`
3. Resolver conflictos manualmente
4. Guardar archivos
5. Hacer commit de la resolución

### **Comandos de Diagnóstico**

```bash
# Ver información del sistema
systeminfo

# Ver procesos corriendo
tasklist

# Ver puertos en uso
netstat -ano

# Ver espacio en disco
dir

# Ver variables de entorno
echo %PATH%
```

---

## ✅ BUENAS PRÁCTICAS

### **Al Escribir Código**

1. **Usar nombres descriptivos**
   ```python
   # ❌ Malo
   def f(x):
       return x * 2

   # ✅ Bueno
   def calcular_precio_con_iva(precio):
       return precio * 1.19
   ```

2. **Comentar código complejo**
   ```python
   # Calcular descuento por cantidad
   if cantidad >= 10:
       descuento = 0.15  # 15% de descuento para compras grandes
   ```

3. **Manejar errores**
   ```python
   try:
       producto = Producto.objects.get(id=producto_id)
   except Producto.DoesNotExist:
       return HttpResponse("Producto no encontrado", status=404)
   ```

### **Al Trabajar con Git**

1. **Hacer commits frecuentes y pequeños**
   ```bash
   # ❌ Malo
   git commit -m "Cambios"

   # ✅ Bueno
   git commit -m "Agregar validación de stock mínimo en productos"
   ```

2. **Usar ramas descriptivas**
   ```bash
   # ❌ Malo
   git checkout -b rama1

   # ✅ Bueno
   git checkout -b feature/reporte-ventas-mensual
   ```

3. **Revisar cambios antes de commit**
   ```bash
   git status
   git diff
   ```

### **Al Trabajar en Equipo**

1. **Comunicar cambios importantes**
2. **Revisar código de otros**
3. **Ayudar a resolver problemas**
4. **Documentar decisiones importantes**

### **Seguridad**

1. **Nunca subir contraseñas al repositorio**
2. **Usar variables de entorno para configuraciones sensibles**
3. **Mantener dependencias actualizadas**
4. **Revisar código antes de fusionar**

---

## 📞 CONTACTO Y SOPORTE

### **Canales de Comunicación**

- **GitHub Issues**: Para reportar bugs o solicitar funcionalidades
- **WhatsApp/Telegram**: Para comunicación rápida del equipo
- **Reuniones semanales**: Para coordinar trabajo

### **Recursos Útiles**

- **Documentación de Django**: https://docs.djangoproject.com/
- **Tutorial de Git**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/

### **Contacto del Equipo**

- **Líder del Proyecto**: [Nombre y contacto]
- **Desarrollador Senior**: [Nombre y contacto]
- **Soporte Técnico**: [Nombre y contacto]

### **Reportar Problemas**

Al reportar un problema, incluye:
1. Descripción clara del problema
2. Pasos para reproducirlo
3. Capturas de pantalla si es necesario
4. Información del sistema (SO, versión de Python, etc.)

---

## 📋 CHECKLIST DE CONFIGURACIÓN

### **Para Nuevos Colaboradores**

- [ ] Python 3.8+ instalado
- [ ] Git instalado y configurado
- [ ] MySQL instalado y configurado
- [ ] Editor de código instalado
- [ ] Repositorio clonado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] Base de datos configurada
- [ ] Migraciones aplicadas
- [ ] Proyecto ejecutándose correctamente
- [ ] Acceso al repositorio de GitHub
- [ ] Rama de trabajo creada

### **Antes de Cada Sesión de Trabajo**

- [ ] Entorno virtual activado
- [ ] Rama actualizada con `main`
- [ ] Cambios guardados y committeados
- [ ] Pull Request creado si es necesario

### **Para Administradores - Revisión de PRs**

- [ ] Revisar todos los archivos modificados
- [ ] Verificar que la funcionalidad sea correcta
- [ ] Comprobar que los tests pasen
- [ ] Revisar la documentación
- [ ] Aprobar o solicitar cambios
- [ ] Comunicar la decisión al colaborador
- [ ] Fusionar el PR si está aprobado

---

## 🎉 CONCLUSIÓN

Siguiendo este manual, podrás trabajar de manera eficiente y colaborativa en el proyecto. Recuerda que la comunicación y el trabajo en equipo son fundamentales para el éxito del proyecto.

**¡Gracias por contribuir al Sistema de Gestión de Ferretería!**

---

*Última actualización: [Fecha]*
*Versión del manual: 1.0* 
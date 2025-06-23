from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Usuario
import random

def login(request):
    # Respuesta temporal para diagnosticar
    return HttpResponse("Página de login funcionando correctamente")
    
    if request.session.get('usuario_id'):
        return redirect('main')  

    if request.method == 'POST':
        nombre = request.POST.get('username', '').strip()
        clave = request.POST.get('password', '').strip()

        usuario = Usuario.objects.filter(nombre_usuario=nombre).first()

        if usuario and usuario.check_password(clave):
            request.session['usuario_id'] = usuario.id_usuario
            request.session['usuario_nombre'] = usuario.nombre_usuario
            request.session['correo_usuario'] = usuario.correo
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('main')  
        
        messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'usuario/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def verificacion(request):
    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()

        if not correo:
            messages.error(request, 'Debes ingresar un correo.')
            return render(request, 'usuario/verificacion.html')

        try:
            validate_email(correo)
        except ValidationError:
            messages.error(request, 'El correo no tiene un formato válido.')
            return render(request, 'usuario/verificacion.html')

        usuario = Usuario.objects.filter(correo__iexact=correo).first()
        if not usuario:
            messages.error(request, 'Este correo no está autorizado para registrar nuevos usuarios.')
            return render(request, 'usuario/verificacion.html')

        codigo = str(random.randint(100000, 999999))
        request.session.update({
            'codigo_enviado': codigo,
            'correo': correo.lower()
        })

        try:
            send_mail(
                'Código de verificación para crear usuario',
                f'Tu código de verificación es: {codigo}',
                settings.EMAIL_HOST_USER,
                [correo]
            )
            messages.success(request, 'Código enviado correctamente. Revisa tu correo autorizado.')
            return redirect('verificar')
        except Exception as e:
            messages.error(request, f'Error al enviar el correo: {e}')

    return render(request, 'usuario/verificacion.html')

def verificar(request):
    if request.method == 'POST':
        codigo_usuario = request.POST.get('codigo', '').strip()
        codigo_correcto = request.session.get('codigo_enviado')

        if codigo_usuario == codigo_correcto:
            request.session['verificado'] = True
            messages.success(request, 'Código verificado correctamente.')
            return redirect('recuperar')

        messages.error(request, 'Código incorrecto. Intenta de nuevo.')

    return render(request, 'usuario/verificar.html')

def recuperar(request):
    if request.method == 'POST':
        nueva_password = request.POST.get('password', '').strip()
        confirmar_password = request.POST.get('password2', '').strip()

        if not nueva_password or not confirmar_password:
            messages.error(request, 'Completa todos los campos.')
        elif nueva_password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            correo = request.session.get('correo')
            usuario = Usuario.objects.filter(correo=correo).first()

            if usuario:
                usuario.set_password(nueva_password)
                usuario.save()

                request.session.flush()
                messages.success(request, 'Contraseña actualizada exitosamente.')
                return redirect('login')

            messages.error(request, 'No existe ningún usuario registrado con ese correo.')

    return render(request, 'usuario/recuperar.html')

def lista_perfiles(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    
    usuarios = Usuario.objects.all()
    nombre_usuario = request.session.get('usuario_nombre', 'Invitado')
    return render(request, 'usuario/perfiles/lista_perfiles.html', {
        'usuarios': usuarios,
        'nombre_usuario': nombre_usuario
    })

def nuevo_perfil(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    
    if request.method == 'POST':
        nombre = request.POST.get('username', '').strip()
        correo = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('password2', '').strip()

        if not all([nombre, correo, password, confirm_password]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'usuario/perfiles/nuevo_perfil.html')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'usuario/perfiles/nuevo_perfil.html')

        if Usuario.objects.filter(nombre_usuario=nombre).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return render(request, 'usuario/perfiles/nuevo_perfil.html')

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'usuario/perfiles/nuevo_perfil.html')

        try:
            usuario = Usuario.objects.create(
                nombre_usuario=nombre,
                correo=correo
            )
            usuario.set_password(password)
            usuario.save()
            messages.success(request, 'Perfil creado exitosamente.')
            return redirect('lista_perfiles')
        except Exception as e:
            messages.error(request, f'Error al crear el perfil: {str(e)}')

    return render(request, 'usuario/perfiles/nuevo_perfil.html')

def editar_perfil(request, id_usuario):
    if not request.session.get('usuario_id'):
        return redirect('login')
    
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    
    if request.method == 'POST':
        nombre = request.POST.get('username', '').strip()
        correo = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('password2', '').strip()

        if not all([nombre, correo]):
            messages.error(request, 'El nombre de usuario y correo son obligatorios.')
            return render(request, 'usuario/perfiles/editar_perfil.html', {'usuario': usuario})

        # Verificar si el nombre de usuario ya existe (excluyendo el usuario actual)
        if Usuario.objects.filter(nombre_usuario=nombre).exclude(id_usuario=id_usuario).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return render(request, 'usuario/perfiles/editar_perfil.html', {'usuario': usuario})

        # Verificar si el correo ya existe (excluyendo el usuario actual)
        if Usuario.objects.filter(correo=correo).exclude(id_usuario=id_usuario).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'usuario/perfiles/editar_perfil.html', {'usuario': usuario})

        try:
            usuario.nombre_usuario = nombre
            usuario.correo = correo
            
            # Actualizar contraseña solo si se proporciona una nueva
            if password and confirm_password:
                if password != confirm_password:
                    messages.error(request, 'Las contraseñas no coinciden.')
                    return render(request, 'usuario/perfiles/editar_perfil.html', {'usuario': usuario})
                usuario.set_password(password)
            
            usuario.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('lista_perfiles')
        except Exception as e:
            messages.error(request, f'Error al actualizar el perfil: {str(e)}')

    return render(request, 'usuario/perfiles/editar_perfil.html', {'usuario': usuario})

def eliminar_perfil(request, id_usuario):
    if not request.session.get('usuario_id'):
        return redirect('login')
    
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    
    if request.method == 'POST':
        try:
            usuario.delete()
            messages.success(request, 'Perfil eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el perfil: {str(e)}')
    
    return redirect('lista_perfiles')



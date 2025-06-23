from .models import Profile, Bitacora, User
from .forms import ProfileForm

from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from openpyxl import Workbook
#from argon.apps.tasks.views import tareas

# Create your views here.
@login_required
def dashboard(request):
    return render(request,'dashboard.html')

#para la vista de "TABLES"
@login_required
def tables(request):
    bitacoras = Bitacora.objects.all()
    profile_list = Profile.objects.all().order_by('name')
    #profile_list = Profile.objects.filter(estatus=True).order_by('name')
    bitacora_list = Bitacora.objects.all()

    search_query = request.GET.get('filter','')
    if search_query:
        profile_list = profile_list.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Paginación de perfiles
    profile_paginator = Paginator(profile_list, 3)
    profile_page_number = request.GET.get('profile_page')
    profiles = profile_paginator.get_page(profile_page_number)

    # Paginación de bitácoras
    bitacora_paginator = Paginator(bitacora_list, 5)
    bitacora_page_number = request.GET.get('bitacora_page')
    bitacoras = bitacora_paginator.get_page(bitacora_page_number)

    context={
        'bitacoras':bitacoras,
        'profiles': profiles,
        'search_query': search_query
    }
    return render(request, 'tables.html',context) 

#para la vista de "PROFILE"
@login_required
def profile(request):
    profile = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile) #SE AGREGO UNA INSTANCIA, ES DECIR "SI NO EXISTE EL PERFIL LO CREA Y SI YA EXISTE LO MODIFICA"
        if form.is_valid():
            #ESTOS SE SACAN DEL IF IS NONE, PARA QUE PERMITA CREAR Y ACTUALIZAR LOS DATOS
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            if profile is None:
                #sI SE QUEDAN AQUI NO EDITARA EL PERFIL
        
                messages.success(request, f'Perfil creado con exito: {new_profile.name}')
                Bitacora.objects.create(movimiento=f"Se creó el perfil: {new_profile.name}")
            else:
                #AQUI SE COMPARA, SI YA EXISTE LO MODIFICA 
                messages.success(request, f'Perfil actualizado: {new_profile.name}')   
                Bitacora.objects.create(movimiento=f"Perfil actualizado: {new_profile.name}")
            return redirect('profile')
    context = {
        'profile': profile
    }
    return render(request, 'profile.html', context)


#PARA EDITAR UN PERFIL
@login_required
def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            update_profile = form.save(commit=False)
            update_profile.estatus = True 
            update_profile.save()
            # Bitácora
            Bitacora.objects.create(
                movimiento=f"Perfil Actualizado: {update_profile.name} con teléfono {update_profile.phone}"
            )
            return redirect('tables')  
        else:
            print("NO SE ACTUALIZARON LOS DATOS, INTENTE OTRA VEZ")
    else:
        form = ProfileForm(instance=profile)
    context = {
        'profile': profile,
        'form': form  
    }
    return render(request, 'edit_profile.html', context)

#PARA ELIMINAR UN PERFIL
@login_required
def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    profile.estatus = False
    Bitacora.objects.create(
        movimiento=f"Perfil Eliminado: {profile.name} con teléfono {profile.phone}"
    )
    return redirect('tables')

#PARA GENERAR EL REPORTE 
@login_required
def report(request):
    profiles = Profile.objects.filter(estatus=True).order_by('name')
    time = timezone.now().date()
    wb = Workbook()
    ws = wb.active
    ws.append(['Username', 'Name', 'Teléfono', 'Correo','Estatus'])

    for profile in profiles:
        ws.append([profile.username, profile.name, profile.phone, profile.email, profile.estatus])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=profiles-{time}.xlsx'
    wb.save(response)

    return response

#GENERAR REPORTE DE BITACORA
@login_required
def reportbit(request):
    bitacoras = Bitacora.objects.all().order_by('fecha')
    time = timezone.now().date()

    wb = Workbook()
    ws = wb.active
    ws.title = "Bitácora"

    ws.append(['movimiento', 'fecha'])

    for bitacora in bitacoras:
        ws.append([bitacora.movimiento,bitacora.fecha.strftime('%Y-%m-%d %H:%M:%S')])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=bitacora-{time}.xlsx'
    wb.save(response)

    return response

#para la vista de SING UP
def signup(request):
    if request.method == 'GET':
        return render(request, 'sign-up.html',{
            'form': UserCreationForm()
        })
    else:
        print(request.POST)
        if  request.POST['password1'] == request.POST['password2']:
            try:
                user= User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                
                Bitacora.objects.create(
                    user= user,
                    movimiento=f"Registro exitoso: {user.username}"
                ) 
                return redirect('profile')
            except:
                Bitacora.objects.create(
                    user= None,
                    movimiento=f"Intento Fallido: {request.POST['username']}, usuario ya existe"
                )
                return render(request, 'sign-up.html',{'error_exists': "usuario ya existe"}) 
        else:
            Bitacora.objects.create(
                user= None,
                movimiento=f"Intento de registro fallido:{request.POST['username']}. Las contraseñas no coinciden"
            )
            return render(request, 'sign-up.html',{
                    'error_exists': "Las contraseñas no coinciden "
                })   

#para la vista de SING IN
def signin(request):
    if request.method == 'GET':
        return render(request, 'sign-in.html') 
    else:
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is None:
            Bitacora.objects.create(
                    user= None,
                    movimiento=f"Intento de sesión fallido:{username}"
                )
            return render(request,'sign-in.html', { 'error_match': 'Usuario o contraseña son incorrectas'})
        else:
            Bitacora.objects.create(
                    user= user,
                    movimiento=f"Intento de sesión éxitoso:{username}"
                )
            login(request,user)
            return redirect('profile')

@login_required
def close(request):
    if request.user.is_authenticated:
        username = request.user.username
        Bitacora.objects.create(user=request.user, movimiento=f"Cierra sesión: {username}")
    
    logout(request)
    return redirect('signin')

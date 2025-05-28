from django.shortcuts import render, redirect
from .models import Profile, Bitacora
from .forms import ProfileForm

# Create your views here.
def dashboard(request):
    return render(request,'dashboard.html')

#para la vista de "TABLES"
def tables(request):
    return render(request, 'tables.html') 

#para la vista de "PROFILE"
def profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        new_profile = form.save(commit=False)
        print(request.POST, request.FILES)
        new_profile.save()

        # BITÁCORA
        Bitacora.objects.create(
            movimiento=f"Se creó el perfil: {new_profile.name}"
        )

        return redirect('profile')
    else:
        print('NO ESTA MOSTRANDO LOS DATOS')

    context = {
        'form': form
    }

    return render(request, 'profile.html', context)




#para la vista de SING UP
def signup(request):
    return render(request, 'sign-up.html') 

#para la vista de SING UP
def signin(request):
    return render(request, 'sign-in.html') 
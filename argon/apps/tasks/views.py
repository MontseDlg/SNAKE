from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Task

def tareas(request):
    search_query = request.GET.get('search', '')
    profile_id = request.GET.get('profile', None)  # Puedes recibir el perfil para filtrar tareas

    tasks = Task.objects.all()

    if search_query:
        tasks = tasks.filter(Q(nombre__icontains=search_query))

    paginator = Paginator(tasks, 3)  # 3 tareas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tasks': page_obj,   # Aquí se pasa el objeto paginado
        'search_query': search_query,  # Por si quieres mostrar el filtro aplicado
    }
    return render(request, 'tareas.html', context)

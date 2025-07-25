"""
URL configuration for argon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path,include
from argon.apps.dashboard import views
from argon.apps.tasks import views as task_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboard,name='dashboard'),
    path('tables/', views.tables, name='tables'),
    path('profile/', views.profile,name='profile'),
    path('edit_profile/<int:profile_id>', views.edit_profile, name='edit_profile'),
    path('delete_profile/<int:profile_id>', views.delete_profile, name='delete_profile'),
    path('export/', views.report, name='report-general'),
    path('exportbit/', views.reportbit, name='report-movimiento'),
    path('sign-up/', views.signup,name='signup'),
    path('sign-in/', views.signin,name='signin'),
    path('close/',views.close,name='close'),
    path('tareas/', task_views.tareas, name='tareas'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Inclui as URLs do aplicativo de usuários
    path('', RedirectView.as_view(url='/users/login/', permanent=False)),  # Redireciona para a página de login
]

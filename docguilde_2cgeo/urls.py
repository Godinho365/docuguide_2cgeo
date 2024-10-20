from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site  # Importando o site do Filebrowser, se necessário

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/filebrowser/', site.urls),  # URLs do Filebrowser, se necessário
    path('users/', include('users.urls')),  # Inclui as URLs do aplicativo de usuários
    path('', RedirectView.as_view(url='/users/login/', permanent=False)),  # Redireciona para a página de login
    path('instructions/', include('instructions.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # URLs do CKEditor
    path('tasks/', include('tasks.urls')),
    path('servers/', include('servers.urls')),
]

# Adiciona suporte para arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

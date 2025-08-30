from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chatbot.views import chat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cars.urls')),
    path('chat/', chat_view, name='chat'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
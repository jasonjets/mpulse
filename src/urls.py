from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.shortcuts import render

# Page not found handler
def handler404(request, exception):
    print('True')
    return render(request, '404.html')


urlpatterns = [
    path('', include('mpulse.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = handler404

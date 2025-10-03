from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from gestion.forms import LoginBootstrapForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='registro/login.html',
        authentication_form=LoginBootstrapForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

from django.conf.urls import handler403
handler403 = 'gestion.views.acceso_denegado'

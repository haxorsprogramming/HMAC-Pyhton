from django.contrib import admin
from django.urls import path

from main_app import views as main_app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_app.login_page),
    path('login/proses', main_app.login_proses),
    path('main_app/beranda', main_app.beranda),
    path('dashboard/beranda', main_app.beranda_kita)
]

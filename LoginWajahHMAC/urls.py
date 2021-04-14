from django.contrib import admin
from django.urls import path

from main_app import views as main_app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_app.login_page),
    path('login/proses', main_app.login_proses),
    path('login/identifikasi-wajah', main_app.identifikasi_wajah),
    path('main_app/beranda', main_app.beranda),
    path('dashboard/beranda', main_app.beranda_kita),
    path('dashboard/manajemen-pegawai', main_app.manajemen_pegawai),
    path('dashboard/proses-tambah-pegawai', main_app.proses_tambah_pegawai),
    path('login/get-data-pegawai', main_app.get_data_pegawai)
]

from django.contrib import admin
from django.urls import path

from main_app import views as main_app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_app.login_page)
]

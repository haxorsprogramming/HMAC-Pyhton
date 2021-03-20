from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import hashlib
import json

from .models import Akses_Login
from .models import Pegawai

# Create your views here.
def login_page(request):
    ip_address = request.META['REMOTE_ADDR']
    context = {
        'aplikasi' : '-',
        'developer' : 'Nurul Pratiwi',
        'ip_address' : ip_address
    }
    return render(request, 'login_page/login_page.html', context)

@csrf_exempt
def login_proses(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    pass_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
    total_user = Akses_Login.objects.filter(username__contains=username).count()
    if total_user > 0 :
        data_user = Akses_Login.objects.filter(username__contains=username).first()
        kd_pegawai = data_user.kd_pegawai
        password_db = data_user.kata_sandi
        if pass_hash == password_db : 
            data_pegawai = Pegawai.objects.filter(kd_pegawai__contains=kd_pegawai).first()
            nama_pegawai = data_pegawai.nama_pegawai
            status_login = 'success'

        else:
            status_login = 'wrong_password'
            nama_pegawai = '-'
    else:
        status_login = 'no_user'
        nama_pegawai = '-'

    context = {
        'username' : username,
        'status_login' : status_login,
        'nama_pegawai' : nama_pegawai
    }
    return JsonResponse(context, safe=False)

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from luxand import luxand

import hashlib
import json
import requests
import base64
import os

client = luxand("0c5e5b2cd47c480fbfa6066c3aee9970")

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

@csrf_exempt
def identifikasi_wajah(request):
    imgData = request.POST['hasil']
    format, imgstr = imgData.split(";base64,")
    dataDecode = ContentFile(base64.b64decode(imgstr))
    imgRandom = get_random_string(10)
    nama_gambar = imgRandom+".png"
    with open("ladun/pic_identifikasi/" + nama_gambar, "wb+") as f:
        for chunk in dataDecode.chunks():
            f.write(chunk)
    alamat_pic = "http://127.0.0.1:7001/ladun/pic_upload/rUZ4sdKVw3.png"
    url = "https://api.luxand.cloud/photo/search"
    payload = {}
    headers = { 'token': "0c5e5b2cd47c480fbfa6066c3aee9970" }
    files = { "photo": open("ladun/pic_identifikasi/"+nama_gambar, "rb") }
    # payload["photo"] = alamat_pic
    response = requests.request("POST", url, data=payload, headers=headers, files=files)
    # result = client.recognize(photo = alamat_pic)
    hasil = response.text

    context = {
        'status' : 'sukses',
        'hasil' : hasil,
        'imgData' : imgData
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def get_data_pegawai(request):
    username = request.POST.get('username')
    data_user = Akses_Login.objects.filter(username__contains=username).first()
    kd_pegawai = data_user.kd_pegawai
    data_pegawai = Pegawai.objects.filter(kd_pegawai__contains=kd_pegawai).first()
    nama_pegawai = data_pegawai.nama_pegawai
    context = {
        'status' : 'sukses',
        'nama' : nama_pegawai
    }
    return JsonResponse(context, safe=False)


def beranda(request):
    context = {
        'status' : 'sukses'
    }
    return render(request, 'dashboard_page/dashboard.html', context)

def beranda_kita(request):
    context = {
        'status' : 'sukses'
    }
    return render(request, 'dashboard_page/beranda.html', context)

@csrf_exempt
def manajemen_pegawai(request):
    url = "https://api.luxand.cloud/subject"
    payload = {}
    headers = { 'token': "0c5e5b2cd47c480fbfa6066c3aee9970" }
    response = requests.request("GET", url, data=payload, headers=headers)
    hasil = response.json
    # print(hasil_arr)
    context = {
        'status' : 'sukses',
        'hasil' : hasil
    }
    # print(response.text)
    # return JsonResponse(context, safe=False)
    return render(request, 'dashboard_page/manajemen_pegawai.html', context)

@csrf_exempt
def proses_tambah_pegawai(request):
    url = "https://api.luxand.cloud/subject/v2"
    headers = { "token" : "0c5e5b2cd47c480fbfa6066c3aee9970" }
    
    # 'dataImg': dataImg, 'nama':nama, 'alamat':alamat, 'password':password 
    imgData = request.POST['dataImg']
    nama = request.POST['nama']
    alamat = request.POST['alamat']
    jk = request.POST['jk']
    password = request.POST['password']
    username = request.POST['username']
    pass_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
    format, imgstr = imgData.split(";base64,")
    dataDecode = ContentFile(base64.b64decode(imgstr))
    imgRandom = get_random_string(10)
    nama_gambar = imgRandom+".png"
    with open("ladun/pic_upload/" + nama_gambar, "wb+") as f:
        for chunk in dataDecode.chunks():
            f.write(chunk)
    
    # start upload to facesoft 
    name = username
    store = '1'
    alamat_pic = "http://127.0.0.1:7001/ladun/pic_upload/" + nama_gambar
    payload = {"name":name,"store":store}
    files = { "photo": open("ladun/pic_upload/" + nama_gambar, "rb") }
    payload["photo"] = alamat_pic
    response = requests.request("POST", url, data=payload, headers=headers, files=files)
    save_akses_login = Akses_Login.objects.create(kd_pegawai=imgRandom, username=username, kata_sandi=pass_hash, mac_x="-", mac_y="-", secret_key="NURUL")
    save_akses_login.save()
    save_pegawai = Pegawai.objects.create(kd_pegawai=imgRandom, nama_pegawai=nama, jenis_kelamin=jk, alamat=alamat, akses="administrator")
    save_pegawai.save()
    context = {
        'status' : 'sukses',
        'respons' : response.text,
        'lokasi' : alamat_pic,
        'nama' : nama
    }
    return JsonResponse(context, safe=False)
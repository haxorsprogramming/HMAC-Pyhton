from django.db import models

# Create your models here.
class Pegawai(models.Model):
    kd_pegawai = models.CharField(max_length=150)
    nama_pegawai = models.CharField(max_length=150)
    jenis_kelamin = models.CharField(max_length=1)
    alamat = models.CharField(max_length=200)
    akses = models.CharField(max_length=50)

class Akses_Login(models.Model):
    kd_pegawai = models.CharField(max_length=150)
    username = models.CharField(max_length=150)
    kata_sandi = models.CharField(max_length=150)
    mac_x = models.CharField(max_length=150)
    mac_y = models.CharField(max_length=150)
    secret_key = models.CharField(max_length=150)

class Data_Wajah(models.Model):
    kd_pegawai = models.CharField(max_length=150)
    kd_wajah = models.CharField(max_length=150)

class Pengujian_HMAC(models.Model):
    kd_pengujian = models.CharField(max_length=150)
    kd_pegawai = models.CharField(max_length=150)
    waktu_login = models.DateTimeField()
    kata_sandi = models.CharField(max_length=150)
    verifikasi_wajah = models.CharField(max_length=150)
    secret_key = models.CharField(max_length=150)
    status_login = models.CharField(max_length=150)



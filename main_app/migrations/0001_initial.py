# Generated by Django 3.2.5 on 2021-07-12 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Akses_Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kd_pegawai', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=150)),
                ('kata_sandi', models.CharField(max_length=150)),
                ('mac_x', models.CharField(max_length=150)),
                ('mac_y', models.CharField(max_length=150)),
                ('secret_key', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Data_Wajah',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kd_pegawai', models.CharField(max_length=150)),
                ('kd_wajah', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Pegawai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kd_pegawai', models.CharField(max_length=150)),
                ('nama_pegawai', models.CharField(max_length=150)),
                ('jenis_kelamin', models.CharField(max_length=1)),
                ('alamat', models.CharField(max_length=200)),
                ('akses', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pengujian_HMAC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kd_pengujian', models.CharField(max_length=150)),
                ('kd_pegawai', models.CharField(max_length=150)),
                ('waktu_login', models.DateTimeField()),
                ('kata_sandi', models.CharField(max_length=150)),
                ('verifikasi_wajah', models.CharField(max_length=150)),
                ('secret_key', models.CharField(max_length=150)),
                ('status_login', models.CharField(max_length=150)),
            ],
        ),
    ]

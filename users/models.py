from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User Model
class User(AbstractUser):
    """
    Model Pengguna Kustom untuk mengelola peran Mahasiswa dan Dosen.
    """
    ROLE_CHOICES = [
        ('MHS', 'Mahasiswa'),
        ('DP', 'Dosen Pembimbing'),
    ]
    
    role = models.CharField(
        max_length=3,
        choices=ROLE_CHOICES,
        default='MHS',
        verbose_name='Peran Pengguna'
    )
    
    # Menghapus field `groups` dan `user_permissions` dari AbstractUser 
    # jika tidak diperlukan, atau biarkan saja.
    # Namun, pastikan Anda telah mengatur AUTH_USER_MODEL = 'users.User' di settings.py
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"


# 2. Profil Tambahan untuk Mahasiswa (OneToOne ke User)
class MahasiswaProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mahasiswa_profile')
    nim = models.CharField(max_length=15, unique=True, verbose_name='Nomor Induk Mahasiswa')
    program_studi = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nim


# 3. Profil Tambahan untuk Dosen (OneToOne ke User)
class DosenProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dosen_profile')
    nip = models.CharField(max_length=20, unique=True, verbose_name='Nomor Induk Pegawai')
    bidang_keahlian = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nip
from django.db import models
from users.models import MahasiswaProfile, DosenProfile

class TugasAkhir(models.Model):
    STATUS_CHOICES = [
        ('PROP', 'Draft Proposal'),
        ('BIMB', 'Sedang Bimbingan'),
        ('REVI', 'Perlu Revisi'),
        ('SIDANG', 'Siap Sidang'),
        ('LULUS', 'Selesai/Lulus'),
    ]

    mahasiswa = models.OneToOneField(
        MahasiswaProfile,
        on_delete=models.CASCADE,
        related_name='proyek_ta',
        verbose_name='Mahasiswa'
    )
    dosen_pembimbing = models.ForeignKey(
        DosenProfile,
        on_delete=models.SET_NULL, # Jika dosen pindah/keluar, data TA tetap ada
        null=True,
        related_name='bimbingan_ta',
        verbose_name='Dosen Pembimbing'
    )
    judul = models.CharField(max_length=255)
    status_bimbingan = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PROP',
        verbose_name='Status Proyek'
    )
    tanggal_mulai = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tugas Akhir"
        verbose_name_plural = "Daftar Tugas Akhir"
    
    def __str__(self):
        return self.judul
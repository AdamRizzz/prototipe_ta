from django.db import models
from django.conf import settings # Menggunakan settings.AUTH_USER_MODEL
from documents.models import LaporanVersi

class Komentar(models.Model):
    laporan_versi = models.ForeignKey(
        LaporanVersi,
        on_delete=models.CASCADE,
        related_name='komentar_laporan'
    )
    oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Menunjuk ke model users.User
        on_delete=models.CASCADE
    )
    teks = models.TextField()
    # Opsional: Field untuk menandai lokasi spesifik di dokumen
    halaman = models.IntegerField(blank=True, null=True, verbose_name='Halaman')
    posisi_teks = models.CharField(max_length=100, blank=True, null=True, verbose_name='Posisi/Line')
    
    tanggal_komentar = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['tanggal_komentar']
        
    def __str__(self):
        return f"Komentar dari {self.oleh.get_full_name()} pada versi {self.laporan_versi.nomor_versi}"
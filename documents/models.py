from django.db import models
from ta_management.models import TugasAkhir

class LaporanVersi(models.Model):
    tugas_akhir = models.ForeignKey(
        TugasAkhir,
        on_delete=models.CASCADE,
        related_name='daftar_laporan',
        verbose_name='Proyek Tugas Akhir'
    )
    nomor_versi = models.IntegerField(default=1)
    file = models.FileField(
        upload_to='laporan_ta/%Y/%m/%d/', # Menyimpan file berdasarkan tahun/bulan/tanggal
        verbose_name='File Laporan'
    )
    catatan_revisi = models.TextField(blank=True, null=True, verbose_name='Catatan Mahasiswa')
    tanggal_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-tanggal_upload'] # Urutkan dari yang terbaru
        unique_together = ('tugas_akhir', 'nomor_versi') # Kombinasi ini harus unik
        
    def __str__(self):
        return f"TA: {self.tugas_akhir.judul} - Versi {self.nomor_versi}"
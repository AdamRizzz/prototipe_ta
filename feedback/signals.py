# feedback/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Komentar
from documents.models import LaporanVersi
from users.models import DosenProfile
from django.core.mail import send_mail
from django.conf import settings 

@receiver(post_save, sender=Komentar)
def notifikasi_komentar_baru(sender, instance, created, **kwargs):
    """
    Mengirim notifikasi email ketika Dosen (atau pengguna lain) membuat Komentar baru.
    """
    if created:
        komentar = instance
        laporan = komentar.laporan_versi
        ta_proyek = laporan.tugas_akhir
        
        # Tentukan penerima: Mahasiswa
        penerima_email = [ta_proyek.mahasiswa.user.email]
        
        # Tentukan pengirim: Dosen Pembimbing (atau pengguna yang membuat komentar)
        pengirim_nama = komentar.oleh.get_full_name()

        # Logika Notifikasi Email
        if settings.EMAIL_HOST_USER: # Pastikan konfigurasi email sudah ada
            subject = f"[TA Monitor] Koreksi Baru pada Laporan Versi {laporan.nomor_versi} ({ta_proyek.judul})"
            message = (
                f"Yth. {ta_proyek.mahasiswa.user.get_full_name()},\n\n"
                f"Anda menerima koreksi baru pada Tugas Akhir Anda: '{ta_proyek.judul}' "
                f"oleh {pengirim_nama}.\n\n"
                f"Silakan login ke sistem untuk melihat rincian komentar:\n"
                f"[Link menuju halaman bimbingan]\n\n"
                f"Isi Komentar: \"{komentar.teks[:100]}...\"\n"
            )
            
            # send_mail(subject, message, settings.EMAIL_HOST_USER, penerima_email)
            print(f"EMAIL SIMULASI DIKIRIM ke: {penerima_email[0]}")
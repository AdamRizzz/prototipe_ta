# documents/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LaporanVersi
from django.conf import settings 

@receiver(post_save, sender=LaporanVersi)
def notifikasi_laporan_baru(sender, instance, created, **kwargs):
    """
    Mengirim notifikasi email kepada Dosen Pembimbing ketika Mahasiswa mengunggah LaporanVersi baru.
    """
    if created:
        laporan = instance
        ta_proyek = laporan.tugas_akhir
        
        # Dosen Pembimbing adalah penerima
        penerima_email = [ta_proyek.dosen_pembimbing.user.email]
        pengirim_nama = ta_proyek.mahasiswa.user.get_full_name()

        if settings.EMAIL_HOST_USER:
            subject = f"[TA Monitor] Laporan Baru Siap Dikoreksi (Versi {laporan.nomor_versi})"
            message = (
                f"Yth. Bapak/Ibu {ta_proyek.dosen_pembimbing.user.get_full_name()},\n\n"
                f"Mahasiswa bimbingan Anda, {pengirim_nama}, telah mengunggah versi laporan baru "
                f"untuk Tugas Akhir: '{ta_proyek.judul}'.\n\n"
                f"Versi: {laporan.nomor_versi}.\n"
                f"Catatan Mahasiswa: {laporan.catatan_revisi if laporan.catatan_revisi else 'Tidak ada'}\n\n"
                f"Mohon tinjauan dan koreksinya. Terima kasih.\n"
            )
            
            # send_mail(subject, message, settings.EMAIL_HOST_USER, penerima_email)
            print(f"EMAIL SIMULASI DIKIRIM ke DP: {penerima_email[0]}")
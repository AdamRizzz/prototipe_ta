from rest_framework import permissions
from django.shortcuts import get_object_or_404
from ta_management.models import TugasAkhir

# --- 1. Izin Berbasis Peran (View-Level Permissions) ---

class IsDosenPembimbing(permissions.BasePermission):
    """
    Izinkan akses hanya jika pengguna terautentikasi dan perannya adalah Dosen Pembimbing ('DP').
    Digunakan untuk membatasi akses ke seluruh ViewSet (misalnya, membuat Komentar).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'DP'

class IsMahasiswa(permissions.BasePermission):
    """
    Izinkan akses hanya jika pengguna terautentikasi dan perannya adalah Mahasiswa ('MHS').
    Digunakan untuk membatasi akses ke seluruh ViewSet (misalnya, mengunggah LaporanVersi).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'MHS'

# --- 2. Izin Berbasis Objek (Object-Level Permissions) ---

class IsDosenPembimbingTA(permissions.BasePermission):
    """
    Izinkan akses Dosen Pembimbing untuk melihat/mengubah objek Tugas Akhir yang dibimbingnya.
    Digunakan pada update/delete objek TugasAkhir.
    """
    message = 'Anda bukan Dosen Pembimbing dari Tugas Akhir ini.'

    def has_object_permission(self, request, view, obj):
        if request.user.role != 'DP':
            return False

        # 'obj' di sini adalah instance TugasAkhir
        try:
            # Bandingkan DosenProfile dari user yang login dengan dosen_pembimbing di objek TA
            return obj.dosen_pembimbing == request.user.dosen_profile
        except AttributeError:
            # Fallback jika objek tidak memiliki atribut yang sesuai
            return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Izinkan akses Baca (GET) untuk semua.
    Izinkan akses Tulis (POST/PUT/DELETE) hanya untuk pemilik (Mahasiswa pemilik TA).
    Digunakan pada objek LaporanVersi dan Komentar.
    """

    def has_object_permission(self, request, view, obj):
        # Izin Baca (GET, HEAD, OPTIONS) diizinkan untuk semua pengguna terautentikasi.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Izin Tulis hanya diizinkan untuk pemilik objek:

        # 1. Jika objek adalah LaporanVersi: pemilik adalah Mahasiswa yang TA-nya terikat.
        if hasattr(obj, 'tugas_akhir'):
            # Mahasiswa hanya boleh memodifikasi laporan yang dia upload
            if request.user.role == 'MHS':
                return obj.tugas_akhir.mahasiswa.user == request.user
            
        # 2. Jika objek adalah Komentar: pemilik adalah pembuat komentar.
        if hasattr(obj, 'oleh'):
            # Dosen/Mahasiswa hanya boleh memodifikasi/menghapus komentar yang dibuatnya sendiri.
            return obj.oleh == request.user
            
        return False
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied, NotFound
from django.db.models import Q
from .models import TugasAkhir
from .serializers import TugasAkhirSerializer
from users.permissions import IsDosenPembimbing, IsMahasiswa, IsDosenPembimbingTA

class TugasAkhirViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk mengelola data Tugas Akhir (TA).
    Implementasi Queryset disesuaikan berdasarkan peran pengguna (Mahasiswa/Dosen).
    """
    serializer_class = TugasAkhirSerializer
    permission_classes = [permissions.IsAuthenticated] # Semua yang login bisa akses, namun dibatasi oleh get_queryset dan get_permissions

    def get_queryset(self):
        """
        Memastikan pengguna hanya melihat TA yang relevan bagi mereka:
        - Mahasiswa: Hanya melihat TA miliknya.
        - Dosen Pembimbing: Hanya melihat daftar TA yang dia bimbing.
        """
        user = self.request.user

        if user.role == 'MHS':
            # Jika user adalah Mahasiswa, filter TA berdasarkan MahasiswaProfile yang terkait dengan user.
            try:
                return TugasAkhir.objects.filter(mahasiswa__user=user)
            except:
                # Jika user MHS belum memiliki MahasiswaProfile, kembalikan queryset kosong.
                return TugasAkhir.objects.none()

        elif user.role == 'DP':
            # Jika user adalah Dosen, filter TA berdasarkan DosenProfile yang terkait.
            try:
                return TugasAkhir.objects.filter(dosen_pembimbing__user=user)
            except:
                # Jika user DP belum memiliki DosenProfile, kembalikan queryset kosong.
                return TugasAkhir.objects.none()
        
        # Admin atau peran lain (jika ada) dapat melihat semua, atau kembalikan kosong jika tidak ada peran spesifik
        return TugasAkhir.objects.all()

    def get_permissions(self):
        """
        Menentukan izin yang berlaku untuk setiap aksi (create, retrieve, update, dll.).
        """
        # 1. CREATE: Hanya Dosen yang dapat membuat TA baru (misalnya, mendaftarkan relasi bimbingan).
        if self.action == 'create':
            # Catatan: Dalam banyak kasus, relasi TA dibuat via admin atau proses backend, bukan via API.
            # Kita asumsikan hanya DP atau Admin yang boleh mendaftarkan TA baru.
            return [IsDosenPembimbing()]
        
        # 2. UPDATE/PARTIAL_UPDATE: Hanya Dosen Pembimbing TA terkait yang boleh mengubah status/judul.
        elif self.action in ['update', 'partial_update']:
            # Gunakan object-level permission untuk memastikan Dosen hanya memodifikasi TA yang dia bimbing
            return [IsDosenPembimbing(), IsDosenPembimbingTA()]

        # 3. DELETE: Batasi penghapusan. Hanya admin atau Dosen Pembimbing yang diizinkan, dan itu pun jarang dilakukan.
        elif self.action == 'destroy':
            return [IsDosenPembimbing(), IsDosenPembimbingTA()]

        # 4. RETRIEVE/LIST: Diizinkan untuk semua yang terautentikasi (sudah difilter di get_queryset).
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Menambahkan logika sebelum TA disimpan (biasanya tidak diperlukan untuk TA,
        karena Mahasiswa dan DP harus diisi secara eksplisit).
        """
        serializer.save()
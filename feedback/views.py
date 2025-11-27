# feedback/views.py

from rest_framework import viewsets, permissions
from .models import Komentar
from .serializers import KomentarSerializer
from users.permissions import IsDosenPembimbing

class KomentarViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk mengelola Komentar/Koreksi pada Laporan.
    """
    serializer_class = KomentarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Memfilter komentar berdasarkan peran dan kepemilikan.
        """
        user = self.request.user
        
        # Mengambil ID Laporan dari parameter URL jika ada
        laporan_id = self.request.query_params.get('laporan_id')
        
        # 1. Jika Mahasiswa: hanya boleh melihat komentar pada TA miliknya
        if user.role == 'MHS':
            queryset = Komentar.objects.filter(
                laporan_versi__tugas_akhir__mahasiswa__user=user
            )
        
        # 2. Jika Dosen Pembimbing: hanya boleh melihat komentar pada TA yang dia bimbing
        elif user.role == 'DP':
            queryset = Komentar.objects.filter(
                laporan_versi__tugas_akhir__dosen_pembimbing__user=user
            )
        else:
            # Peran lain (Admin, dll)
            queryset = Komentar.objects.all()

        # Filtering opsional berdasarkan parameter URL (laporan_id)
        if laporan_id:
            queryset = queryset.filter(laporan_versi__id=laporan_id)
        
        return queryset.select_related('laporan_versi', 'oleh') # Optimasi Query

    def get_permissions(self):
        """
        Menentukan izin untuk aksi CREATE.
        """
        # Hanya Dosen yang boleh membuat (POST) Komentar baru (koreksi)
        if self.action == 'create':
            return [IsDosenPembimbing()]
        
        # UPDATE/DELETE harus dikontrol oleh IsOwnerOrReadOnly jika diperlukan
        # Untuk kasus koreksi, seringkali edit/delete komentar dibatasi
        if self.action in ['update', 'partial_update', 'destroy']:
            # Asumsi: Hanya pengirim (Dosen) yang boleh mengedit/menghapus komentarnya sendiri
            # Anda perlu mengimpor IsOwnerOrReadOnly dan menambahkannya di sini jika diizinkan
            # return [IsDosenPembimbing(), IsOwnerOrReadOnly()] 
            # Untuk keamanan, kita batasi edit/hapus
            raise permissions.IsAdminUser() # Hanya Admin yang boleh edit/hapus

        return [permissions.IsAuthenticated()]
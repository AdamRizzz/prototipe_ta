from rest_framework import viewsets
from .models import LaporanVersi
from .serializers import LaporanVersiSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsMahasiswa

class LaporanVersiViewSet(viewsets.ModelViewSet):
    # Mahasiswa hanya bisa melihat laporannya sendiri
    def get_queryset(self):
        if self.request.user.role == 'MHS':
            return LaporanVersi.objects.filter(tugas_akhir__mahasiswa__user=self.request.user)
        return LaporanVersi.objects.all()
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsMahasiswa()]
        # Untuk GET (List/Retrieve), semua yang login bisa
        return [IsAuthenticated()]
    
    serializer_class = LaporanVersiSerializer
    permission_classes = [IsAuthenticated]
# feedback/serializers.py

from rest_framework import serializers
from .models import Komentar
from documents.models import LaporanVersi

class KomentarSerializer(serializers.ModelSerializer):
    # Field read-only untuk menampilkan nama pengirim (Dosen/Mahasiswa)
    oleh_nama = serializers.CharField(source='oleh.get_full_name', read_only=True)
    
    # Field read-only untuk menampilkan peran pengirim
    oleh_role = serializers.CharField(source='oleh.role', read_only=True)
    
    class Meta:
        model = Komentar
        fields = [
            'id', 
            'laporan_versi', 
            'oleh', 
            'oleh_nama', 
            'oleh_role', 
            'teks', 
            'halaman', 
            'posisi_teks', 
            'tanggal_komentar'
        ]
        read_only_fields = ['oleh', 'tanggal_komentar']
        
    def create(self, validated_data):
        """
        Mengisi field 'oleh' (pengirim) secara otomatis dengan user yang sedang login.
        """
        # User yang sedang request (yang login)
        user = self.context['request'].user
        validated_data['oleh'] = user
        
        return Komentar.objects.create(**validated_data)
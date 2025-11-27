# ta_management/serializers.py

from rest_framework import serializers
from .models import TugasAkhir
from users.models import MahasiswaProfile, DosenProfile

class TugasAkhirSerializer(serializers.ModelSerializer):
    # Field read-only tambahan untuk menampilkan nama, bukan hanya ID
    mahasiswa_nama = serializers.CharField(
        source='mahasiswa.user.get_full_name', 
        read_only=True
    )
    dosen_pembimbing_nama = serializers.CharField(
        source='dosen_pembimbing.user.get_full_name', 
        read_only=True
    )
    
    class Meta:
        model = TugasAkhir
        fields = [
            'id', 
            'mahasiswa', 
            'mahasiswa_nama', 
            'dosen_pembimbing', 
            'dosen_pembimbing_nama', 
            'judul', 
            'status_bimbingan', 
            'tanggal_mulai'
        ]
        # Field yang hanya bisa dilihat, tidak bisa dikirim saat POST/PUT
        read_only_fields = ['tanggal_mulai', 'mahasiswa_nama', 'dosen_pembimbing_nama'] 

    def update(self, instance, validated_data):
        """
        Mengimplementasikan logika bisnis untuk UPDATE TugasAkhir.
        Hanya Dosen Pembimbing (yang sudah divalidasi di views.py) yang bisa mengubah STATUS TA.
        """
        user = self.context['request'].user
        
        # 1. Logika untuk Dosen Pembimbing (Mengubah Status)
        if user.role == 'DP':
            # Dosen hanya diizinkan mengubah status_bimbingan dan judul (jika perlu)
            instance.status_bimbingan = validated_data.get('status_bimbingan', instance.status_bimbingan)
            instance.judul = validated_data.get('judul', instance.judul)
            
            # Jika dosen ingin mengganti dosen pembimbing (hanya jika ada izin khusus)
            # Anda bisa tambahkan validasi di sini
            
            instance.save()
            return instance

        # 2. Logika untuk Mahasiswa (Mungkin hanya boleh mengubah Judul awal sebelum disetujui)
        elif user.role == 'MHS':
            # Mahasiswa hanya diizinkan mengubah judul jika statusnya masih 'Draft Proposal'
            if instance.status_bimbingan == 'PROP':
                 instance.judul = validated_data.get('judul', instance.judul)
                 instance.save()
                 return instance
            else:
                # Jika status sudah berjalan, Mahasiswa tidak boleh mengubah data ini.
                raise serializers.ValidationError({"detail": "Mahasiswa hanya dapat mengubah data Tugas Akhir saat status masih Draft Proposal."})

        # Logika fallback jika ada update dari user lain (seharusnya sudah dicegah oleh permissions di views.py)
        raise serializers.ValidationError({"detail": "Anda tidak memiliki izin untuk mengubah data ini."})
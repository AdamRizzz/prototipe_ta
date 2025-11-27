from rest_framework import serializers
from django.db import models
from .models import LaporanVersi
from ta_management.models import TugasAkhir

class LaporanVersiSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaporanVersi
        fields = '__all__'
def validate(self, data):
        # 1. Pastikan Mahasiswa memiliki TA yang aktif
        user = self.context['request'].user
        
        try:
            ta_proyek = TugasAkhir.objects.get(mahasiswa__user=user)
        except TugasAkhir.DoesNotExist:
            raise serializers.ValidationError("Anda belum terdaftar memiliki proyek Tugas Akhir.")

        # 2. Pastikan proyek TA belum berstatus 'LULUS'
        if ta_proyek.status_bimbingan == 'LULUS':
            raise serializers.ValidationError("Proyek Tugas Akhir Anda sudah selesai dan tidak bisa diubah.")
            
        data['tugas_akhir'] = ta_proyek # Tambahkan objek TA ke data yang divalidasi
        return data
        
def create(self, validated_data):
        # Atur nomor versi otomatis saat membuat laporan baru
        ta_proyek = validated_data['tugas_akhir']
        last_version = ta_proyek.daftar_laporan.aggregate(models.Max('nomor_versi'))['nomor_versi__max']
        validated_data['nomor_versi'] = (last_version or 0) + 1
        
        return LaporanVersi.objects.create(**validated_data)
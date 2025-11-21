import math

jumlah_hari = 360
sisa_hari = jumlah_hari

tahun = math.floor(sisa_hari/360)
sisa_hari %= 360 # sisa_hari = sisa_hari % 360

bulan = math.floor(sisa_hari/30)
sisa_hari %= 30 # sisa_hari = sisa_hari % 30

minggu = math.floor(sisa_hari/7)
sisa_hari %= 7 # sisa_hari = sisa_hari % 7

print("Total hari:", jumlah_hari)
print("Tahun:", tahun)
print("Bulan:", bulan)
print("Minggu:", minggu)
print("Hari:", sisa_hari)
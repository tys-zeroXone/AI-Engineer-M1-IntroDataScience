import math


# kecepatan
# 60 km/h + 40 km/h = 100km/h
# jarak 120 km
# 120/100 = 1.2 jam - 60 menit + 12 menit
# 9.00 -> jam 10 menit ke 12

jam_awal = 9
jarak_km = 120
kecepatan_km_per_jam = 100
kedcepatan_km_per_detik = kecepatan_km_per_jam / 3600

total_detik = jarak_km / kedcepatan_km_per_detik
jam = math.floor(total_detik/3600)
menit = math.floor((total_detik%3600)/60)
detik = math.floor((total_detik%3600)%60)

if detik < 10:
    detik = "0" + str(detik)
print("Tabrakan terjadi di jam {}:{}:{}".format(jam_awal + jam, menit, detik))
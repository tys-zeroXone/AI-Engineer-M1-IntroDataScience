# LAMBDA BASICS
# lambda = fungsi anonim, singkat untuk operasi sederhana
# <variable_lambda> = lambda <parameter>: <return_value>
print("lambda basics")
hasil = lambda angka: angka * 2
lambda_plus = lambda num1, num2: num1 + num2
print("hasil(10) =", hasil(10))              # 20
print("lambda_plus(10, 5) =", lambda_plus(10, 5))  # 15
print("-----------")

# MANUAL LOOP vs MAP
print("manual loop vs map")
list_angka = [1, 2, 3, 4, 5]
print("list_angka =", list_angka)

# Manual loop (tanpa map)
print("manual: kalikan tiap elemen dengan 2 pakai for loop")
list_angka_hasil = []
for x in list_angka:
    y = x * 2
    list_angka_hasil.append(y)
print("hasil manual =", list_angka_hasil)

print("-----------")

# MAP DENGAN FUNGSI BIASA
print("map() dengan fungsi biasa")
def kali2(angka):
    return angka * 2

list_angka_dengan_map = map(kali2, list_angka)  # callback function
print("hasil map + fungsi =", list(list_angka_dengan_map))

# MAP DENGAN LAMBDA
print("map() dengan lambda")
list_angka_dengan_map = map(lambda angka: angka * 2, list_angka)
print("hasil map + lambda =", list(list_angka_dengan_map))
print("-----------")

# FILTER (MENYARING DATA)
print("filter() — menyaring elemen dengan kondisi True/False")
list_angka = [1, 2, 3, 4, 5]
print("list_angka =", list_angka)

def cek_bilangan_ganjil(angka):
    # mengembalikan sisa bagi 2; non-nol dianggap True (ganjil → True)
    return angka % 2

def cek_bilangan_genap(angka):
    # True jika angka genap
    return angka % 2 == 0

print("filter: ganjil (pakai fungsi)")
list_angka_hasil = filter(cek_bilangan_ganjil, list_angka)
print("ganjil =", list(list_angka_hasil))

print("filter: genap (pakai fungsi)")
list_angka_hasil = filter(cek_bilangan_genap, list_angka)
print("genap =", list(list_angka_hasil))

print("filter: genap (pakai lambda)")
list_angka_hasil = filter(lambda angka: angka % 2 == 0, list_angka)
print("genap =", list(list_angka_hasil))
print("-----------")

print("Selesai 🎉")
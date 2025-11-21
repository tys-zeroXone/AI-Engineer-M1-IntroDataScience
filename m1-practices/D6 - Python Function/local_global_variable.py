# LOCAL SCOPE
print("local scope: variabel hanya hidup di dalam fungsi")
def total(x, y):
    z = x + y  # z adalah variabel lokal (hanya ada di dalam fungsi total)
    return z

hasil = total(1, 2)
print("hasil total(1, 2) =", hasil)  # 3
# print(z)  # akan error: NameError, karena z tidak dikenal di luar fungsi
print("-----------")

# SHADOWING (nama variabel sama, tapi beda scope)
print("shadowing: nama variabel 'x' lokal vs 'x' global")
def coba():
    x = 8                    # x lokal → 'menutupi' (shadow) x global
    print("di dalam coba(), x + 2 =", x + 2)  # 10
    return x + 3             # 11

x = 5                         # x global
print("panggil coba() →", coba())      # 11
print("x global setelah coba() pertama =", x)  # tetap 5 (tidak berubah)
print("-----------")

# REDEFINISI FUNGSI (coba didefinisikan ulang)
print("redefinisi fungsi: 'coba' versi baru (masih tanpa global)")
def coba():
    x = 2          # masih x lokal, beda dengan x global
    x += 8         # x lokal jadi 10
    print("di dalam coba() v2, x + 2 =", x + 2)  # 12
    return x + 3   # 13

x = 5
print("panggil coba() v2 →", coba())  # 13
print("x global setelah coba() v2 =", x)  # tetap 5
print("-----------")

# KEYWORD GLOBAL (mengubah variabel global dari dalam fungsi)
print("keyword 'global': memodifikasi x global dari dalam fungsi")
def coba():
    global x       # menyatakan bahwa kita akan memakai/mengubah x global
    x += 8         # x global: 5 → 13
    print("di dalam coba() v3, x + 2 =", x + 2)  # 15 (jika awal x=5)
    return x + 3   # 16

x = 5
print("panggil coba() v3 →", coba())  # 16
print("x global setelah coba() v3 =", x)  # 13 (berubah!)
print("-----------")

print("Selesai 🎉")
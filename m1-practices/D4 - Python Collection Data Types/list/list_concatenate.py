list_contoh = ["hello", 1, 1, 3, True]
list_baru = ["world", 2, 2, 4, False]

list_gabungan = list_contoh + list_baru
print(list_gabungan)

list_gabungan.extend(list_baru)
print(list_gabungan)
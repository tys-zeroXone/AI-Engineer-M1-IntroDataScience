# create list
# index/urutan mulai dari 0 (dihitung dari kiri ke kanan)
# index negatif dihitung dari kanan ke kiri (dimulai dari -1, -2, dst)
list_contoh = ["hello", 1, 1, 3, True]
print(list_contoh)

# access data
print("positif indexing")
print(list_contoh[2]) # positif indexing

print("negatif indexing")
print(list_contoh[-5]) # negatif indexing

print("slicing, start itu termasuk, end itu tidak termasuk")
print(list_contoh[0:3]) # slicing, start itu termasuk, end itu tidak termasuk
print(list_contoh[2:3])

print("slicing")
print(list_contoh[-3:]) # sama dengan sampai akhir
print(list_contoh[:3]) # sama dengan start =0/dari awal
print("-----------")

print("change data")
print(list_contoh)
print("ubah data list_contoh index ke-1 menjadi world")
list_contoh[1] = "world"
print(list_contoh)
print("ubah data list_contoh index ke-(-2) menjadi 3.0")
list_contoh[-2] = 3.0
print(list_contoh)

print("-----------")
print("add data")
print(list_contoh)
print("tambah metode append, menambahkan data di akhir list")
list_contoh.append(False)
print(list_contoh)
print("tambah dengan metode insert")
list_contoh.insert(2, "!")
print(list_contoh)

print("-----------")
print("remove data")
print(list_contoh)
print("delete data metode remove")
list_contoh.remove("hello")
print(list_contoh)
print("delete data metode pop, menghapus element terakhir dari list")
list_contoh.pop()
print(list_contoh)
print("delete data metode del, menghapus element by index value di dalam list")
del list_contoh[2]
print(list_contoh)
print("menghapus semua data di dalam list")
list_contoh.clear()
print(list_contoh)
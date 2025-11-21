print("membuat dictionary secara manual")
dictionary_contoh = {
    "nama": "Arif Agustyawan",
    "usia": 17,
    "pekerjaan": "Programmer",
    "status_menikah": False
}

print(dictionary_contoh)

print("\n\nmembuat dictionary menggunakan function dict()")

dictionary_contoh2 = dict(name="Arif Agustyawan", usia=17, pekerjaan="Programmer", status_menikah=False)
print(dictionary_contoh2)

# dictionary di dalam dictionary
dictionary_contoh3 = dict(name="Arif Agustyawan", usia=17, pekerjaan="Programmer", status_menikah=False, alamat= {"usaha_1": "Jl. A", "usaha_2": "Jl. B"})
print(dictionary_contoh3)

print("\n\nmengakses data di dalam dictionary")
print("ini nama", dictionary_contoh3["name"])
print("\n\nmengambil data dalam dictionary menggunakan .get()")
print(dictionary_contoh3.get("name"))

print("\n\nmenampilkan alamat usaha 1")
print("Alamat usaha 1 ada di", dictionary_contoh3["alamat"]["usaha_1"])

print("\n\nmenampilkan usaha 1 dengan menggunakan methode .get()")
print("Alamat usaha 1 ada di", dictionary_contoh3.get("alamat").get("usaha_1"))

# print(dictionary_contoh3["umur"]) # akan error karena ngga ada key umur di dalam dictionary
# print(dictionary_contoh3.get("umur")) #akan mengembalikan None value

print("\n\nmengubah data di dalam dictionary")
dictionary_contoh3["alamat"]["usaha_2"] = "Jl. C"
dictionary_contoh3["name"] = ""
print(dictionary_contoh3)

print("\n\nmenmabahkan data ke dalam dictionary")
dictionary_contoh3["hobi"] = ["membaca", "jalan-jalan"]
print(dictionary_contoh3)


print("\n\nmenghapus data di dalam dictionary")
print("1. perintah del")
del dictionary_contoh3["alamat"]["usaha_1"]
print(dictionary_contoh3)

print("\n2. perintah pop")
dictionary_contoh3.pop("status_menikah")
print(dictionary_contoh3)

print("\n3. perintah popitem")
dictionary_contoh3.popitem()
print(dictionary_contoh3)

print("\n4. perintah clear")
dictionary_contoh3.clear()
print(dictionary_contoh3)

print("\n\nakses dictionary menggunakan loop")
dictionary_contoh = dict(name="Arif Agustyawan", usia=17, pekerjaan="Programmer", status_menikah=False)
print(dictionary_contoh)
print("1. loop through the dictionary")
for x in dictionary_contoh:
    print(x)

print("2. loop through the keys")
for key in dictionary_contoh.keys():
    print(key)

print("3. loop through the values")
for val in dictionary_contoh.values():
    print(val)

print("4. loop through both keys and values")
for x in dictionary_contoh.items():
    print(x)
    
for key, value in dictionary_contoh.items():
    print(key, value)

print("\n\nmengecek apakah key ada dalam dictionary")
if "umur" in dictionary_contoh:
    print("umur ada di dictionary")
else:
    print("umur ga ada di dictionary")

print("\n\nmengecek panjang dari suatu dictionary")
print("panjang dictionary", len(dictionary_contoh))

print("\n\ncopy dictionary")
print("dict contoh", dictionary_contoh)
dictionary_contoh_x = dictionary_contoh.copy()
print("dict contoh x", dictionary_contoh_x)

print("\n\nnested dictionary")
data_karyawan = {
    "1991": {
        "nama": "Arif Agustyawan",
        "usia": 17,
        "pekerjaan": "Programmer",
        "status_menikah": False
    },
    "1992": {
        "nama": "Budi",
        "usia": 17,
        "pekerjaan": "Programmer",
        "status_menikah": False
    }
}

print(data_karyawan)

print(data_karyawan["1991"])
print(len(data_karyawan))
print(len(data_karyawan["1991"]))

# dictionary di dalam dictionary
# data_karyawan = [
#     {
#         "nama": "Arif Agustyawan",
#         "usia": 17,
#         "pekerjaan": "Programmer",
#         "status_menikah": False
#     },
#     {
#         "nama": "Budi",
#         "usia": 17,
#         "pekerjaan": "Programmer",
#         "status_menikah": False
#     }
# ]

# print(data_karyawan[0])

# data_karyawan = [
#     ["Arif Agustyawan", 17, "Programmer", False],
#     ["Budi", 17, "Programmer", False]
# ]

a, x = 10, 20
print(a, x)
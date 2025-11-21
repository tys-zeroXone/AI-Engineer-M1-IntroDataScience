print("membuat set")
set_contoh = {"The Avengers", "Iron Man 3", "Avengers: Age of Ultron", "Iron Man 3"}
print(set_contoh)

print("\n\ncasting list ke set")
list_contoh = ["The Avengers", "Iron Man 3", "Avengers: Age of Ultron", "Iron Man 3"]
set_list_contoh = set(list_contoh)
print(set_list_contoh)

print("\n\ncasting tuple ke set")
tuple_contoh = ("The Avengers", "Iron Man 3", "Avengers: Age of Ultron", "Iron Man 3")
set_tuple_contoh = set(tuple_contoh)
print(set_tuple_contoh)

print("\n\ncasting dictionary ke set")
dictionary_contoh = {
    "name": "Arif Agustyawan",
    "usia": 17,
    "pekerjaan": "Programmer",
    "status_menikah": False
}

set_dictionary_contoh = set(dictionary_contoh)
print(set_dictionary_contoh)

print("\n\nakses set menggunakan loop")
for x in set_contoh:
    print(x)

print("\n\nmengecek data di set menggunakan in")
search = "Iron Man 4"    
if search in set_contoh:
    print(f"{search} ada di set")
else:
    print(f"{search} tidak ada di set")
    
print("\n\nmenambah data di set")
set_contoh.add("Hulk")
print(set_contoh)

print("\n\nmengupdate data di set")
set_contoh.update(["Spiderman 1", "Hulk"])
print(set_contoh)

print("\n\nmenghapus data di set, jika data tidak ada maka akan error")
set_contoh.remove("Iron Man 3")
print(set_contoh)

print("\n\nmenghapus data di set, jika data tidak ada maka tidak akan error")
set_contoh.discard("Hulk")
print(set_contoh)

print("\n\nmenghapus data di set secara acak")
set_contoh.pop()
print(set_contoh)

print("\n\nmenghapus semua data di set")
set_contoh.clear()
print(set_contoh)

set_1 = {"The Avengers", "Iron Man 3", "Avengers: Age of Ultron"}
set_2 = {"Titanic", "The Avengers", "Hulk"}

print("\n\nmenggabungkan set, dengan menggunakan union() menggabungkan data dari set satu dan set lainnya")
set_3 = set_1.union(set_2)
print(set_3)

print("\n\nmenampilkan data yang ada di set satu namun tidak ada di set lainnya, dengan menggunakan difference()")
set_3 = set_1.difference(set_2)
print(set_3)

print("\n\nmenampilkan data yang ada di set satu namun tidak ada di set lainnya, dengan menggunakan difference_update() / langsung update set asal")
set_1.difference_update(set_2)
print(set_1)
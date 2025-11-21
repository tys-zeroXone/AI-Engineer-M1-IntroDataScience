judul = "Belajar Python dasar"
judul = 'Belajar Python dasar'
judul = '''Belajar Python dasar'''
judul = """Belajar Python dasar
Tanggal 20 Agustus 2024""" # single quote tidak bisa mengandung enter
print(judul)


judul = "Belajar \"Python\" dasar"
print(judul)

judul = 'Belajar "Python" dasar'
print(judul)

judul = "Belajar \\Python dasar"
print(judul)

judul = "Belajar \nPython dasar" # \n adalah new line (enter)
print(judul)

judul = "Belajar \tPython dasar" # \t adalah tab
print(judul)

judul = "Belajar \bPython dasar" # \b adalah backspace
print(judul)

judul = "Belajar Python dasar"
print(len(judul)) # len adalah length (panjang string)
print(judul.index("a")) # index adalah posisi karakter dalam string
print(judul.split(" ")) # split adalah memecah string menjadi list
print(judul.lower())
print(judul.upper())

print(judul[0:7])
print(judul[:7])
print(judul[8:])

judul_1 = "Bersama Purwadhika"
print(judul + " " + judul_1)

nama = "Budi Yanto"
umur = 30

print("Halo, nama saya {}, umur saya {}".format(nama, umur))
print("Halo, nama saya {umurx}, umur saya {namax}".format(umurx=nama, namax=umur))
print(f"Halo, nama saya {nama}, umur saya {umur}")

judul = "   Belajar Python dasar   "
print("python" in judul)

nama = input("Masukkan nama: ")
print(f"Halo, {nama}")

z = range(0, 5, 1) # range(start=0, stop=5, step=1)
z = range(5) # sama dengan range(0, 5, 1)

for x in z: # -> "FOR" -> "VARIABLE" -> "IN" -> "DATA"
    print(x, end=" ") # end=" " -> agar tidak ada enter atau ganti dengan space

print("\n")    
z = range(1, 5, 1) # range(start=1, stop=5, step=1), akan mencetak 1, 2, 3, 4
for x in z:
    print(x, end=" ")

print("\n")

z = range(0, 5, 2) # range(start=0, stop=5, step=2), akan mencetak 0, 2, 4
for x in z:
    print(x, end=" ")

print("\n")   
    
z = range(5)
for x in z:
    print("Halo selamat datang!!!")
    
print("\n")

judul = "Belajar Python dasar"
for x in judul:
    print(x)
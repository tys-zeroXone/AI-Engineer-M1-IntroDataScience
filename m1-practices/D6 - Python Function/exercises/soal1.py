def ganjil_genap(angka) :
    if(angka % 2 == 0):
        return 'Genap'
    return 'Ganjil'

def ubah_jadi_ganjil_genap(list_angka):
    return list(map(ganjil_genap, list_angka))

list_1 = [1,3,4,5]
list_2 = [22,17,19,20,14]
list_3 = [1,3,5]
list_4 = [2,4,6]

list_1 = ubah_jadi_ganjil_genap(list_1)
list_2 = ubah_jadi_ganjil_genap(list_2)
list_3 = ubah_jadi_ganjil_genap(list_3)
list_4 = ubah_jadi_ganjil_genap(list_4)

print(list_1)
print(list_2)
print(list_3)
print(list_4)
def tambah(num1, num2):
    hasil = num1+num2
    tampilkan_hasil(hasil)

def kurang(num1, num2):
    hasil = num1-num2
    tampilkan_hasil(hasil)

def kali():
    pass

def bagi():
    pass

def tampilkan_hasil(num):
    print("hasilnya adalah", num)

def hitung(fn_operation, num1, num2):
    fn_operation(num1, num2)     


kurang(5,1)
hitung(kurang, 5, 1)

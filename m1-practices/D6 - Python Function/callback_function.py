def tambah(num1, num2):
    return num1 + num2

def kurang(num1, num2):
    return num1 - num2

def hitung(fn_operation, num1, num2):
    hasil = fn_operation(num1, num2)
    return hasil



x = hitung(tambah, 1, 2)
print(x)

y = hitung(kurang, 1, 2)
print(y)
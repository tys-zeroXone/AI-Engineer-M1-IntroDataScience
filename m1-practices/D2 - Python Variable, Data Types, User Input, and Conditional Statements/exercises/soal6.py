hargaApel = 10000
hargaJeruk = 15000
hargaAnggur = 20000

jumlahApel = int(input('Masukkan Jumlah Apel : '))
jumlahJeruk = int(input('Masukkan Jumlah Jeruk : '))
jumlahAnggur = int(input('Masukkan Jumlah Anggur : '))

totalHargaApel = jumlahApel * hargaApel
totalHargaJeruk = jumlahJeruk * hargaJeruk
totalHargaAnggur = jumlahAnggur * hargaAnggur

print('''
Detail Belanja

Apel : {jmlApel} x {hrgApel} = {totalHrgApel}
Jeruk : {jmlJeruk} x {hrgJeruk} = {totalHrgJeruk}
Anggur : {jmlAnggur} x {hrgAnggur} = {totalHrgAnggur}

Total : {totalHarga}
'''.format(jmlApel=jumlahApel, hrgApel=hargaApel, totalHrgApel=totalHargaApel, 
    jmlJeruk=jumlahJeruk, hrgJeruk=hargaJeruk, totalHrgJeruk=totalHargaJeruk,
    jmlAnggur=jumlahAnggur, hrgAnggur=hargaAnggur, totalHrgAnggur=totalHargaAnggur,
    totalHarga=(totalHargaAnggur+totalHargaApel+totalHargaJeruk)))




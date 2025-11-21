'''
PENJELASAN SOAL NO 2
Lalu untuk soal berikutnya, dari app market yang sudah kita kerjakan di session sebelumnya, pada kali ini teman - teman perlu menambahkan fitur sebagai berikut :

Yang pertama, tambahkanlah fitur stock. Sekarang, setiap buah memiliki jumlah stock masing2, dimana teman-teman diberi kebebasan untuk menentukan jumlah stock dari setiap buahnya. 
Kemudian saat user menginput jumlah buah yang ingin dibeli melebihi jumlah stocknya , akan dimunculkan text di terminal berupa informasi bahwa stock kurang dari permintaan dan meminta user untuk menginput jumlahnya kembali, dan fitur ini berlaku untuk setiap buahnya. Lalu programnya juga tidak akan berpindah ke proses selanjutnya jika user tidak menginput jumlahnya dengan tepat, yaitu kurang dari atau sama dengan jumlah stocknya. 

Untuk fitur yang kedua, pada penginputan uang pembayaran, akan diterapkan hal yang mirip, yaitu jika user menginput jumlah uang kurang dari yang seharusnya, akan memunculkan text di terminal berupa informasi bahwa uang yang dimasukkan masih kurang dan meminta user untuk menginput ulang jumlah uangnya. Kemudian untuk informasi textnya, tolong munculkan jumlah kekurangan yang harus dibayar. Misalnya total harga adalah 275.000 namun user hanya menginput 240.000, maka pada text di terminal akan muncul informasi bahwa user kurang uangnya sebesar 35.000. Jika nilai input yang dimasukkan lebih dari seharusnya maka akan menampilkan terima kasih dan jumlah  kembaliannya, namun jika uangnya pas, maka text yang akan tampil hanya terima kasih saja, dan aplikasi akan selesai atau berhenti bila user sudah memasukkan jumlah uang sama atau lebih dari total harganya.

'''
harga_apel = 10000
harga_jeruk = 15000
harga_anggur = 20000

stock_apel = 5
stock_jeruk = 7
stock_anggur = 6

while True:
    jumlah_apel = int(input('Masukkan Jumlah Apel : '))
    if jumlah_apel > stock_apel:
        print('Jumlah yang dimasukkan terlalu banyak \nStock Apel tinggal : ' + str(stock_apel))
    else:
        break

while True:
    jumlah_jeruk = int(input('Masukkan Jumlah Jeruk : '))
    if jumlah_jeruk > stock_jeruk:
        print('Jumlah yang dimasukkan terlalu banyak \nStock Jeruk tinggal : ' + str(stock_jeruk))
    else:
        break

while True:
    jumlah_anggur = int(input('Masukkan Jumlah Anggur : '))
    if jumlah_anggur > stock_anggur:
        print('Jumlah yang dimasukkan terlalu banyak \nStock Anggur tinggal : ' + str(stock_anggur))
    else:
        break

total_harga_apel = jumlah_apel * harga_apel
total_harga_jeruk = jumlah_jeruk * harga_jeruk
total_harga_anggur = jumlah_anggur * harga_anggur
total_harga = total_harga_anggur + total_harga_apel + total_harga_jeruk

print('''
    Detail Belanja

    Apel : {jml_apel} x {hrg_apel} = {total_hrg_apel}
    Jeruk : {jml_jeruk} x {hrg_jeruk} = {total_hrg_jeruk}
    Anggur : {jml_anggur} x {hrg_anggur} = {total_hrg_anggur}

    Total : {total_harga}
    '''.format(
        jml_apel=jumlah_apel, hrg_apel=harga_apel, total_hrg_apel=total_harga_apel,
        jml_jeruk=jumlah_jeruk, hrg_jeruk=harga_jeruk, total_hrg_jeruk=total_harga_jeruk,
        jml_anggur=jumlah_anggur, hrg_anggur=harga_anggur, total_hrg_anggur=total_harga_anggur,
        total_harga=total_harga
    ))

while True:
    jml_uang = int(input('Masukkan jumlah uang : '))

    if jml_uang > total_harga:
        kembali = jml_uang - total_harga
        print('Terima kasih \n\nUang kembali anda : {}'.format(kembali))
        break
    elif jml_uang == total_harga:
        print('Terima kasih')
        break
    else:
        kekurangan = total_harga - jml_uang
        print('Uang anda kurang sebesar {}'.format(kekurangan))

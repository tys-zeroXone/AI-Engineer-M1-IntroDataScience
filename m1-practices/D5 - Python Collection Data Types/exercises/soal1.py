list_buah = [
    {
        'nama': 'Apel',
        'stock': 20,
        'harga': 10000
    },
    {
        'nama': 'Jeruk',
        'stock': 15,
        'harga': 15000
    },
    {
        'nama': 'Anggur',
        'stock': 25,
        'harga': 20000
    }
]

cart = []

while True :
    pilihan_menu = input('''
        Selamat Datang di Pasar Buah

        List Menu :
        1. Menampilkan Daftar Buah
        2. Menambah Buah
        3. Menghapus Buah
        4. Membeli Buah
        5. Exit Program

        Masukkan angka Menu yang ingin dijalankan : ''')

    if(pilihan_menu == '1') :

        print('Daftar Buah\n')
        print('Index\t| Nama  \t| Stock\t| Harga')
        for i in range(len(list_buah)) :
            print('{}\t| {}  \t| {}\t| {}'.format(i,list_buah[i]['nama'],list_buah[i]['stock'],list_buah[i]['harga']))

    elif(pilihan_menu == '2') :

        nama_buah = input('Masukkan Nama Buah : ')
        stock_buah = int(input('Masukkan Stock Buah : '))
        harga_buah = int(input('Masukkan Harga Buah : '))
        list_buah.append({
            'nama': nama_buah,
            'stock': stock_buah,
            'harga': harga_buah
        })
        print('Daftar Buah\n')
        print('Index\t| Nama  \t| Stock\t| Harga')
        for i in range(len(list_buah)) :
            print('{}\t| {}  \t| {}\t| {}'.format(i,list_buah[i]['nama'],list_buah[i]['stock'],list_buah[i]['harga']))

    elif(pilihan_menu == '3') :

        print('Daftar Buah\n')
        print('Index\t| Nama  \t| Stock\t| Harga')
        for i in range(len(list_buah)) :
            print('{}\t| {}  \t| {}\t| {}'.format(i,list_buah[i]['nama'],list_buah[i]['stock'],list_buah[i]['harga']))
        index_buah = int(input('Masukkan index buah yang ingin dihapus : '))
        del list_buah[index_buah]
        print('Daftar Buah\n')
        print('Index\t| Nama  \t| Stock\t| Harga')
        for i in range(len(list_buah)) :
            print('{}\t| {}  \t| {}\t| {}'.format(i,list_buah[i]['nama'],list_buah[i]['stock'],list_buah[i]['harga']))

    elif(pilihan_menu == '4') :

        print('Daftar Buah\n')
        print('Index\t| Nama  \t| Stock\t| Harga')
        for i in range(len(list_buah)) :
            print('{}\t| {}  \t| {}\t| {}'.format(i,list_buah[i]['nama'],list_buah[i]['stock'],list_buah[i]['harga']))
        while True :
            index_buah = int(input('Masukkan index buah yang ingin dibeli : '))
            qty_buah = int(input('Masukkan jumlah yang ingin dibeli : '))
            if(qty_buah > list_buah[index_buah]['stock']) :
                print('Stock tidak cukup, stock {} tinggal {}'.format(list_buah[index_buah]['nama'],list_buah[index_buah]['stock']))
            else :
                cart.append({
                    'nama': list_buah[index_buah]['nama'], 
                    'qty': qty_buah, 
                    'harga': list_buah[index_buah]['harga'], 
                    'index': index_buah
                })
            print('Isi Cart :')
            print('Nama\t| Qty\t| Harga')
            for item in cart :
                print('{}\t| {}\t| {}'.format(item['nama'], item['qty'], item['harga']))
            checker = input('Mau beli yang lain? (ya/tidak) = ')
            if(checker == 'tidak') :
                break

        print('Daftar Belanja :')
        print('Nama\t| Qty\t| Harga\t| Total Harga')
        total_harga = 0
        for item in cart :
            print('{}\t| {}\t| {}\t| {}'.format(item['nama'], item['qty'], item['harga'], item['qty'] * item['harga']))
            total_harga += item['qty'] * item['harga']    
        while True :
            print('Total Yang Harus Dibayar = {}'.format(total_harga))
            jml_uang = int(input('Masukkan jumlah uang : '))
            if(jml_uang > total_harga) :
                kembali = jml_uang - total_harga
                print('Terima kasih \n\nUang kembali anda : {}'.format(kembali))
                for item in cart :
                    list_buah[item['index']]['stock'] -= item['qty']
                cart.clear()
                break
            elif(jml_uang == total_harga) :
                print('Terima kasih')
                for item in cart :
                    list_buah[item['index']]['stock'] -= item['qty']
                cart.clear()
                break
            else :
                kekurangan = total_harga - jml_uang
                print('Uang anda kurang sebesar {}'.format(kekurangan))
                
    elif(pilihan_menu == '5') :
        break
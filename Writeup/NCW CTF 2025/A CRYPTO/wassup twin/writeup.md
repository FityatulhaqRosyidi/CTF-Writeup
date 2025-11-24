# Writeup - wassup twin

note : disarankan baca dan pahami challenge sebelum membaca writeup ini

## Observasi : 

**1. karena N kecil, p dan q mudah didapat dengan memfaktorkan N**

**2. tradeoff dari N kecil adalah nilai m bisa saja terpotong saat dienkripsi**

ukuran N = 2 ^ 64 = 256 ^ 8

artinya, jika message m lebih besar dari 8 byte, maka m akan terpotong

c = m^e mod N = (m mod N)^e mod N

ketika di dekripsi 

m0 = c^d mod N

yang kita peroleh adalah m yang sudah terpotong yaitu m0 (m0 = m mod N)

**3. diketahui informasi panjang flag adalah 23, dengan prefix "NCW{", dan encode flag dilakukan dengan big endian**

karena panjang flag 23, m terpotong

kita akan mencari k dimana m = m0 + kN

karena big endian, maka nilai prefix "NCW{" saat diubah ke byte akan signifikan, ini bisa digunakan untung mengurangi iterasi bruteforce


## Solusi : 

**1. cari p dan q**

**2. cari m0**

**3. lakukan bruteforce untuk mencari k yang cocok**


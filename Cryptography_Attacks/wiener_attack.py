import random
from math import isqrt
from Crypto.Util.number import long_to_bytes


def get_val_from_cf(a) :
    # fungsi ini menerima list continued fraction dan mengembalikan nilai pecahannya
    # list continued fraction yang dimaksud adalah list dengan format [a0, a1, a2, a3, ... , an] 
    # misalnya untuk continued fraction [1,2,3,2] maka hasilnya adalah 1 + 1/(2 + 1/(3 + 1/2)) = 23/16 
    # fungsi ini mengembalikan tuple (numerator,denominator)

    numerator = 1
    denominator = a[-1]
    a = a[:-1]
    # nilai num dan den awal adalah konstan untuk semua continued fraction yaitu 1 dan an (nilai terakhir di list)
    # kemudian nilai an dihapus dari list a

    while len(a) >= 1 :
    # looping while dengan syarat panjang list a minimal 1, agar bisa mengakses a[-1]

        numerator += (denominator * a[-1])
        denominator, numerator = numerator, denominator  
        # perhitungan numerator baru dilakukan dengan menambah nilai numerator lama dengan a terakhir dikali denominator lama
        # kemudian nilai numerator dan denominator ditukar sesuai dengan rumus continued fraction

        a = a[:-1]
        # nilai a terakhir dihapus dari list a

    # diluar loop sudah dipastikan list a sudah habis / kosong

    return (denominator, numerator)
    # return nilai den dan num yang sudah di swap lagi 
    # alasan di swap adalah karena pada akhir perhitungan, sebenarnya numerator dan denominator tidak perlu di swap 
    # dan karena pada loop terakhir mereka di swap, maka perlu di swap lagi untuk menetralkannya

def get_cf_from_val(numerator, denominator) : 
    # fungsi ini menerima dua bil bulat numerator dan denominator
    # kemudian menghasilkan list continued fraction dari pecahan tersebut
    # list continued fraction yang dimaksud adalah list dengan format [a0, a1, a2, a3, ... , an]
    # misalnya untuk pecahan 23/16 maka hasilnya adalah [1,2,3,2] karena 23/16 = 1 + 1/(2 + 1/(3 + 1/2))

    cf = []
    while denominator != 0 :
    # dilakukan iterasi sampai denominator bernilai 0, karena jika denominator 0 maka tidak bisa dilakukan pembagian dan modulo

        a = numerator // denominator 
        b = numerator % denominator
        cf.append(a)
        # disini idenya adalah memecah numerator dengan mencari nilai a dan b
        # dimana numerator = a * denominator + b 
        # bentuk pecahan akan menjadi sperti ini --> a + b/denominator
        # nilai a dimasukkan ke list continued fraction cf dan b menjadi numerator baru
        numerator, denominator = denominator, b
        # kemudian nilai numerator dan denominator ditukar untuk proses selanjutnya

    return cf

    # asumsi cf selalu memiliki panjang terbatas karena nilai input adalah bilangan rasional

def get_convergents_from_val(numerator, denominator) :
    # prosedur ini menerima pecahan
    # kemudian akan menampilkan semua konvergen dari pecahan tersebut mulai dari konvergen pertama sampai konvergen terakhir
    cf = get_cf_from_val(numerator, denominator)
    # mendapatkan continued fraction dari pecahan 

    for i in range(len(cf)) :
        val = get_val_from_cf(cf[:i + 1])
        print(f"Convergent {i} : {val[0]/val[1]} ~ {val[0]}/{val[1]}")

        # menhitung semua konvergen parsial dari cf

def is_vulnerable_to_wiener(d, n) :
    # fungsi ini menerima d dan n
    # mengembalikan True jika d memenuhi syarat wiener attack
    # syarat wiener attack adalah 
    #  d < 1/3 * n^(1/4)
    
    return d < isqrt(isqrt(n)) // 3
    


def attack(e : int, n : int) -> int :
    # simulasi wiener attack
    # menerima e sebagai numerator dan n sebagai denominator
    # akan dicari semua konvergen dari e/n untuk mendekati nilai k/d
    # syarat bahwa d diterima ada 3 yaitu
    # 1. d ganjil
    # 2. ed - 1 habis dibagi k
    # 3. akar solusi dari x^2 - (n - phi(n) + 1)x + n = 0 adalah p dan q 

    cf = get_cf_from_val(e, n)
    # ambil semua continued fraction dari e/n

    for i in range(1, len(cf)) :
    # mencoba konstruksi semua konvergen parsial dari cf

        val = get_val_from_cf(cf[:i + 1])
        k, d = val
        # boleh diuncomment
        # print(f'Trying val k : {k} , d : {d}')

        # cek syarat 1 : d harus ganjil
        if d % 2 == 0 :
            continue

        # cek syarat 2 : ed - 1 harus habis dibagi k
        if (e * d - 1) % k != 0 :
            continue

        # cek syarat 3 : akar dari x^2 - (n - phi(n) + 1)x + n = 0 adalah p dan q
        phi_n = (e * d - 1) // k
        a = 1
        b = -(n - phi_n + 1)
        c = n
        discriminant = b * b - 4 * a * c
        if discriminant < 0 :
            continue
        sqrt_discriminant = isqrt(discriminant)
        if sqrt_discriminant * sqrt_discriminant != discriminant :
            continue
        p = (-b + sqrt_discriminant) // (2 * a)
        q = (-b - sqrt_discriminant) // (2 * a)
        if p * q == n :
            # boleh diuncomment
            # print(f"Found p : {p}")
            # print(f"Found q : {q}")
            # print(f"Found d : {d}")
            return d



if __name__ == "__main__" :

    # ganti parameter disini
    N = 0xb8af3d3afb893a602de4afe2a29d7615075d1e570f8bad8ebbe9b5b9076594cf06b6e7b30905b6420e950043380ea746f0a14dae34469aa723e946e484a58bcd92d1039105871ffd63ffe64534b7d7f8d84b4a569723f7a833e6daf5e182d658655f739a4e37bd9f4a44aff6ca0255cda5313c3048f56eed5b21dc8d88bf5a8f8379eac83d8523e484fa6ae8dbcb239e65d3777829a6903d779cd2498b255fcf275e5f49471f35992435ee7cade98c8e82a8beb5ce1749349caa16759afc4e799edb12d299374d748a9e3c82e1cc983cdf9daec0a2739dadcc0982c1e7e492139cbff18c5d44529407edfd8e75743d2f51ce2b58573fea6fbd4fe25154b9964d
    e = 0x9ab58dbc8049b574c361573955f08ea69f97ecf37400f9626d8f5ac55ca087165ce5e1f459ef6fa5f158cc8e75cb400a7473e89dd38922ead221b33bc33d6d716fb0e4e127b0fc18a197daf856a7062b49fba7a86e3a138956af04f481b7a7d481994aeebc2672e500f3f6d8c581268c2cfad4845158f79c2ef28f242f4fa8f6e573b8723a752d96169c9d885ada59cdeb6dbe932de86a019a7e8fc8aeb07748cfb272bd36d94fe83351252187c2e0bc58bb7a0a0af154b63397e6c68af4314601e29b07caed301b6831cf34caa579eb42a8c8bf69898d04b495174b5d7de0f20cf2b8fc55ed35c6ad157d3e7009f16d6b61786ee40583850e67af13e9d25be3
    c = 0x3f984ff5244f1836ed69361f29905ca1ae6b3dcf249133c398d7762f5e277919174694293989144c9d25e940d2f66058b2289c75d1b8d0729f9a7c4564404a5fd4313675f85f31b47156068878e236c5635156b0fa21e24346c2041ae42423078577a1413f41375a4d49296ab17910ae214b45155c4570f95ca874ccae9fa80433a1ab453cbb28d780c2f1f4dc7071c93aff3924d76c5b4068a0371dff82531313f281a8acadaa2bd5078d3ddcefcb981f37ff9b8b14c7d9bf1accffe7857160982a2c7d9ee01d3e82265eec9c7401ecc7f02581fd0d912684f42d1b71df87a1ca51515aab4e58fab4da96e154ea6cdfb573a71d81b2ea4a080a1066e1bc3474

    d = attack(e, N)

    pt = long_to_bytes(pow(c, d, N))
    print(pt.decode())





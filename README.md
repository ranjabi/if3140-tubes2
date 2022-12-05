# IF3140-tubes2

# Simple Locking

## How to Run
```
cd SimpleLocking/src
```
```
python SimpleLocking.py
```
Ikuti panduan pada CLI.

## Format Input Schedule
```
R1(X) W2(X) W2(Y) W3(Y) W1(X) C1 C2 C3
```
- R merupakan kode operasi read, W kode operasi write, dan C kode operasi commit.
- Angka merupakan kode transaksi dan huruf dalam kurung merupakan kode item.
- Kode transaksi dan kode item dapat berupa angka atau huruf, tetapi tidak keduanya.
    - ✅ R1(X); R1(1); RX(1); RX(X)
    - ❌ R1X(X); R1(1X)
- Rekomendasi: R\<angka>(\<huruf>).

## Test Case
Test case tersimpan pada file .txt dalam direktori test.
- test1.txt: schedule tanpa deadlock
- test2.txt: schedule dengan deadlock

# Optimistic Concurrency Control

## How to Run
```
cd OCC
```
```
python Schedule.py input1.txt
```

## Test Case
- input1.txt: valid schedule
- input2.txt: invalid schedule, intersect operation
- input3.txt: invalid schedule, Ti<Tj and Tj complete write after Ti start validation phase

# Optimistic Concurrency Control

## How to Run
```
cd MVCC/src
```
```
python Main.py
```
Ikuti panduan pada CLI.

## Format Input Schedule
```
R1(X)
W2(X)
W2(Y)
W3(Y)
W1(Y)
R2(Y)
C1
C2
C3
```
- R merupakan kode operasi read, W kode operasi write, dan C kode operasi commit.
- Angka merupakan kode transaksi dan huruf dalam kurung merupakan kode item.

## Test Case
- test.txt: schedule with abort
- test2.txt: schedule without abort
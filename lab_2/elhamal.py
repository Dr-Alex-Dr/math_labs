import math
import random

privateKey = 0

def is_prime(a):
    if a < 2:
        return False
    for i in range(2, int(a ** 0.5 + 1)):
        if a % i == 0:
            return False
    else:
        return True

def generateKey():
    global privateKey
    p = 1
    while not is_prime(p):
        p = random.randint(10**2 , 10**5)
    g = getPrimitiveRoot(p)
    privateKey = random.randint(2, p -2)
    y = pow(g,privateKey,p)
    print("Открытый ключ: ", (y,g,p))
    print("Закрытый ключ: " , privateKey)
    return y,g,p

def getPrimitiveRoot(prime):
    euler_func = set(num for num in range (1, prime))
    for g in range(2, prime):
        current_func = set(pow(g, powers,prime) for powers in range (1, prime))
        if euler_func == current_func:
            return g

    
def encrypt(fileName):
    file  = open(fileName , 'r' , encoding='utf-8')
    mess = file.read()
    print('Исходное сообщение: ' , mess)
    file.close()
    y,g,p = generateKey()
    cryptFile = open('crypto.txt' , 'w')
    cryptFile.write(f'{p}\n')
    for sym in mess:
        sessionKey = random.randint(2, p-2)
        a = pow(g,sessionKey,p)
        b = (y**sessionKey*ord(sym))%p
        cryptFile.write(f'{a} {b}\n')
    cryptFile.close()

def decrypt():
    global privateKey
    cryptFile = open('crypto.txt' , 'r')
    decrypt = open('decrypt.txt' , 'w' , encoding='utf8')
    p = int(cryptFile.readline())
    
    for code in cryptFile.readlines():
        a, b = [int(x) for x in code.split()]
        symbol = chr((b * pow(a , p-1 - privateKey)%p))
        decrypt.write(symbol)
    cryptFile.close()
    decrypt.close()

encrypt('test.txt')
decrypt()
decr = open('decrypt.txt' , 'r' , encoding='utf8')
print('Результат дешифрования: ',decr.read())
decr.close()
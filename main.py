from hashlib import sha1
from Componentes.generan_prim import generan_prim_EM
from Componentes.inv import INV
from Componentes.expo_m import expo_m, expo_b
from Componentes.euclides import Euclides, EUCLIDES_EXTEND
from Componentes.rsa import RSA_KEY_GENERATOR

def mensaje_de_ataque():
    print("Ataque de módulo común - POSIBLE")

def CIFRA(m, k: tuple):
    arg1, arg2 = k
    return expo_m(m, arg1, arg2)



def ataque_1():
    e = 65537
    n = 999630013489
    P = e, n
    c = 747120213790

    prim, segu = generan_prim_EM(n)
    
    N = (prim - 1) * (segu - 1)
    S = INV(e, N), n

    m = CIFRA(c, S)
    cx = CIFRA(m, P)

    print("-----------------------EVALUAMOS SIENDO M EL MENSAJE, C EL CIFRADO Y LA P LA CLAVE PÚBLICA----------------------------") 
    print("m: {:}\nc: {:}\nP(m) = cx: {:}".format(m, cx, c == cx))

def ataque_2():
    e = 7
    n = 35794234179725868774991807832568455403003778024228226193532908190484670252364677411513516111204504060317568667
    P = e, n
    c = 35794234179725868774991807832568455403003778024228226193532908190484670252364677411513516052471686245831933544
    
    e_ = 11
    P_ = (e_, n)
    c_ = 35794234179725868774991807832568455403003778024228226193532908190484670252364665786748759822531352444533388184

    if (Euclides(e, e_ == 1) and Euclides(c_, n)):
        mensaje_de_ataque()

        z, x, y = EUCLIDES_EXTEND(e, e_)

        a = expo_m(INV(c, n), -x, n) if x < 0 else expo_m(c, x, n)
        b = expo_b(INV(c_, n), -y, n) if y < 0 else expo_b(c_, y, n)

        m = (a * b) % n
        cx = CIFRA(m, P)

        print("-----------------------EVALUAMOS SIENDO M EL MENSAJE, C EL CIFRADO Y LA P={e,n} LA CLAVE PÚBLICA----------------------------")
        print("\nm: {:}\ncx: {:}\nc: {:}\ncx = c: {:}".format(m, cx, c, cx == c))
    else:
        print("Es completamente inútil")

def ataque_3():
    k = 32
    P, S = RSA_KEY_GENERATOR(k)
    _, n = P
    M = b'ESTE ES UN MENSAJE DE PRUEBA'

    h = sha1()
    h.update(M)
    m = int(h.hexdigest(), 16)
    m %= n

    señal = CIFRA(m, S)
    u = CIFRA(señal, P)

    print("-----------------------HA SIDO GENERADO m A TRAVEZ DE M----------------------------")

    print("M: {:}\nm: {:}\nsign: {:}\nu: {:}\nu = m: {:}".format(M, m, señal, u, u == m))

print("EVALUACION DE LOS ATAQUES")        
print("Ataque 1")
ataque_1()
print("Ataque 2")
ataque_2()
print("Ataque 3")
ataque_3()
print("-----------------------FINALIZA EL ATAQUE----------------------------")

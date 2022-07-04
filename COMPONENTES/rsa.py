from Componentes.inv import INV
from Componentes.BITS_R import BITS_R
from Componentes.expo_m import expo_m
from Componentes.euclides import Euclides
from Componentes.generan_prim import generan_prim


def RSA_KEY_GENERATOR(bits):
    arg = bits // 2
    p = generan_prim(arg)
    q = generan_prim(arg)
    while p == q:
        q = generan_prim(arg)

    n = p * q
    phiN = (p - 1) * (q - 1)
    
    e = BITS_R(bits)
    while Euclides(e, phiN) != 1:
        e = BITS_R(bits)
    
    d = INV(e, phiN)
    return (e, n), (d, n)
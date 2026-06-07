import pytest

def soma(a,b):
    return a+b

def test_soma_dois_numeros_parte2():
    resultado = soma(4,6)
    assert resultado == 10

def test_soma_dois_numeros_parte1():
    resultado = soma(6,6)
    assert resultado == 10
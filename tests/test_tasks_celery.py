from tasks import somar, fatorial

def test_somar():
    resultado = somar.apply(args=[2, 3]).get()
    assert resultado == 5

def test_fatorial():
    resultado = fatorial.apply(args=[5]).get()
    assert resultado == 120
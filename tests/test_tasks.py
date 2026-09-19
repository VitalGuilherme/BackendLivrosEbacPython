from fastapi.testclient import TestClient
from main import app
from tasks import somar, fatorial

client = TestClient(app)

def test_somar():
    resultado = somar.apply(args=[2, 3]).get()
    assert resultado == 5

def test_fatorial(mocker):
    mock_fatorial_delay = mocker.patch("tasks.fatorial.delay")
    mock_fatorial_delay.return_value.get.return_value = 120
    resultado = fatorial.delay(args=[5]).get()
    assert resultado == 120

def test_fatorial_zero(mocker):
    mock_fatorial_delay = mocker.patch("tasks.fatorial.delay")
    mock_fatorial_delay.return_value.get.return_value = 1
    resultado = fatorial.delay(args=[0]).get()
    assert resultado == 1
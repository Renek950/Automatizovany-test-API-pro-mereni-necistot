import requests
import pytest

# Základní URL API 
BASE_URL = "https://to-barrel-monitor.azurewebsites.net"

@pytest.fixture
def create_barrel():
    """Vytvoří nový barel a vrátí jeho ID."""
    # Přidání požadovaných polí z error logu (Nfc, Qr, Rfid)
    payload = {
        "name": "Test Barrel",
        "Nfc": "123456",
        "Qr": "987654",
        "Rfid": "abcdef"
    }
    response = requests.post(f"{BASE_URL}/barrels", json=payload)
    assert response.status_code == 201
    return response.json()["id"]

def test_create_barrel():
    #Test vytvoření nového barelu.
    payload = {
        "name": "Test Barrel",
        "Nfc": "123456",
        "Qr": "987654",
        "Rfid": "abcdef"
    }
    response = requests.post(f"{BASE_URL}/barrels", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data



def test_get_barrels():
    #Test získání seznamu všech barelů.
    response = requests.get(f"{BASE_URL}/barrels")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_measurement(create_barrel):
    #Test přidání měření nečistot k barelu.
    barrel_id = create_barrel
    measurement_data = { "barrelId": barrel_id,"dirtLevel": 10.5, "weight": 0}
    response = requests.post(f"{BASE_URL}/measurements", json=measurement_data)
    assert response.status_code == 201

def test_get_measurements():
    #Test získání všech měření.
    response = requests.get(f"{BASE_URL}/measurements")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_barrel_details(create_barrel):
    #Test získání detailu konkrétního barelu.
    barrel_id = create_barrel
    response = requests.get(f"{BASE_URL}/barrels/{barrel_id}")
    assert response.status_code == 200    

def test_delete_barrel(create_barrel):
    #Test smazání konkrétního barelu.
    barrel_id = create_barrel
    response = requests.delete(f"{BASE_URL}/barrels/{barrel_id}")
    assert response.status_code == 204
    
def test_create_barrel_negative():
    #Test vytvoření nového barelu s nevalidními daty .
    payload = {
        "name": "fhsdjfhsdf",
        "Nfc": "123456",
        "Qr": "987654",
        "Rfid": "sfsfsf"
    }
    response = requests.post(f"{BASE_URL}/barrels", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "id" in data    


def test_get_barrels_negative():
    #Test získání seznamu všech barelů s invalidním get requestem (random).
    response = requests.get(f"{BASE_URL}/random")
    assert response.status_code == 404
    assert isinstance(response.json(), list)






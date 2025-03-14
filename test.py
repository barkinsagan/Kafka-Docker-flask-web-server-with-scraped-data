import requests

BASE_URL = 'http://localhost:5000/pokemon'

def test_create_pokemon():
    data = {
        "name": "Pikachu",
        "description": "Electric type Pokemon",
        "price": "100",
        "stock": "10"
    }
    response = requests.post(BASE_URL, json=data)
    print(f'Create Pokemon: {response.status_code} - {response.json()}')

def test_get_pokemons():
    response = requests.get(BASE_URL)
    print(f'Get All Pokemons: {response.status_code} - {response.json()}')

def test_get_pokemon(name):
    response = requests.get(f'{BASE_URL}/{name}')
    print(f'Get Pokemon ({name}): {response.status_code} - {response.json()}')

def test_update_pokemon(name):
    data = {
        "description": "Electric type Pokemon - Updated",
        "price": "120",
        "stock": "5"
    }
    response = requests.put(f'{BASE_URL}/{name}', json=data)
    print(f'Update Pokemon ({name}): {response.status_code} - {response.json()}')

def test_delete_pokemon(name):
    response = requests.delete(f'{BASE_URL}/{name}')
    print(f'Delete Pokemon ({name}): {response.status_code} - {response.json()}')

if __name__ == '__main__':
   
    test_create_pokemon()
    
    
    
    
    
    test_get_pokemon('Kakuna')
    
   
    test_update_pokemon('Pikachu')
    
    
    test_get_pokemon('Pikachu')
    
    
    test_delete_pokemon('Pikachu')
    
    
    test_get_pokemon('Pikachu')

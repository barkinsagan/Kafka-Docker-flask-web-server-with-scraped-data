from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
database_path='/app/data/pokemon.db'

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS pokemon (
    name TEXT PRIMARY KEY,
    description TEXT,
    price TEXT,
    stock TEXT
)
''')

conn.commit()

def get_db_connection():
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/pokemon', methods=['GET'])
def get_pokemons():
    conn = get_db_connection()
    pokemons = conn.execute('SELECT * FROM pokemon').fetchall()
    conn.close()
    return jsonify([dict(pokemon) for pokemon in pokemons])

@app.route('/pokemon/<string:name>', methods=['GET'])
def get_pokemon(name):
    conn = get_db_connection()
    pokemon = conn.execute('SELECT * FROM pokemon WHERE name = ?', (name,)).fetchone()
    conn.close()
    if pokemon is None:
        return jsonify({'error': 'Pokemon not found'}), 404
    return jsonify(dict(pokemon))

@app.route('/pokemon/<string:name>', methods=['PUT'])
def update_pokemon(name):
    conn = get_db_connection()
    pokemon = conn.execute('SELECT * FROM pokemon WHERE name = ?', (name,)).fetchone()
    if pokemon is None:
        conn.close()
        return jsonify({'error': 'Pokemon not found'}), 404
    
    data = request.json
    description = data.get('description', pokemon['description'])
    price = data.get('price', pokemon['price'])
    stock = data.get('stock', pokemon['stock'])
    
    conn.execute('''
    UPDATE pokemon
    SET description = ?, price = ?, stock = ?
    WHERE name = ?
    ''', (description, price, stock, name))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Pokemon updated successfully'})

@app.route('/pokemon', methods=['POST'])
def create_pokemon():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    conn = get_db_connection()
    conn.execute('''
    INSERT INTO pokemon (name, description, price, stock) VALUES (?, ?, ?, ?)
    ''', (name, description, price, stock))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Pokemon created successfully'}), 201

@app.route('/pokemon/<string:name>', methods=['DELETE'])
def delete_pokemon(name):
    conn = get_db_connection()
    pokemon = conn.execute('SELECT * FROM pokemon WHERE name = ?', (name,)).fetchone()
    if pokemon is None:
        conn.close()
        return jsonify({'error': 'Pokemon not found'}), 404
    
    conn.execute('DELETE FROM pokemon WHERE name = ?', (name,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Pokemon deleted successfully'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True) 

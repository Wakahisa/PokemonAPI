import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Pokedex Home Page</h1>
    <p>Explore pokemon entries.</p>'''

@app.route('/api/v1/resources/pokemon/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('pokedex.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_pokemon = cur.execute('SELECT * FROM pokemon;').fetchall()

    return jsonify(all_pokemon)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>No pokemon could be found.</p>", 404

@app.route('/api/v1/resources/pokemon', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    name = query_parameters.get('name')
    pokemon_type = query_parameters.get("pokemon_type")

    query = "SELECT * FROM pokemon WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if name:
        query += ' name=? AND'
        to_filter.append(name)
    if pokemon_type:
        query += ' pokemon_type=? AND'
        to_filter.append(pokemon_type)
    if not (id or name or pokemon_type):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('pokedex.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()
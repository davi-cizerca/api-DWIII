import psycopg2
from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

try:
    conn = psycopg2.connect("dbname=azar user=postgres password=3f@db host=164.90.152.205 port=80")
    print("Conexão com banco de dados local estabelecida com sucesso")
except Exception as e:
    print("Erro ao conectar ao banco de dados local:", e)
    exit(1)

cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS filmes (
        id SERIAL PRIMARY KEY,
        titulo VARCHAR(255) NOT NULL,
        ano INTEGER,
        tipo VARCHAR(50),
        poster TEXT,
        data_cache TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

@app.route("/filmes", methods=["GET"])
def listarFilmes():
    """Lista todos os filmes do banco de dados local"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM filmes ORDER BY data_cache DESC')
    
    filmes = []
    for item in cursor:
        filmes.append({
            "id": item[0],
            "titulo": item[1],
            "ano": item[2],
            "tipo": item[3],
            "poster": item[4],
            "data_cache": item[5].isoformat()
        })
    
    return jsonify(filmes)

@app.route("/filmes/<titulo>", methods=["GET"])
def buscarFilme(titulo):
    """Busca um filme primeiro no banco local, depois no OMDb"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM filmes WHERE titulo ILIKE %s', (f'%{titulo}%',))
    
    resultado = cursor.fetchone()
    if resultado:
        print(f"Filme '{titulo}' encontrado no banco local")
        return jsonify({
            "id": resultado[0],
            "titulo": resultado[1],
            "ano": resultado[2],
            "tipo": resultado[3],
            "poster": resultado[4],
            "data_cache": resultado[5].isoformat(),
            "fonte": "banco_local"
        })
    
    print(f"Buscando filme '{titulo}' no OMDb...")
    API_KEY = "1a8427f2" 
    response = requests.get(f"http://www.omdbapi.com/?t={titulo}&apikey={API_KEY}")
    dados = response.json()
    
    if dados.get("Response") == "True":
        cursor.execute('''
            INSERT INTO filmes (titulo, ano, tipo, poster)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        ''', (dados["Title"], int(dados["Year"]), dados["Type"], dados["Poster"]))
        conn.commit()
        
        novo_id = cursor.fetchone()[0]
        print(f"Filme '{titulo}' salvo no banco local")
        
        return jsonify({
            "id": novo_id,
            "titulo": dados["Title"],
            "ano": int(dados["Year"]),
            "tipo": dados["Type"],
            "poster": dados["Poster"],
            "data_cache": datetime.now().isoformat(),
            "fonte": "omdb"
        })
    
    return jsonify({"erro": "Filme não encontrado"}), 404

@app.route("/filmes/<int:id>", methods=["DELETE"])
def deletarFilme(id):
    """Remove um filme do banco de dados local"""
    cursor = conn.cursor()
    cursor.execute('DELETE FROM filmes WHERE id = %s', (id,))
    conn.commit()
    
    return jsonify({
        "mensagem": "Filme removido do banco local com sucesso",
        "id": id
    })

@app.route("/filmes/limpar", methods=["POST"])
def limparCache():
    """Limpa todo o banco de dados local"""
    cursor = conn.cursor()
    cursor.execute('DELETE FROM filmes')
    conn.commit()
    
    return jsonify({
        "mensagem": "Banco de dados local limpo com sucesso"
    })

if __name__ == '__main__':
    app.run(debug=True) 
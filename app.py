from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>API da Biblioteca Virtual</h1>"

import sqlite3

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS LIVROS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                image_url TEXT NOT NULL
                )
        """)
init_db()

@app.route('/doar', methods =["POST"])
def doar():
    
    dados = request.get_json()
    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    with sqlite3.connect('database.db') as conn:
        conn.execute(f"""
        INSERT INTO LIVROS (titulo, categoria, autor, image_url)
        VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
    """)
        
    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro":"Todos os campos são obrigatórios"}), 400

    conn.commit()

    return jsonify({"mensagem":"Livro cadastrado com sucesso"}), 201

@app.route("/livros", methods=["GET"])
def listar_livros():
    
    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()
        livros_formatados = []
        for item in livros:
            dicionario = {
                "id": item[0],
                "titulo": item[1],
                "categoria": item[2],
                "autor": item[3],
                "image_url": item[4]
            }
        livros_formatados.append(dicionario)
    
    return jsonify(livros_formatados)



if __name__ == "__main__":
    app.run(debug=True)



#  source venv/Scripts/activate ---> ativar o ambiente virtual
#  python app.py ---> abrir no navegador
# reqbin.com ---> site para ver o código da API como json
# Postman -> POST -> colar endpoint com caminho da api -> body -> raw -> mudar TEXT para JSON
#
#  {
#     "titulo":"a",
#     "categoria":"b",
#     "autor":"c",
#     "image_url":"d"
# }
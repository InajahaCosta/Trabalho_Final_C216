from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os

app = Flask(__name__)

# Definindo as variáveis de ambiente
API_BASE_URL = "http://backend:8000"

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro
@app.route('/cadastro', methods=['GET'])
def inserir_item_form():
    return render_template('cadastro.html')

# Rota para enviar os dados do formulário de cadastro para a API
@app.route('/inserir', methods=['POST'])
def inserir_item():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano = request.form['ano']
    genero = request.form['genero']
    quantidade = request.form['quantidade']

    payload = {
        'titulo' : titulo,
        'autor' : autor,
        'ano': ano,
        'genero' : genero,
        'quantidade': quantidade
    }

    response = requests.post(f'{API_BASE_URL}/api/v1/livros/', json=payload)
    
    if response.status_code == 201:
        return redirect(url_for('listar_livros'))
    else:
        return "Erro ao inserir livro", 500

# Rota para listar todos os livros
@app.route('/estoque', methods=['GET'])
def listar_livros():
    response = requests.get(f'{API_BASE_URL}/api/v1/livros/')
    try:
        livros = response.json()
    except:
        livros = []
    return render_template('estoque.html', livros=livros)


@app.route("/emprestimo/", methods=["POST"])
def emprestar_livro():
    try:
        # Recebe os dados da requisição
        data = request.get_json()
        id_livro = data.get("id_livro")
        nome_usuario = data.get("nome_usuario")
        
        # Lógica para registrar o empréstimo (exemplo simples)
        # Aqui você pode integrar com banco de dados ou lógica de validação
        if not id_livro or not nome_usuario:
            return jsonify({"error": "ID do livro e nome do usuário são necessários"}), 400
        
        # Suponha que o empréstimo seja feito com sucesso
        return jsonify({"message": f"Empréstimo do livro {id_livro} para {nome_usuario} realizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

# Rota para resetar o banco de dados
@app.route('/reset-database', methods=['GET'])
def resetar_database():
    response = requests.delete(f"{API_BASE_URL}/api/v1/livros/")
    
    if response.status_code == 200:
        return render_template('confirmacao.html')
    else:
        return "Erro ao resetar o banco de dados", 500
    

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')

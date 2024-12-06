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
        'titulo': titulo,
        'autor': autor,
        'ano': ano,
        'genero': genero,
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

# Rota de emprestimo
@app.route('/emprestimo', methods=['GET', 'POST'])
def emprestimo():
    if request.method == 'POST':
        print("Form data recebida:", request.form)
        
        livro_id = request.form.get('livro')  
        nome_usuario = request.form.get('nome_usuario')  

        if not livro_id or not nome_usuario:
            print("Erro: Dados inválidos no formulário")
            return "Dados inválidos no formulário", 400

        payload = {
            'id_livro': int(livro_id),  
            'nome_usuario': nome_usuario
        }

        print("Payload para API:", payload)

        response = requests.post(f'{API_BASE_URL}/api/v1/emprestimos/', json=payload)

        if response.status_code == 200:
            api_response = response.json() 
            print("Sucesso na API:", api_response)
            return render_template('emprestimo.html', mensagem=f"Emprestimo realizado com sucesso!", sucesso=True)
        else:
            print("Erro ao realizar a emprestimo, status code:", response.status_code)
            return render_template('emprestimo.html', mensagem=f"Erro ao realizar emprestimo. Status code: {response.status_code}", sucesso=False)

    response = requests.get(f'{API_BASE_URL}/api/v1/livros/')
    livros = response.json() if response.status_code == 200 else []

    return render_template('emprestimo.html', livros=livros)


# Rota de devolução
@app.route('/devolucao', methods=['GET', 'POST'])
def devolucao():
    if request.method == 'POST':
        print("Form data recebida:", request.form)

        livro_id = request.form.get('livro')  
        nome_usuario = request.form.get('nome_usuario') 

        if not livro_id or not nome_usuario:
            print("Erro: Dados inválidos no formulário")
            return render_template('devolucao.html', mensagem="Dados inválidos no formulário", sucesso=False)

        payload = {
            'id_livro': int(livro_id), 
            'nome_usuario': nome_usuario
        }

        print("Payload para API:", payload)

        response = requests.post(f'{API_BASE_URL}/api/v1/devolucoes/', json=payload)

        if response.status_code == 200:
            api_response = response.json() 
            print("Sucesso na API:", api_response)
            return render_template('devolucao.html', mensagem=f"Devolução realizada com sucesso!", sucesso=True)
        else:
            print("Erro ao realizar a devolução, status code:", response.status_code)
            return render_template('devolucao.html', mensagem=f"Erro ao realizar a devolução. Status code: {response.status_code}", sucesso=False)

    response = requests.get(f'{API_BASE_URL}/api/v1/livros/')
    livros = response.json() if response.status_code == 200 else []

    return render_template('devolucao.html', livros=livros, mensagem=None, sucesso=None)

# Rota excluir livro
@app.route('/excluir', methods=['GET', 'POST'])
def excluir_livro():
    if request.method == 'POST':
        livro_id = request.form.get('livro_id')
        if not livro_id:
            return render_template('excluir.html', livros=[], mensagem="Livro não selecionado", sucesso=False)
        
        response = requests.delete(f'{API_BASE_URL}/api/v1/livros/{livro_id}')
        if response.status_code == 204:
            return render_template('excluir.html', livros=[], mensagem="Livro excluído com sucesso", sucesso=True)
        else:
            return render_template('excluir.html', livros=[], mensagem="Erro ao excluir livro", sucesso=False)
    
    response = requests.get(f'{API_BASE_URL}/api/v1/livros/')
    livros = response.json() if response.status_code == 200 else []
    return render_template('excluir.html', livros=livros)


# Rota para resetar o banco de dados
@app.route('/reset-database', methods=['GET'])
def resetar_database():
    response = requests.delete(f"{API_BASE_URL}/api/v1/livros/")
    
    if response.status_code == 200:
        return render_template('confirmacao.html')
    else:
        return "Erro ao resetar o banco de dados", 500

# Bloco principal
if __name__ == '__main__':
    app.run(debug=True, port=3003, host='0.0.0.0')

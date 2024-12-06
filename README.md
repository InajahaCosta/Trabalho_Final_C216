# Sistema de Gerenciamento de Biblioteca

Este é um sistema de gerenciamento de biblioteca que permite aos usuários cadastrar livros, atualizar informações, excluir livros, realizar empréstimos e devoluções.

## Autora
- Inajaha Costa Vilas - 318 - GES - (inajaha.costa@ges.inatel.br)


## Tecnologias Utilizadas

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend**: [Flask](https://flask.palletsprojects.com/)
- **Banco de Dados**: [PostgreSQL](https://www.postgresql.org/)
- **Containers**: [Docker](https://www.docker.com/)
- **Testes de API**: [Postman](https://www.postman.com/)

## Funcionalidades

- **Cadastro de livros**: Adicionar novos livros ao sistema.
- **Atualização de livros**: Atualizar as informações de livros cadastrados.
- **Exclusão de livros**: Remover livros do sistema.
- **Empréstimos**: Registrar o empréstimo de livros aos usuários.
- **Devoluções**: Registrar a devolução de livros emprestados.

## Como Configurar e Executar

### Pré-requisitos

Certifique-se de ter o [Docker](https://www.docker.com/) instalado em sua máquina.

### Passos para Executar

1. Clone este repositório para sua máquina local:
   ```bash 
   git clone https://github.com/InajahaCosta/Trabalho_Final_C216.git
   
2. Entre no diretório do projeto:
   ```bash 
   cd Trabalho_Final_C216
   
3. Execute o Docker:
   ```bash 
   docker-compose up --build

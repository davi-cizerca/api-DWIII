Documentação

# API de Filmes com Cache Local (Flask + PostgreSQL)

## Descrição
Esta aplicação é uma API RESTful desenvolvida com Flask que permite buscar, listar, remover e armazenar dados de filmes. Ela utiliza PostgreSQL como banco de dados local para armazenar filmes previamente consultados, funcionando como uma camada de cache. Se um filme não for encontrado localmente, a aplicação consulta a API externa OMDb (Open Movie Database) e salva o resultado.

---

## Tecnologias Utilizadas
- Python 3
- Flask
- PostgreSQL
- Psycopg2 (driver PostgreSQL)
- Requests (requisições HTTP)

---

## Estrutura do Banco de Dados
**Tabela: `filmes`**

| Campo       | Tipo         | Descrição                         |
|-------------|--------------|-----------------------------------|
| id          | SERIAL       | Chave primária                    |
| titulo      | VARCHAR(255) | Título do filme                   |
| ano         | INTEGER      | Ano de lançamento                 |
| tipo        | VARCHAR(50)  | Tipo (ex: movie, series)          |
| poster      | TEXT         | URL do pôster                     |
| data_cache  | TIMESTAMP    | Data em que foi salvo             |

A tabela é criada automaticamente ao iniciar a aplicação.

---

## Endpoints

### GET `/filmes`
Lista todos os filmes salvos no banco, ordenados pela data de inserção mais recente.

### GET `/filmes/<titulo>`
Busca um filme pelo título:
- Primeiro verifica se existe no banco local usando busca case-insensitive (`ILIKE`).
- Se não encontrar, faz requisição à API OMDb, armazena no banco e retorna os dados.

### DELETE `/filmes/<id>`
Remove o filme com o ID especificado do banco local.

### POST `/filmes/limpar`
Apaga **todos os registros** da tabela `filmes`. Útil para testes ou reinicialização do cache.

---

## Como Executar o Projeto

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure o banco de dados:**
Certifique-se de que o PostgreSQL esteja rodando e atualize a string de conexão no código:
```python
psycopg2.connect("dbname=azar user=postgres password=3f@db host=164.90.152.205 port=80")
```

4. **Inicie o servidor Flask:**
```bash
python app.py
```
A aplicação estará disponível em `http://localhost:5000`

---

## Exemplos de Requisições HTTP

As chamadas abaixo são feitas para `http://localhost:5000`

### 1. Listar todos os filmes
```http
GET http://localhost:5000/filmes
Content-Type: application/json
```

### 2. Buscar filme: Inception
```http
GET http://localhost:5000/filmes/Inception
Content-Type: application/json
```

### 3. Buscar filme: The Matrix
```http
GET http://localhost:5000/filmes/The%20Matrix
Content-Type: application/json
```

### 4. Deletar filme pelo ID
```http
DELETE http://localhost:5000/filmes/1
Content-Type: application/json
```

### 5. Limpar o cache (remover todos os filmes)
```http
POST http://localhost:5000/filmes/limpar
Content-Type: application/json
```

---

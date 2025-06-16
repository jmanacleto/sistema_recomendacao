## 1. Objetivo do Projeto

[cite_start]O objetivo principal deste projeto é desenvolver um sistema de recomendação utilizando FastAPI para a criação da API e Docker para a conteinerização da aplicação[cite: 2]. [cite_start]Esta atividade visa proporcionar experiência prática na construção e implantação de sistemas de recomendação, além de familiarizar com ferramentas modernas de desenvolvimento e implantação[cite: 3].

## 2. Estrutura do Projeto

O projeto está estruturado da seguinte forma:

```
├── app/
│   ├── __init__.py
│   ├── data.py
│   ├── model.py
│   ├── utils.py
│   └── model.py
├── data/
│   └── netflix_titles.csv
├── static/
│   └── index.html
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

## 3. Módulos

### 3.1. `main.py`

Este arquivo contém a aplicação FastAPI. Ele configura a API, serve o frontend, carrega os dados, inicializa o modelo de recomendação e define o endpoint de recomendação.

* `app = FastAPI(title="Recomendador Netflix")`: Inicializa a aplicação FastAPI.
* `app.mount("/static", StaticFiles(directory="static"), name="static")`: Monta o diretório `static` para servir arquivos estáticos como HTML, CSS e JavaScript.
* `@app.get("/")`: Redireciona a URL raiz para `/frontend`.
* `@app.get("/frontend")`: Serve o arquivo `index.html` localizado no diretório `static`.
* `df = carregar_dados()`: Carrega o conjunto de dados da Netflix usando a função `carregar_dados` de `app.data`.
* `modelo = RecomendadorNetflix(df)`: Inicializa o modelo de recomendação usando os dados carregados.
* `@app.get("/recomendar/{titulo}")`: Este é o endpoint principal da API de recomendação. Ele recebe um `titulo` como entrada, obtém recomendações do modelo e as retorna. Se o título não for encontrado, ele levanta uma exceção HTTP 404.

### 3.2. `app/data.py`

Este módulo é responsável por carregar e pré-processar o conjunto de dados.

* `carregar_dados()`: Lê o arquivo `netflix_titles.csv` em um Pandas DataFrame, remove as linhas com valores ausentes em `title` ou `description`, e redefine o índice do DataFrame antes de retorná-lo.

### 3.3. `app/model.py`

Este módulo contém a lógica do modelo de recomendação.

* Classe `RecomendadorNetflix`:
    * `__init__(self, df: pd.DataFrame)`:
        * Inicializa o `TfidfVectorizer` para converter descrições de texto em recursos TF-IDF, removendo stop words em inglês.
        * Ajusta e transforma a coluna `description` do DataFrame de entrada para criar a `tfidf_matrix`.
        * Cria uma série Pandas `indices` mapeando títulos de filmes aos seus índices correspondentes no DataFrame.
    * `recomendar(self, titulo: str, n=5)`:
        * Verifica se o `titulo` fornecido existe nos `indices`. Caso contrário, retorna uma lista vazia.
        * Recupera o índice do `titulo` fornecido.
        * Calcula a similaridade de cosseno entre o vetor TF-IDF do título de entrada e todos os outros títulos usando `linear_kernel`.
        * Classifica as pontuações de similaridade em ordem decrescente e obtém os índices dos `n` itens mais semelhantes.
        * Retorna um dicionário dos títulos recomendados e suas descrições.

## 4. `docker-compose.yml`

[cite_start]Este arquivo é usado para definir e executar os contêineres Docker para a aplicação[cite: 13].

* [cite_start]`version: '3.9'`: Especifica a versão do formato do arquivo Docker Compose[cite: 1].
* [cite_start]`services:`: Define os serviços para a aplicação[cite: 1].
    * [cite_start]`netflix-recommendation:`: Define o serviço de recomendação[cite: 1].
        * [cite_start]`build: .`: Informa ao Docker para construir a imagem usando o `Dockerfile` no diretório atual[cite: 1].
        * [cite_start]`ports:`: Mapeia a porta 8000 do host para a porta 8000 do contêiner, permitindo o acesso à aplicação FastAPI[cite: 1].
        * [cite_start]`volumes:`: Monta o diretório atual (`.`) no diretório `/app` dentro do contêiner, permitindo alterações de código em tempo real sem reconstruir a imagem[cite: 1].

## 5. `requirements.txt`

Este arquivo lista as dependências Python necessárias para o projeto.

* [cite_start]`fastapi`: Para construir a API web[cite: 1].
* [cite_start]`uvicorn`: Um servidor ASGI para executar a aplicação FastAPI[cite: 1].
* [cite_start]`pandas`: Para manipulação e análise de dados[cite: 1].
* [cite_start]`scikit-learn`: Para implementar o modelo de recomendação (TF-IDF e similaridade de cosseno)[cite: 1].

## 6. Como Executar

### 6.1. Pré-requisitos

* Docker e Docker Compose instalados.
* Python 3.x

### 6.2. Executando com Docker Compose

1.  Navegue até o diretório raiz do projeto onde o `docker-compose.yml` está localizado.
2.  Execute o seguinte comando para construir e iniciar os serviços:

    ```bash
    docker-compose up --build
    ```

3.  A aplicação estará acessível em `http://localhost:8000`.

### 6.3. Executando Localmente (sem Docker)

1.  Instale as dependências necessárias:

    ```bash
    pip install -r requirements.txt
    ```

2.  Execute a aplicação FastAPI:

    ```bash
    uvicorn main:app --reload
    ```

3.  A aplicação estará acessível em `http://127.0.0.1:8000`.

## 7. Endpoints da API

* **GET `/`**: Redireciona para `/frontend`.
* **GET `/frontend`**: Serve o arquivo `index.html`, fornecendo a interface do usuário.
* **GET `/recomendar/{titulo}`**:
    * **Descrição**: Retorna uma lista de filmes ou programas de TV recomendados com base no título de entrada.
    * **Parâmetros**:
        * `titulo` (string): O título do filme ou programa de TV para o qual obter recomendações.
    * **Respostas**:
        * `200 OK`: Recomendação bem-sucedida. Retorna um objeto JSON com uma lista de títulos e descrições recomendados.
        * `404 Not Found`: Se o título fornecido não for encontrado no conjunto de dados.

## 8. Exemplo de Uso

Uma vez que a aplicação esteja em execução, você pode acessar o frontend em `http://localhost:8000/frontend` (ou `http://127.0.0.1:8000/frontend` se estiver executando localmente).

Você pode testar a API de recomendação diretamente navegando para:

* `http://localhost:8000/recomendar/Lupin`
* `http://localhost:8000/recomendar/La%20casa%20de%20papel`

Exemplos de recomendações bem-sucedidas para "Lupin" e "La casa de papel.

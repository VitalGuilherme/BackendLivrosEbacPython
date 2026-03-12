# Projeto raiz, uma API de livros (gerenciador de bibliotecas). 

# Tecnologia Utilizadas

**Framework:** FastAPI (Assíncrono)
* **Banco de Dados:** SQLAlchemy com SQLite (via aiosqlite para suporte async)
* **Cache:** Redis (Implementação de padrão Cache-Aside para otimização de consultas)
* **Gerenciamento de Dependências:** Poetry
* **Infraestrutura:** Docker & Docker Compose (Substituindo a implementação inicial em Podman para melhor integração com Redis no Windows)

 Utiliza o FastAPI como framework base e o sqlalchemy e aiosqlite para o banco de dados.

 O Poetry instala gerencia as dependências do projeto.

 O Dockerfile com instruções pré-definidas, cria a imagem docker e guarda o projeto um container.

# Com o Podman como gerenciador de container, através dos comandos, cria uma imagem docker copiando a imagem salva do repositorio local e por fim sobre para a web pela porta definida no docker-compose.yml

# Comandos Podman.
# podman machine init 
# podman machine start
# podman-compose build
# podman-compose up -d

## Jornada de Infraestrutura e Desafios

Originalmente, o projeto foi concebido utilizando o **Podman** como gerenciador de containers. No entanto, durante a evolução para a fase de caching com **Redis**, migramos para o **Docker Desktop** para garantir uma integração mais fluida e estável com o ecossistema Windows via **WSL 2**.

### O processo de configuração incluiu:
1.  **Ativação de Virtualização:** Configuração de BIOS e recursos do Windows.
2.  **Configuração do WSL 2:** Instalação do subsistema Linux para garantir performance nativa de containers.
3.  **Docker Desktop Engine:** Configuração do motor de containers para orquestrar a API e o Redis simultaneamente.

## Como Executar o Projeto

### Pré-requisitos
* Docker Desktop instalado e rodando (com suporte a WSL 2).

### Passo a Passo
1.  **Clone o repositório e acesse a pasta:**
    ```bash
    cd Ebac_ProjetoBackendPythonLivros
    ```

2.  **Suba os containers (API + Redis):**
    ```bash
    docker-compose up --build
    ```

3.  **Acesse a documentação automática:**
    * Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
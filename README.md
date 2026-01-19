# Projeto raiz, uma API de livros (gerenciador de bibliotecas). 

# Utiliza o FastAPI como framework base e o sqlalchemy e aiosqlite para o banco de dados.

# O Poetry instala gerencia as dependências do projeto.

# O Dockerfile com instruções pré-definidas, cria a imagem docker e guarda o projeto um container.

# Com o Podman como gerenciador de container, através dos comandos, cria uma imagem docker copiando a imagem salva do repositorio local e por fim sobre para a web pela porta definida no docker-compose.yml

# Comandos Podman.
# podman machine init 
# podman machine start
# podman-compose build
# podman-compose -d

#!/bin/bash

DEPLOYMENT="deployment.yaml"
SERVICE="service.yaml"

# Verifica se minikube está instalado e rodando
if command -v minikube >/dev/null 2>&1; then
    echo "Verificando se o minikube está rodando..."
    if ! minikube status | grep -q "Running"; then
        echo "Minikube não está rodando. Iniciando o minikube..."
        minikube start
    else
        echo "Minikube já está rodando."
    fi
else
    echo "Minikube não está instalado, certifique-se de ter um cluster Kubernetes local ativo."
fi

echo "Aplicando o deployment..."
kubectl apply -f $DEPLOYMENT

echo "Aplicando o service..."
kubectl apply -f $SERVICE

echo "Aguarde os pods iniciarem..."
kubectl wait --for=condition=available --timeout=60s deployment/livros-api

echo "Iniciando port-forward para localhost:8000 -> service porta 80..."

# Rodar o port-forward em background
kubectl port-forward svc/livros-api-service 8000:80 > /dev/null 2>&1 &

# Dá um tempo para garantir que o port-forward está ativo
sleep 3

# Detecta sistema operacional para abrir o navegador
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost:8000
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8000
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
    start http://localhost:8000
else
    echo "Abra o seu navegador e acesse http://localhost:8000"
fi

echo "Aplicação disponível em http://localhost:8000"
echo "Pressione Ctrl+C para encerrar o port-forward e sair."
# Mantém o script rodando para que o port-forward continue ativo
wait
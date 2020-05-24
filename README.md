# Brasil em Números
---

Brasil em números é um dashboard que facilita a divulgação de informações públicas brasileiras para que a população possa entender melhor como o Brasil está sendo administrado. Esse projeto é uma tentativa de simplificar o consumo de dados públicos de uma forma mais acessível.

Idéia concebida por @fvall e @juliano.

## Executando

### Via Python

#### Requsitos

- Python 3.6 ou superior

> Observação: Caso tenha também tenha instalado python versão 2.7, substitua `python` por `python3` e `pip` por `pip3` nos comandos abaixo.

#### Instalação

- Clone o repositório
- Crie um virtual environment

```Python
python -m venv venv/
```

- Ative o virtual environment

```
source venv/bin/activate
```

- Instale os pacotes necessários


```Python
pip install -r requirements.txt
```

- Se não for rodar o dashboard, você pode desativar o virtual environment

```
deactivate
```

#### Rodando o dashboard

- Caso o virutal enviroment não esteja ativado, ative-o usando os comandos acima.

```Python
python dash.py
```

O dashboard estará acessível em localhost:5000 no seu browser predileto.

## Via Docker

A execução via docker é bem mais fácil

- Crie a imagem

````
docker build -t ben .
````

- Rode a imagem

````
docker run --rm -it -p 5000:5000 ben
````


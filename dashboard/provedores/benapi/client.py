import requests

URL = "http://localhost:8080/api/v1/despesas-publicas"


def despesas_publicas(codigo):
    query_params = {'codigoOrgaoSuperior': codigo}
    return requests.get(URL, stream=True, params=query_params).json()

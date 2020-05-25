
import re
import os
import pandas as pd
import requests
import concurrent.futures

from numbers import Number
from functools import reduce
from collections.abc import Iterable
from collections import OrderedDict, ChainMap
from ..benapi import client

loc = os.path.abspath(
    os.path.dirname(__file__)
)


def despesas():

    arquivos = os.listdir(loc)
    arquivos = filter(
        lambda a: re.search("^despesas_\\d{2}_\\d{4}\\.csv$", a) is not None,
        arquivos
    )

    desp = pd.concat(
        map(
            lambda a: pd.read_csv(os.path.join(loc, a), delimiter = ";"),
            arquivos
        ),
        sort = False
    )

    # -----------------------------
    #  Remove colunas com códigos
    # -----------------------------

    cols = filter(
        lambda c: re.search(r'código', c, re.I) is None,
        desp.columns
    )

    cols = list(cols)

    # -----------------------
    #  Renomeando as colunas
    # -----------------------

    anomes = {
        'Ano e mês do lançamento' : 'ano_mes'
    }

    nome = {
        c : re.sub(r'^Nome ', '', c) for c in cols if c.startswith('Nome ')
    }

    valor = {
        c : c.replace(
            'Valor', ''
        ).replace(
            'a Pagar ', ''
        ).replace(
            '(R$)', ''
        ) for c in cols if c.startswith('Valor ')
    }

    novo_nome = ChainMap(anomes, nome, valor)
    return desp[list(cols)].rename(
        columns = novo_nome
    )


def orgaos_superiores():
    return {
        20000 : 'Presidência da República',
        22000 : 'Ministério da Agricultura, Pecuária e Abastec',
        24000 : 'Ministério da Ciência, Tecnologia, Inovações',
        25000 : 'Ministério da Economia',
        26000 : 'Ministério da Educação',
        30000 : 'Ministério da Justiça e Segurança Pública',
        32000 : 'Ministério de Minas e Energia',
        33000 : 'Ministério da Previdência Social',
        35000 : 'Ministério das Relações Exteriores',
        36000 : 'Ministério da Saúde',
        37000 : 'Controladoria-Geral da União',
        39000 : 'Ministério da Infraestrutura',
        44000 : 'Ministério do Meio Ambiente',
        52000 : 'Ministério da Defesa',
        53000 : 'Ministério do Desenvolvimento Regional',
        54000 : 'Ministério do Turismo',
        55000 : 'Ministério da Cidadania',
        63000 : 'Advocacia-Geral da União',
        81000 : 'Ministério da Mulher, Família e Direitos Huma'
    }


def despesas_publicas_por_id(ids):

    url = client.URL
    if not isinstance(ids, Iterable):
        ids = int(ids)
        url += + "/" + str(ids)
        linha = requests.get(url, stream = True)
        if linha.status_code != 200:
            raise ValueError(f"Não há dados para linha {ids}")

        return pd.DataFrame({0 : linha.json()}, orient = 'index')
    
    ids = [int(i) for i in ids]
    url = [url + "/" + str(i) for i in ids]
    with concurrent.futures.ThreadPoolExecutor(100) as executor:
        output = executor.map(lambda u: requests.get(u), url)

    output = filter(lambda x: x.status_code == 200, output)
    return pd.DataFrame.from_dict({
        idx : o.json() for idx, o in enumerate(output)
    }, orient = 'index')


def despesas_publicas_por_codigo(codigo, **params):

    params  = dict(**params)
    filtros = [
        filtra_campo(key, val) for key, val in params.items()
    ]
    
    # ----------------------------
    #  Filtra usando condição "E"
    # ----------------------------

    def filtro(json):
        def resultado(x):
            return reduce(lambda f, g: g(f), filtros, x)
        
        return resultado(json)

    linhas = map(processa_json, client.despesas_publicas(codigo))
    if filtros:
        linhas = filtro(linhas)

    return pd.DataFrame.from_dict(
        {idx : linha for idx, linha in enumerate(linhas)},
        orient = 'index'
    )


def despesas_publicas(**params):
    
    params = dict(**params)
    codigo = params.pop('codigo', None)
    if codigo is None:
        codigo = list(orgaos_superiores().keys())

    if isinstance(codigo, str):
        try:
            codigo = int(codigo)
        except ValueError:
            return despesas_publicas(**params)
    
    if isinstance(codigo, Number):
        codigo = [int(codigo)]

    max_threads = len(orgaos_superiores())
    partial = lambda cdg: despesas_publicas_por_codigo(cdg, **params)
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        output = executor.map(partial, codigo)

    output = pd.concat(output, sort = False).reset_index(drop = True)
    return output


def filtra_campo(campo, valor):

    if isinstance(valor, str) or (not isinstance(valor, Iterable)):
        valor = {valor}
    else:
        valor = set(valor)

    if isinstance(campo, Iterable) and (not isinstance(campo, str)):
        raise ValueError(
            f"Campo tem que ser uma uníca string! Campo -> {campo}"
        )

    def filtro(iterable):
        return filter(lambda x: x.get(campo) in valor, iterable)
    
    return filtro


def processa_json(j):

    ordem = list(j.keys())
    output = OrderedDict()

    # ----------------------------
    #  Columnas com nome 'codigo'
    #  não são necessárias
    # ----------------------------

    desnecessario = {
        'Modalidade da Despesa',
        'Nome Grupo de Despesa',
        'Nome Programa Governo'
    }

    for c in ordem:

        if c in desnecessario:
            continue

        if c == 'codigoOrgaoSuperior':
            output[c] = j[c]
            continue

        if c == 'lancamento':
            output[c] = j[c]
            if j[c] is None:
                ano = None
                mes = None
            else:
                ano, mes, *_ = j[c].split("/")
                ano = int(ano)
                mes = int(mes)
                
            output['ano'] = ano
            output['mes'] = mes
            continue

        if re.search('^codigo', c, re.I) is None:
            output[c] = j[c]

    return output

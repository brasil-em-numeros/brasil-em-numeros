import re
import pandas as pd

from collections import ChainMap
from .downloader import download


def despesas():

    def url(mes):
        return f'https://raw.githubusercontent.com/brasil-em-numeros/public-data/master/portaltransparencia/despesas-execucao/2020{mes:02d}.csv'

    url_list = [url(mes) for mes in range(1, 6)]

    desp = pd.concat(
        map(
            lambda a: pd.read_csv(a, delimiter = ";"),
            download(url_list)
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
        ).strip() for c in cols if c.startswith('Valor ')
    }

    novo_nome = ChainMap(anomes, nome, valor)
    return desp[list(cols)].rename(
        columns = novo_nome
    ).pipe(
        lambda df: df.melt(
            id_vars = [c for c in df.columns if c not in set(valor.values())],
            value_name = 'valor',
            var_name   = 'modalidade'
        )
    )


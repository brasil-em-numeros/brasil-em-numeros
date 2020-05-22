import csv
import locale
import json
import re
from collections import OrderedDict
import pandas as pd
import functools
import operator


def parse_num(_str):

    # ------------------------------
    # Se houver vírgula, é um float
    # caso contrário é inteiro
    # ------------------------------

    dec_mark = locale.localeconv().get('decimal_point')

    if re.search(dec_mark, _str) is None:
        num_fun = locale.atoi
    else:
        num_fun = locale.atof

    try:
        val = num_fun(_str)
    except Exception:

        # ---------------------------
        # Se não conseguir converter,
        # retorna a string
        # ---------------------------

        val = _str

    return val


def parse_csv(csv_file):

    # --------------------------------------------------------------------------
    #                               Exemplo
    # csv_file = '/Users/Felipe/Downloads/201912_Despesas.csv'
    # http://www.portaltransparencia.gov.br/download-de-dados/despesas-execucao
    # --------------------------------------------------------------------------

    encoding = "ISO-8859-1"
    loc = locale.getlocale()
    try:
        
        locale.setlocale(locale.LC_ALL, "pt_BR")
        date_col = "Ano e mês do lançamento"
        with open(csv_file, "r", encoding = encoding) as f:
            rows = []
            for i, r in enumerate(csv.reader(f, delimiter = ";")):
                
                if i == 0:
                    header = r
                else:
                    r = OrderedDict(
                        (h, parse_num(val)) for h, val in zip(header, r)
                    )

                    ano_mes = r.get(date_col).split("/")
                    ano = parse_num(ano_mes[0])
                    mes = parse_num(ano_mes[1])
                    r["Ano"] = ano
                    r['Mês'] = mes
                    del r[date_col]
                    rows.append(r)
    
    finally:
        locale.setlocale(locale.LC_ALL, loc)

    return rows


def to_json(data):

    save = data.loc[
        data['Código Função'] == 10  # - Saúde
    ].head(20).reset_index(
        drop = True
    ).to_dict(orient = "index")

    with open("exemplo.json", "w", encoding = "utf-8") as f:
        json.dump(save, f, indent = 2, ensure_ascii = False)


def coleta_dados(dados, campos = None, filtros = None):

    with open(dados, "r", encoding = "utf-8") as f:
        dados = json.load(f)

    # -------------------------------
    #  Remover coisas desnecessárias
    # -------------------------------

    colunas_inuteis = filter(
        lambda c: re.search(r'^Código', c, re.I) is not None,
        dados.get("0").keys()
    )

    colunas_inuteis = set(colunas_inuteis)
    colunas_inuteis.update({
        'Modalidade da Despesa',
        'Nome Grupo de Despesa',
        'Nome Programa Governo'
    })

    if campos is not None:
        colunas_inuteis.update(set(campos))

    # ---------------------------------------
    #  Certas columnas serão sempre expostas
    # ---------------------------------------

    # Basicamente, toda as columas com valores numéricos e
    # com datas. Isso vai depender de arquivo para arquivo

    sempre_visiveis = {
        c for c in dados.get("0").keys() if re.search(r'^Valor', c, re.I) is not None
    }.union({
        'Ano', 'Mês'
    })

    usar = dict()
    for linha, colunas in dados.items():
        
        # ----------
        # Filtragem
        # ----------
    
        if filtros is not None:

            flt = [
                colunas.get(key) in val for key, val in filtros.items() if colunas.get(key) is not None
            ]
            
            if flt:
                if not functools.reduce(operator.or_, flt):
                    continue

        usar[linha] = dict()
        for coluna, valor in colunas.items():
            if coluna in (colunas_inuteis - sempre_visiveis):
                continue

            usar[linha][coluna] = valor

    return pd.DataFrame.from_dict(usar, orient = 'index')

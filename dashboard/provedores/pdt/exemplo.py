import data as dados

filtros = {
    'Nome Órgão Superior' : ['Ministério da Saúde', 'Ministério da Educação']
}

file = "exemplo.json" # "./dashboard/provedores/pdt/exemplo.json"
zzz = dados.coleta_dados(file, filtros = filtros)

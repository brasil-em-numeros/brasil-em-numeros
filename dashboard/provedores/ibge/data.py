import os
import io
import re
import numpy as np
import pandas as pd
import ftplib
import urllib
import tqdm
import datetime
import itertools


loc = os.path.abspath(
    os.path.dirname(__file__)
)


def area_nacional(year = None):

    url = "ftp://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/areas_territoriais/"
    file_name = 'AR_BR_RG_UF_MES_MIC_MUN'
    extension = "xls"

    if year is None:
        year = 2018

    file_name += "_" + str(year) + "." + extension
    url = urllib.parse.urlparse(url)
    file_path = os.path.join(url.path, str(year))

    ftp = ftplib.FTP(url.netloc)
    ftp.login()
    try:

        file_name = os.path.join(file_path, file_name)
        size = ftp.size(file_name)

        with io.BytesIO() as data:

            with tqdm.tqdm(
                total = size,
                unit  = 'B',
                unit_scale   = True,
                unit_divisor = 1024
            ) as progress:

                def download_chunk(data_):
                    progress.update(len(data_))
                    data.write(data_)

                ftp.retrbinary(
                    'RETR {}'.format(file_name),
                    download_chunk
                )

            spreadsheet = data.getvalue()

        mun_tbl = pd.read_excel(spreadsheet, sheet_name = 'AR_BR_MUN_2018')
        reg_tbl = pd.read_excel(spreadsheet, sheet_name = 'AR_BR_RG_2018')

    finally:
        ftp.close()

    return AreaNacional(mun_tbl, reg_tbl)


class AreaNacional(object):

    def __init__(self, munis, regions):
        self.munis = munis
        self.regions = regions

    @staticmethod
    def limpa(tbl):

        id_ = tbl.get('ID')
        if id_ is not None:
            tbl = tbl.where(~id_.isna()).dropna()
        else:
            return tbl

        # - Format columns

        int_cols = itertools.chain(
            ['ID'],
            filter(
                lambda x: re.search('^CD_', x, re.I), tbl.columns
            )
        )

        for c in int_cols:
            tbl[c] = tbl[c].astype("int64")

        tbl['ID'] -= 1
        tbl = tbl.set_index('ID')

        # ================
        #  Rename columns
        # ================

        mapping = {
            'CD_GCUF' : 'codigo_uf',
            'NM_UF'   : 'nome_uf',
            'NM_UF_SIGLA' : 'nome_uf_sigla',
            'CD_GCMUN' : 'codigo_mun',
            'NM_MUN_2018' : 'nome_mun',
            'AR_MUN_2018' : 'area',
            'CD_GCRG' : 'codigo_reg',
            'NM_RG' : 'nome_reg',
            'NM_RG_SIGLA' : 'nome_reg_sigla'
        }

        return tbl.rename(columns = mapping)

    def clean_data(self):

        self.munis = self.clean(self.munis)
        self.regions = self.clean(self.regions)

        # -------------------------
        # Add region code to munis
        # -------------------------

        col = 'codigo_reg'
        reg_code = self.munis.get(col)
        if reg_code is None:
            self.munis[col] = self.munis.get('codigo_uf').apply(
                lambda x: int(str(x)[0])
            )

    def states(self):

        self.clean_data()
        return pd.merge(
            self.munis[[
                'nome_uf', 'nome_uf_sigla', "codigo_reg"
            ]].drop_duplicates(),
            self.regions[["codigo_reg", "nome_reg", "nome_reg_sigla"]],
            how = 'left'
        )


def fake_data(periods = 5):

    periods = int(periods)
    if periods < 2:
        raise ValueError("Periods must be greater than 1")

    now = datetime.datetime.now()
    bgn = now + datetime.timedelta(days = -periods * 365)
    bgn = datetime.date(bgn.year, 1, 1)
    end = datetime.date(now.year, 12, 31)
    rng = pd.date_range(bgn, end, freq = "Y")

    # -----------
    # Get states
    # -----------

    states = pd.read_csv(
        os.path.join(loc, "..", "data", "static", "estados.csv")
    )

    yr = [r.date().year for r in rng]
    fake = pd.DataFrame(
        np.random.randint(1, 500, size = (len(states.index), len(yr))),
        index = states.index,
        columns = yr
    )

    fake = pd.merge(
        states, fake,
        how = 'left',
        left_index  = True,
        right_index = True
    ).melt(
        id_vars    = states.columns,
        var_name   = 'ano',
        value_name = 'valor'
    )

    return fake

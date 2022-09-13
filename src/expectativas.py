import pandas as pd
from bcb import Expectativas
from dotenv import dotenv_values

from connect_gsheets import export_dataset

ENV = dotenv_values('.env')

"""
https://www3.bcb.gov.br/expectativas2/#/consultaSeriesEstatisticas

Seleções:
Índices de preços | Anual | IPCA
Expec informadas últ 5 dias | Mediana
"""

em = Expectativas()
ep = em.get_endpoint('ExpectativasMercadoAnuais')


def extracao_expectativas(indicador):
    df = (
        ep.query()
        .filter(ep.Indicador == f'{indicador}')
        .filter(ep.Data >= '2021-01-01')
        .select(
            ep.Indicador,
            ep.Data,
            ep.DataReferencia,
            ep.Mediana,
            ep.numeroRespondentes,
            ep.baseCalculo,
        )
        .collect()
    )
    return df


if __name__ == '__main__':
    GSHEET_ID = ENV['GSHEET_ID']
    indicadores = ['IPCA', 'PIB Total', 'PIB Serviços']

    dfs = list()
    for indicador in indicadores:
        df_extracao = extracao_expectativas(indicador)
        dfs.append(df_extracao)

    df = pd.concat(dfs)
    export_dataset(GSHEET_ID, df)

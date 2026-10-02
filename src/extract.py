import pandas as pd


def df_extract_transacciones(data_trasacciones):
    df_transacciones = pd.read_csv(data_trasacciones, sep=',')
    return df_transacciones

def df_extract_clientes(data_clientes):
    df_clientes = pd.read_csv(data_clientes)
    return df_clientes
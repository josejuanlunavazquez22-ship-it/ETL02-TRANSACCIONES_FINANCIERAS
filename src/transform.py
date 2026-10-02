import pandas as pd
import numpy as np


def df_transform_transacciones(df_transacciones):
    #1. Filtrar por APPROVED
    df_transacciones = df_transacciones[df_transacciones['status'].astype(str).str.upper() == 'APPROVED']
 
    #2. Casteo de los datos
    df_transacciones["amount"] = pd.to_numeric(df_transacciones["amount"], errors="coerce")
    df_transacciones["tx_date"] = pd.to_datetime(df_transacciones["tx_date"], errors="coerce")

    #3. Filtrar montos
    df_transacciones = df_transacciones[
        (df_transacciones["amount"] > 0)
    ].copy()

    #4. Deduplicar por tx_id
    df_transacciones = df_transacciones.drop_duplicates(subset=["tx_id"])

    return df_transacciones

def df_transform_clientes(df_clientes):
    #1. Casteo de los datos
    df_clientes["signup_date"] = pd.to_datetime(df_clientes["signup_date"], errors="coerce")

    #2. Deduplicar los datos
    df_clientes = df_clientes.drop_duplicates(subset=["client_id"])

    return df_clientes

def df_transacciones_finales(df_transacciones, df_clientes):
    #1. Realiar un left join mediante el campo client_id
    df_final = pd.merge(
        df_transacciones,
        df_clientes,
        on="client_id",
        how="left"
    )

    #2. Realizar conversion a dolares
    df_final["monto_mxn"] = np.where(df_final["currency"].astype(str).str.upper() == 'USD', df_final["amount"] * 20, df_final["amount"]) 

    df_final["full_name"] = df_final["full_name"].fillna("UNKNOWN")

    #3. Renombrar las columnas
    df_final = df_final.rename(columns={
        "tx_id": "id_transaccion",
        "client_id": "id_cliente",
        "full_name": "nombre_cliente",
        "amount": "monto_original",
        "currency": "moneda",
        "tx_date": "fecha_transaccion"
    })

    #4. Ordenar las columnas
    df_final = df_final[[
        "id_transaccion",
        "id_cliente",
        "nombre_cliente",
        "monto_original",
        "moneda",
        "monto_mxn",
        "fecha_transaccion"
    ]].copy()

    return df_final
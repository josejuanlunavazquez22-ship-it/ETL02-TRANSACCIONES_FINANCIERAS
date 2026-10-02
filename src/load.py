import pandas as pd


def load_parquet(df_transacciones_final, path_parquet):
    df_transacciones_final.to_parquet(path_parquet, index=False)

def load_reporte_csv(df_transacciones, path_csv):
    df_transacciones_agrupado = df_transacciones.groupby(
        "nombre_cliente", as_index=False
    ).agg(
        total_mxn = ("monto_mxn", "sum") 
    )

    df_transacciones_agrupado.to_csv(path_csv, index=False)
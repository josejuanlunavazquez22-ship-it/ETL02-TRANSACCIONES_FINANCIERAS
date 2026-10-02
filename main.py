from src.extract import df_extract_clientes, df_extract_transacciones
from src.transform import df_transform_transacciones, df_transform_clientes, df_transacciones_finales
from src.load import load_parquet, load_reporte_csv
import os
import logging

# Configurar el formato y nivel de logging para que se vean los mensajes en consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)

path_data_transacciones = os.path.join("data", "raw", "transacciones.txt")
path_data_clientes = os.path.join("data", "raw", "clientes.csv")

path_load_parquet = os.path.join("data", "processed", "pago_consolidado.parquet")
path_load_csv = os.path.join("data", "processed", "reporte_monto_por_cliente.csv")

def main():
    logging.info("Inicio de Pipeline")

    logging.info("Procesos de extraccion")
    df_transacciones = df_extract_transacciones(path_data_transacciones)
    df_clientes = df_extract_clientes(path_data_clientes)


    logging.info("Proceso de transformacion")
    df_transf_transacciones = df_transform_transacciones(df_transacciones)
    df_transf_clientes = df_transform_clientes(df_clientes)

    df_final = df_transacciones_finales(df_transf_transacciones, df_transf_clientes)

    logging.info("Proceso de carga")
    load_parquet(df_final, path_load_parquet)
    load_reporte_csv(df_final, path_load_csv)

    logging.info("Pipeline finalizado")
if __name__ == "__main__":
    main()
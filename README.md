# 💳 ETL02-TRANSACCIONES_FINANCIERAS: Ingesta Financiera y Conversión de Monedas

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas)
![Format](https://img.shields.io/badge/Output-Parquet%20%7C%20CSV-green)

Pipeline ETL (Extract, Transform, Load) desarrollado en Python para procesar transacciones financieras internacionales en formato heterogéneo, enriquecer la información mediante un cruce con el catálogo de clientes y unificar los montos transaccionados a moneda local (**MXN**).
---

## 📌 Caso de Negocio

El equipo de finanzas y auditoría requiere consolidar los pagos internacionales realizados en **USD** y **MXN**, enriqueciendo las transacciones con el nombre del cliente registrado y calculando el **monto equivalente en MXN** utilizando una tasa de cambio fija ($1 \text{ USD} = 20.00 \text{ MXN}$). 

El pipeline limpia registros inválidos o declinados, remueve transacciones duplicadas y genera dos salidas analíticas:
1. **Dataset Unificado Columnar (`.parquet`):** Granularidad por transacción para consultas de alta velocidad.
2. **Reporte Consolidado (`.csv`):** Agregación del total pagado en MXN agrupado por cliente.

---

## 🛠️ Arquitectura y Flujo de Datos

```text
┌────────────────────────┐      ┌────────────────────────┐
│ data/raw/              │      │ data/raw/              │
│ transacciones.txt      │      │ clientes.csv           │
└───────────┬────────────┘      └───────────┬────────────┘
            │                               │
            └───────────────┬───────────────┘
                            ▼
                ┌───────────────────────┐
                │   src/extract.py      │
                │ (Lectura de Fuentes)  │
                └───────────┬───────────┘
                            ▼
                ┌───────────────────────┐
                │   src/transform.py    │
                │ - Filtrado APPROVED   │
                │ - Left Join Clientes  │
                │ - Conversión a MXN    │
                │ - Deduplicación       │
                └───────────┬───────────┘
                            ▼
                ┌───────────────────────┐
                │     src/load.py       │
                │ (Exportación Parquet  │
                │  y Reporte CSV)       │
                └───────────┬───────────┘
                            ▼
        ┌───────────────────────────────────────┐
        │ data/processed/                       │
        │ ├── pago_consolidado.parquet          │
        │ └── reporte_monto_por_cliente.csv     │
        └───────────────────────────────────────┘


⚙️ Reglas de Calidad y Transformación

Filtros de Calidad:
    - Exclusión de transacciones no aprobadas (status == 'APPROVED').
    - Eliminación de montos nulos o menores/iguales a cero (amount > 0).
    - Deduplicación por clave primaria de transacción (tx_id).

Enriquecimiento de Datos (Left Join):
    - Cruce entre transacciones y clientes mediante la llave client_id.
    - Imputación de valores faltantes en clientes no encontrados con 'UNKNOWN'.

Conversión Monetaria (Regla de Negocio):
    - Tasa de cambio fija: $1 \text{ USD} = 20.00 \text{ MXN}$.
    - Si currency == 'USD', se calcula monto_mxn = amount * 20.
    - Si currency == 'MXN', se preserva el monto original.

Estandarización de Esquema:
    - Selección y ordenamiento de columnas: id_transaccion, id_cliente, nombre_cliente, monto_original, moneda, monto_mxn, fecha_transaccion

📂 Estructura del Proyecto

ETL02-TRANSACCIONES_FINANCIERAS/
├── data/
│   ├── processed/
│   │   ├── pago_consolidado.parquet
│   │   └── reporte_monto_por_cliente.csv
│   └── raw/
│       ├── clientes.csv
│       └── transacciones.txt
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt

🚀 Guía de Ejecución
Prerrequisitos
Python 3.10 o superior.

1. Clonar el repositorio
git clone [https://github.com/josejuanlunavazquez22-ship-it/ETL02-TRANSACCIONES_FINANCIERAS)
cd ETL02-TRANSACCIONES_FINANCIERAS

2. Crear e inicializar el entorno virtual
# En Linux/macOS:
python3 -m venv env
source env/bin/activate

# En Windows:
python -m venv env
env\Scripts\activate

3. Instalar dependencias
pip install -r requirements.txt

4. Ejecutar el Pipeline
python main.py

📊 Resultados Generados

1. Dataset Procesado (data/processed/pago_consolidado.parquet)

id_transaccion	id_cliente	nombre_cliente	monto_original	moneda	monto_mxn	fecha_transaccion
TX-901	        CLI-10	    Carlos Mendoza	150	            USD	    3000	    20/09/2026
TX-902	        CLI-12	    Ana Gómez	    3500	        MXN	    3500	    20/09/2026
TX-904	        CLI-15	    John Smith	    1200	        USD	    24000	    21/09/2026
 

2. Reporte Consolidado por Cliente (data/processed/reporte_monto_por_cliente.csv)

nombre_cliente	total_mxn
Ana Gómez	    3500
Carlos Mendoza	3000
John Smith	    24000

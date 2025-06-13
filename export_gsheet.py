import pandas as pd
import sqlite3
import gspread
from gspread_dataframe import set_with_dataframe

# --- CONFIGURACIÓN ---
# Nombre del archivo JSON de tus credenciales
CREDENCIALES_JSON = 'credenciales.json' 
# Nombre EXACTO de tu hoja de cálculo en Google Sheets
NOMBRE_GOOGLE_SHEET = 'FIFA19_DataSet'

# --- 1. LEER DATOS DE LA BASE DE DATOS LOCAL ---
print("Leyendo datos desde 'dataset.db'...")
try:
    conn = sqlite3.connect('dataset.db')
    df = pd.read_sql_query("SELECT * FROM players", conn)
    conn.close()
    # Looker Studio maneja mejor los nulos que los 0 en algunos casos. 
    # Convertimos las fechas 0 a NaT (Not a Time) para que Sheets las deje en blanco.
    if 'Joined' in df.columns:
        df['Joined'] = pd.to_datetime(df['Joined'], errors='coerce')
    print("Datos leídos correctamente.")
except Exception as e:
    print(f"Error al leer la base de datos: {e}")
    exit()

# --- 2. CONECTARSE A GOOGLE SHEETS Y SUBIR LOS DATOS ---
try:
    print("Conectando con Google Sheets...")
    gc = gspread.service_account(filename=CREDENCIALES_JSON)
    spreadsheet = gc.open(NOMBRE_GOOGLE_SHEET)

    # Selecciona la primera hoja de trabajo
    worksheet = spreadsheet.get_worksheet(0)

    # Limpia la hoja antes de escribir nuevos datos
    worksheet.clear()

    print(f"Subiendo {len(df)} filas a la hoja de cálculo '{NOMBRE_GOOGLE_SHEET}'...")
    # Usa gspread-dataframe para subir el DataFrame completo
    set_with_dataframe(worksheet, df)

    print("\n¡Éxito! Los datos han sido subidos a Google Sheets.")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo de credenciales '{CREDENCIALES_JSON}'. Asegúrate de que el nombre sea correcto y esté en la misma carpeta.")
except Exception as e:
    print(f"Ocurrió un error al conectar o subir los datos: {e}")
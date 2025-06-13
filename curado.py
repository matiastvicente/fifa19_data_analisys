import pandas as pd
import sqlite3

# Se crea el dataframe
df = pd.read_csv('dataset.csv', encoding='cp1252') 

# Se eliminan las filas duplicadas si las hubiese (en esta base no hay)
initial_rows = len(df)
df.drop_duplicates(inplace=True)
final_rows = len(df)

# Se eliminan las filas con el nombre de jugador duplicado manteniuendo solo la primera encontrada
df.drop_duplicates(subset=['Name'], keep='first', inplace=True)
rows_removed = initial_rows - len(df)

initial_rows = len(df)
# Se usa ~ para negar la condición, manteniendo las filas que NO contienen '?'
df = df[~df['Name'].str.contains(r'\?', na=False)]
rows_removed = initial_rows - len(df)
# Se crea una máscara booleana para encontrar los clubes con '?'
mask_club = df['Club'].str.contains(r'\?', na=False)
clubs_replaced = mask_club.sum()
# Se usa .loc para asignar de forma segura el nuevo valor
df.loc[mask_club, 'Club'] = 'Unknown'

# Se agrupan las posiciones en roles para facilitar el punto 5 del analisis final
position_map = {
    'GK': 'Goalkeeper',
    'CB': 'Defender', 'LCB': 'Defender', 'RCB': 'Defender', 'LB': 'Defender', 'RB': 'Defender', 'LWB': 'Defender', 'RWB': 'Defender',
    'CM': 'Midfielder', 'LCM': 'Midfielder', 'RCM': 'Midfielder', 'CDM': 'Midfielder', 'LDM': 'Midfielder', 'RDM': 'Midfielder', 'CAM': 'Midfielder', 'LAM': 'Midfielder', 'RAM': 'Midfielder', 'LM': 'Midfielder', 'RM': 'Midfielder',
    'ST': 'Forward', 'LS': 'Forward', 'RS': 'Forward', 'CF': 'Forward', 'LF': 'Forward', 'RF': 'Forward', 'LW': 'Forward', 'RW': 'Forward'
}
if 'Position' in df.columns:
    df['Position_Group'] = df['Position'].replace(position_map)

# Se corrigen formatos de fecha y categorías
if 'Joined' in df.columns:
    df['Joined'] = pd.to_datetime(df['Joined'], errors='coerce')
for col in ['Club', 'Nationality', 'Position', 'Preferred Foot']:
    if col in df.columns:
        df[col] = df[col].fillna('Unknown')
        df[col] = df[col].astype('category')

# Se implementa la función convert_value_to_float para convertir valores como '€110.5M' o '€565K' a números
def convert_value_to_float(value):
    if isinstance(value, str):
        value = value.replace('€', '')
        if 'M' in value:
            value = float(value.replace('M', '')) * 1000000
        elif 'K' in value:
            value = float(value.replace('K', '')) * 1000
    return float(value)

# Se aplica la función a las columnas relevantes para el análisis
df['Value'] = df['Value'].apply(convert_value_to_float)
df['Wage'] = df['Wage'].apply(convert_value_to_float)
if 'Release Clause' in df.columns: 
    # Se llena la columna release clause con 0 para evitar posibles errores y se aplica la funcion
    df['Release Clause'] = df['Release Clause'].fillna('€0').apply(convert_value_to_float)


# Se llenan con 0 los valores numericos nulos.
numeric_cols = df.select_dtypes(include=['number']).columns
df[numeric_cols] = df[numeric_cols].fillna(0)

# Visualizacion rápida para corroborar efectivamente si los datos fueron reemplazados
print(df[['Name', 'Value', 'Wage', 'Joined', 'Release Clause', 'Preferred Foot']].head()) 

# Se crea la base de datos con los datos ya curados
conn = sqlite3.connect('dataset.db') 
df.to_sql('players', conn, if_exists='replace', index=False)
conn.close()
import pandas as pd
import sqlite3

# Se carga la base creada anteriormente
try:
    conn = sqlite3.connect('dataset.db')
    df = pd.read_sql_query("SELECT * FROM players", conn)
    conn.close()
except Exception as e:
    print(f"Error al conectar o leer la base de datos: {e}")
    # Sale del script si da error
    exit()

# Se crea un DataFrame vacío donde se almacenarán todos los outliers encontrados
all_outliers_df = pd.DataFrame()
 
# Columnas para analizar
columns_to_analyze = ['Wage', 'Value', 'Age', 'Overall', 'Potential']

# Bucle de analisis y recolección
for column in columns_to_analyze:
    print(f"\n=============================================\n")
    print(f"Análisis para la columna: '{column}'")
    
    if pd.api.types.is_numeric_dtype(df[column]):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        if column in ['Wage', 'Value']:
            multiplier = 15.0
        else:
            multiplier = 1.5
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        if column in ['Wage', 'Value']:
            lower_bound = max(0, lower_bound)
        elif column == 'Age':
            lower_bound = max(16, lower_bound)
        
        print(f"Estadísticas:")
        print(f"  - Primer Cuartil (Q1): {Q1:,.2f}")
        print(f"  - Tercer Cuartil (Q3):  {Q3:,.2f}")
        print(f"  - Multiplicador IQR utilizado: {multiplier}")

        outliers_df = df[(df[column] > upper_bound) | (df[column] < lower_bound)]
        print(f"  - Cantidad de Outliers encontrados: {len(outliers_df)}")

        # Se añaden los outliers de esta iteración al DataFrame general
        if not outliers_df.empty:
            all_outliers_df = pd.concat([all_outliers_df, outliers_df])
            
    else:
        print(f"La columna '{column}' no es numérica y no puede ser analizada.")


# Guardado de outliers unicos 
if not all_outliers_df.empty:
    print(f"\n=============================================\n")
    print(f"Total de menciones de outliers encontradas (con duplicados): {len(all_outliers_df)}")
    
    # Se eliminan los jugadores duplicados basándose en la columna 'ID'
    unique_outliers_df = all_outliers_df.drop_duplicates(subset=['ID'], keep='first')
    print(f"Total de jugadores outliers únicos: {len(unique_outliers_df)}")
    
    # Se guarda el DataFrame de outliers únicos en una nueva base de datos
    try:
        conn_outliers = sqlite3.connect('outliers.db')
        unique_outliers_df.to_sql('outlier_players', conn_outliers, if_exists='replace', index=False)
        conn_outliers.close()
        print("\nSe ha creado correctamente la base de datos 'outliers.db' con la tabla 'outlier_players'.\n")
    except Exception as e:
        print(f"Error al guardar la base de datos de outliers: {e}")
else:
    print("\nNo se encontraron outliers para guardar.")
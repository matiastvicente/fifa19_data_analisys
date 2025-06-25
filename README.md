# Análisis de Datos del Dataset FIFA 19

Este proyecto es un análisis completo del dataset "FIFA 19 Complete Player Dataset" de Kaggle. El proceso incluye una fase exhaustiva de limpieza y curado de datos con Python, y la creación de un tablero de visualización interactivo en Google Looker Studio para presentar los hallazgos clave.

## 🚀 Hallazgos y Visualizaciones

El análisis se centra en 5 puntos clave, explorados en un tablero interactivo:

* **Detección de Outliers:** Identificación de jugadores con características atípicas usando criterios estadísticos y de negocio.
* **Ranking de Jugadores:** Un ranking dinámico del Top 5 de jugadores por Salario, Valoración General y Potencial.
* **Comparativa de Clubes:** Análisis de las estrategias de los clubes a través de su gasto salarial y la edad promedio de sus plantillas.
* **Correlaciones Clave:** Un explorador interactivo para descubrir la relación entre diferentes atributos de los jugadores.
* **Perfil de Habilidades por Posición:** Un Gráfico de Radar que define el "ADN de habilidad" para cada rol en el campo.

### 🔗 Link al Tablero Interactivo
<a href="https://lookerstudio.google.com/reporting/057de687-782e-4ab6-b763-91ebf03a6698" target="_blank">**Puedes explorar el tablero completo aquí**</a>

### 🔗 Link a la Documentación
<a href="https://docs.google.com/document/d/1DxnqKScSOTILQCtX0PfI4uhmLk700QJBue2WQa4yT10/edit?tab=t.0" target="_blank">**Puedes explorar la documentación del proceso aquí**</a>


## 🛠️ Stack Tecnológico

* **Lenguaje:** Python
* **Librerías de Análisis:** Pandas
* **Base de Datos:** SQLite
* **Herramienta de BI:** Google Looker Studio
* **Puente de Datos:** Google Sheets

## ⚙️ Cómo Replicar el Proyecto

1.  Clona este repositorio.
2.  Asegúrate de tener el archivo `dataset.csv` en la carpeta raíz.
3.  Ejecuta el script `curado.py` para limpiar los datos y generar la base de datos `dataset.db`.
4.  (Opcional) Ejecuta los scripts de análisis (`outliers.py`, etc.) para ver los resultados en la consola.
5.  (Opcional) Para conectar a Looker Studio, sigue las instrucciones [aquí](#) para generar tus propias credenciales y sube los datos a tu Google Sheets.

---
**Autor:** Matías Tomás Vicente

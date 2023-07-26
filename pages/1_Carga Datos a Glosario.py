import pandas as pd
import streamlit as st
import mysql.connector

# Configura la página
st.set_page_config(
    page_title="Inicio",
    page_icon="🏡",
    layout='wide'
)

# Configurar la conexión a MySQL
# Reemplaza los valores con tus credenciales de MySQL
host = 'mm90.hosting-ar.com'
user = 'talbot_tradusr'
password = '3jV5tDTT'
database_name = 'talbot_tradprj'

# Función para insertar DataFrame en la tabla "glosario" de MySQL
def insert_dataframe_to_db(dataframe):
    try:
        # Conexión a MySQL
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )

        # Crear un cursor para ejecutar la consulta de inserción
        cursor = connection.cursor()

        # Iterar sobre cada fila del DataFrame y realizar la inserción en la tabla
        for _, row in dataframe.iterrows():
            tag = str(row['tag'])
            english = str(row['english'])
            spanish = str(row['spanish'])
            comment = str(row['comment'])

            # Ejecutar la consulta de inserción
            query = "INSERT INTO glosario (tag, english, spanish, comment) VALUES (%s, %s, %s, %s)"
            values = (tag, english, spanish, comment)
            cursor.execute(query, values)

        # Confirmar los cambios y cerrar el cursor y la conexión
        connection.commit()
        cursor.close()
        connection.close()

        st.success("Datos insertados correctamente en la tabla 'glosario'.")
    except Exception as e:
        st.write("Error al insertar datos en la base de datos:", e)

# Streamlit
st.title("Carga de datos en la tabla 'glosario' de MySQL")

# Widget para cargar el archivo Excel
file = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

if file:
    try:
        # Leer el archivo Excel en un DataFrame
        df_excel = pd.read_excel(file, engine='openpyxl')

        # Mostrar el DataFrame cargado en Streamlit
        st.write("Datos cargados desde el archivo Excel:")
        st.write(df_excel)

        # Botón para insertar el DataFrame en la tabla "glosario"
        if st.button("Insertar en la tabla 'glosario'"):
            insert_dataframe_to_db(df_excel)
    except Exception as e:
        st.write("Error al leer el archivo Excel:", e)

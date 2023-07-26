import pandas as pd
import streamlit as st
import pyodbc
import io

# Configura la página
st.set_page_config(
    page_title="Inicio",
    page_icon="🏡",
    layout='wide'
)

# Conexion Database
server = 'JTALBOT-NOTEBOO\SQLEXPRESS'
database = 'db'
connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Función para insertar DataFrame en la tabla "dbo.glosario" de la base de datos
def insert_dataframe_to_db(dataframe):
    try:
        # Conexión a la base de datos
        connection = pyodbc.connect(connection_string)

        # Crear un cursor para ejecutar la consulta de inserción
        cursor = connection.cursor()

        # Iterar sobre cada fila del DataFrame y realizar la inserción en la tabla
        for index, row in dataframe.iterrows():
            st.write(row['spanish'])
            if pd.isna(row['tag']):
                tag = ''
            else:
                tag = row['tag']
            
            if pd.isna(row['comment']):
                comment = ''
            else:
                comment = row['comment']

            if row['english'] != '' and row['spanish'] != '':
                cursor.execute(
                    "INSERT INTO dbo.glosario (tag, english, spanish, comment) VALUES (?, ?, ?, ?)",
                    tag, row['english'], row['spanish'], comment
                )

        # Confirmar los cambios y cerrar el cursor y la conexión
        connection.commit()
        cursor.close()
        connection.close()

        st.success("Datos insertados correctamente en la tabla 'dbo.glosario'.")
    except Exception as e:
        st.write("Error al insertar datos en la base de datos:", e)

# Streamlit
st.title("Carga de datos en la tabla 'dbo.glosario'")

# Widget para cargar el archivo Excel
uploaded_file = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Leer el archivo Excel en un DataFrame
        with io.BytesIO(uploaded_file.read()) as buffer:
            df_excel = pd.read_excel(buffer, engine='xlrd')

        # Mostrar el DataFrame cargado en Streamlit
        st.write("Datos cargados desde el archivo Excel:")
        st.write(df_excel)

        # Botón para insertar el DataFrame en la tabla "dbo.glosario"
        if st.button("Insertar en la tabla 'dbo.glosario'"):
            insert_dataframe_to_db(df_excel)
    except Exception as e:
        st.write("Error al leer el archivo Excel:", e)

st.write()


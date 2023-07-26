import pandas as pd
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Configura la página
st.set_page_config(
    page_title="Inicio",
    page_icon="🏡",
    layout='wide'
)

# Configurar la conexión a Firebase
# Configurar la conexión a Firebase
cred = credentials.Certificate("C:/Users/juani/OneDrive/Desktop/traductionProject/traductionproject-efb4b-default-rtdb-export.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://traductionproject-efb4b-default-rtdb.firebaseio.com/'
})


# Función para insertar DataFrame en la colección "glosario" de MongoDB
def insert_dataframe_to_db(dataframe):
    try:
        # Accede a la base de datos de Firebase
        ref = db.reference('/glosario')  # 'glosario' es el nombre de la colección

        # Inserta cada fila del DataFrame en la colección
        for _, row in dataframe.iterrows():
            data = {
                'tag': str(row['tag']),
                'english': str(row['english']),
                'spanish': str(row['spanish']),
                'comment': str(row['comment'])
            }
            ref.push(data)

        st.success("Datos insertados correctamente en la colección 'glosario'.")
    except Exception as e:
        st.write("Error al insertar datos en la base de datos:", e)


# Streamlit
st.title("Carga de datos en la colección 'glosario' de MongoDB")

# Widget para cargar el archivo Excel
file = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

if file:
    try:
        # Leer el archivo Excel en un DataFrame
        df_excel = pd.read_excel(file, engine='openpyxl')

        # Mostrar el DataFrame cargado en Streamlit
        st.write("Datos cargados desde el archivo Excel:")
        st.write(df_excel)

        # Botón para insertar el DataFrame en la colección "glosario"
        if st.button("Insertar en la colección 'glosario'"):
            insert_dataframe_to_db(df_excel)
    except Exception as e:
        st.write("Error al leer el archivo Excel:", e)

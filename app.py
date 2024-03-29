# Import required libraries
import PIL

import streamlit as st
from ultralytics import YOLO

# Replace the relative path to your weight file
model_path = 'weights/best.pt'

# Setting page layout
st.set_page_config(
    page_title="Calidad de Citricos",  # Setting page title
    #page_icon="🍋",     # Setting page icon
    layout="wide",      # Setting layout to wide
    initial_sidebar_state="expanded"    # Expanding sidebar by default
)

# Creating sidebar
with st.sidebar:
    st.header("Cargue su imagen")     # Adding header to sidebar
    # Adding file uploader to sidebar for selecting images
    source_img = st.file_uploader(
        "Seleccione una imagen...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    # Model Options
    confidence = 0.15
    #float(st.slider(
    #    "Nivel de confianza del modelo", 25, 100, 40)) / 100

# Creating main page heading
st.title("Control de Calidad - Lapacho Amarillo")

# Creating two columns on the main page
col1, col2 = st.columns(2)

# Adding image to the first column if image is uploaded
with col1:
    if source_img:
        # Opening the uploaded image
        uploaded_image = PIL.Image.open(source_img)
        # Adding the uploaded image to the page with a caption
        st.image(source_img,
                 caption="Imagen cargada",
                 use_column_width=True
                 )

try:
    model = YOLO(model_path)
except Exception as ex:
    st.error(
        f"No fue posible cargar la imagen. por favor revise el directorio: {model_path}")
    st.error(ex)

if st.sidebar.button('Detectar calidad de limon'):
    res = model.predict(uploaded_image,
                        #conf=confidence
                        )
    boxes = res[0].boxes
    res_plotted = res[0].plot()[:, :, ::-1]
    with col2:
        st.image(res_plotted,
                 caption='Imagen cargada',
                 use_column_width=True
                 )
        try:
            with st.expander("Resultados de deteccion"):
                for box in boxes:
                    st.write(box.xywh)
        except Exception as ex:
            st.write("Ninguna imagen fue cargada")

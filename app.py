import streamlit as st
from spider_testing2 import *
from downloader import FileDownloader
import streamlit.components as select_slider
import pandas
import base64
import time
from io import BytesIO
from st_on_hover_tabs import on_hover_tabs
import re
import asyncio


def scrapping_data(dataframe):
    spider = AsyncSpiderFunctions()
   
    return asyncio.run(spider.httpx_http(dataframe))






st.set_page_config(layout="wide")
def main():
    # values = ["Scrapping","About"]
    # st.sidebar.selectbox("Valores",values)
    st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

    st.markdown("""
                    <style>
                    .loading-container {
                        display: flex;
                        align-items: center;
                        margin-top: 20px;
                        justify-content: center;
                    }
                    .loading-container span {
                        font-size: 16px;
                        color: #333;
                        margin-right: 10px;
                    }
                    .loading {
                        width: 30px;
                        height: 30px;
                        border: 5px solid #f3f3f3;
                        border-top: 5px solid #3498db;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                    }
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    </style>
                """, unsafe_allow_html=True)

    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Scrapping',"About"],
                            iconName=['dashboard', 'search'], default_choice=0,
                            styles = {'navtab': {'background-color':'#111',
                                                  'color': '#818181',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                       'tabStyle': {':hover :hover': {'color': 'red',
                                                                      'cursor': 'pointer'}},
                                       'tabStyle' : {'list-style-type': 'none',
                                                     'margin-bottom': '30px',
                                                     'padding-left': '30px'},
                                       'iconStyle':{'position':'fixed',
                                                    'left':'7.5px',
                                                    'text-align': 'left'},
                                       },
                             key="1")

    if tabs == "Scrapping":

    
        st.title("Web scrapping de administradores de fincas")
        dataframe_value = st.file_uploader("Suba el archivo para extraer los datos")
        with st.form(key="scrapping"):
            st.markdown("**Pulse el botón para scrappear :)**")
        
            value = st.form_submit_button("Submit request")
        if value:
            if dataframe_value:

                loading_placeholder = st.empty()

                loading_placeholder.markdown("""
                    <div class="loading-container" id="loading-container">
                        <span>Extrayendo datos de administradores de fincas. Por favor espere...</span>
                        <div class="loading"></div>
                    </div>
                """, unsafe_allow_html=True)
            
            # pass
            
            df = scrapping_data(dataframe_value)
            st.success("Datos extraidos con exito !")
            loading_placeholder.empty()
            # st.markdown("""
            #     <script>
            #     document.getElementById("loading-container").style.display = "none";
            #     </script>
            # """, unsafe_allow_html=True)
            st.dataframe(df)
            tab1,tab2,tab3 = st.tabs(["CSV","Excel","JSON"])

            with tab1:
                download = FileDownloader(df.to_csv(), file_ext=".csv").download()

            with tab2:
                towrite = BytesIO()
                df.to_excel(towrite, index=False, engine='openpyxl')
                towrite.seek(0)
                download = FileDownloader(towrite.read(), file_ext="xlsx").download_xlsx()

            with tab3:
                json_data = df.to_json(orient='records')
                download = FileDownloader(json_data, file_ext="json").download_json()

    else:
        st.title("Sobra la app web")
        st.markdown("#### En esta app web extraemos los datos de páginas web mediante la busqueda")
        st.markdown("#### Suba el archivo y presione click para obtener los resultados")
        st.markdown("*Tendremos la opción de descargar el archivo en tres diferentes tipos de archivos: excel, csv o json*")

if __name__=="__main__":
    main()
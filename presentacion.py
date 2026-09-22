import streamlit as st
import pandas as pd
import numpy as np
import pycountry
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import statsmodels.formula.api as smf
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="El pastel que no se reparte")
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 25px;
        }
        .stTabs [data-baseweb="tab"] p {
            font-size: 25px;
        }
    </style>
""", unsafe_allow_html=True)

if "seccion" not in st.session_state:
    st.session_state.seccion = 0

def mostrar_indicador_parte(numero, nombre, color="#E8873A"):
    st.markdown(f"""
    <div style="background-color: {color}; color: white; padding: 8px 18px; 
                border-radius: 6px; font-size: 15px; font-weight: 600; 
                display: inline-block; margin-top: 10px; margin-bottom: 15px; 
                margin-left: 0;">
        Parte {numero} de 3 · {nombre}
    </div>
    """, unsafe_allow_html=True)

def mostrar_tabla_sql(nombre, columnas, color_borde="#1f77b4", color_fondo="#eaf2fb"):
    filas_html = ""
    for col, es_pk in columnas:
        prefijo = "🔑 " if es_pk else ""
        filas_html += f"<div style='padding: 2px 0; font-size: 12px;'>{prefijo}{col}</div>"
    st.markdown(f"""
    <div style="background-color: {color_fondo}; border: 1px solid {color_borde}; border-radius: 4px; margin-bottom: 10px;">
        <div style="background-color: {color_borde}; color: white; padding: 6px 8px; border-radius: 3px 3px 0 0; font-weight: bold; font-size: 13px;">{nombre}</div>
        <div style="padding: 7px 9px;">{filas_html}</div>
    </div>
    """, unsafe_allow_html=True)

def mostrar_portada():
    col_img, col_texto = st.columns([1.3, 2])

    with col_img:
        st.image("imgdesigualdad.jpg", width=650)
        st.markdown("<p style='font-size: 12px; color: #999; margin-top: -10px;'>Collage digital. Fuente: Instituto Tricontinental de Investigación Social (2022), basado en archivos de Wikimedia Commons,<br>la Biblioteca Británica y el documental <i>Las fuerzas de la desigualdad</i> (2021).</p>", unsafe_allow_html=True)

    with col_texto:
        st.markdown("""
        <div style="height: 500px; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; text-align: right;">
            <h1 style="font-size: 76px; font-weight: 800; margin-bottom: 20px;">El pastel que no se reparte</h1>
            <div style="width: 80px; height: 5px; background-color: #d62728; margin-bottom: 20px;"></div>
            <p style="font-size: 34px; color: #222;">Un retrato de la desigualdad, 1980-2024</p>
        </div>
        <div style="text-align: right; padding-right: 20px; margin-top: 120px;">
            <p style="font-style: italic; color: #222; font-size: 28px; margin-bottom: 4px;">Francesca Pani</p>
            <p style="color: #222; font-size: 18px;">Proyecto final · Itinerario Data Analytics · IT Academy · Barcelona Activa</p>
        </div>
        """, unsafe_allow_html=True)

def mostrar_gracias():
    st.markdown("""
    <div style="height: 500px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
        <h1 style="font-size: 76px; font-weight: 800; margin-bottom: 20px;">¡Muchas gracias!</h1>
        <div style="width: 80px; height: 5px; background-color: #d62728;"></div>
    </div>
    """, unsafe_allow_html=True)

def mostrar_mapa():
    st.header("Introducción")

    tab1, tab3, tab2 = st.tabs(["Mapa de la presentación", "Fuentes, flujo y herramientas", "Glosario"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="position: relative; background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">PARTE 1 DE 3</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">El contexto</p>
            <p style="font-size: 18px; color: #444; margin: 0;">¿Cómo ha evolucionado la desigualdad en el tiempo (Gini) y cómo se reparten riqueza e ingreso hoy?</p>
            <svg viewBox="0 0 60 60" width="90" height="90" style="position: absolute; right: 70px; top: 50%; transform: translateY(-50%);">
                <line x1="14" y1="46" x2="14" y2="30" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round"/>
                <line x1="26" y1="46" x2="26" y2="18" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round"/>
                <line x1="38" y1="46" x2="38" y2="34" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round"/>
                <line x1="50" y1="46" x2="50" y2="12" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
        </div>
        <div style="position: relative; background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">PARTE 2 DE 3</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">La pregunta</p>
            <p style="font-size: 18px; color: #444; margin: 0;">¿Cómo hemos llegado a una situación en la que tan pocas manos controlan una porción tan grande de la riqueza mundial?</p>
            <svg viewBox="0 0 60 60" width="90" height="90" style="position: absolute; right: 70px; top: 50%; transform: translateY(-50%);">
                <circle cx="14" cy="30" r="4" fill="none" stroke="#D4AF37" stroke-width="2"/>
                <circle cx="46" cy="30" r="4" fill="none" stroke="#D4AF37" stroke-width="2"/>
                <line x1="19" y1="30" x2="41" y2="30" stroke="#D4AF37" stroke-width="2" stroke-dasharray="4 3"/>
                <text x="30" y="20" text-anchor="middle" font-size="14" fill="#D4AF37">?</text>
            </svg>
        </div>
        <div style="position: relative; background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">PARTE 3 DE 3</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Las conclusiones</p>
            <p style="font-size: 18px; color: #444; margin: 0;">¿Podemos afirmar que la teoría se confirma? ¿Qué limitaciones tiene el análisis?</p>
            <svg viewBox="0 0 60 60" width="90" height="90" style="position: absolute; right: 70px; top: 50%; transform: translateY(-50%);">
                <path d="M 30 12 A 18 18 0 1 1 13 24" fill="none" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("""
            <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
                <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Gini</p>
                <p style="font-size: 18px; color: #444; margin: 0;">El índice (o coeficiente) de Gini mide qué tan repartida está la riqueza o el ingreso en una sociedad: 0 significa igualdad total y 1 significa desigualdad máxima.</p>
            </div>
            <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
                <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Riqueza VS Ingreso</p>
                <p style="font-size: 18px; color: #444; margin: 0;">La riqueza es un stock: una foto de todo lo que se tiene acumulado en un momento dado. Los ingresos son un flujo: lo que se gana por período.</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
                <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Riqueza</p>
                <p style="font-size: 18px; color: #444; margin: 0;">Es la riqueza neta: todos los activos financieros y no financieros que poseen los hogares, menos sus deudas. No financieros: vivienda, otras propiedades, etc. Financieros: ahorros, acciones, fondos, etc</p>
            </div>
            <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
                <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Capital VS Trabajo</p>
                <p style="font-size: 18px; color: #444; margin: 0;">El dinero que genera una economía se reparte entre dos bolsillos: el capital (beneficios) y el trabajo (sueldos).</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; gap: 60px;">
            <svg viewBox="0 0 60 60" width="90" height="90">
                <path d="M10 45 A20 20 0 0 1 50 45" fill="none" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round"/>
                <line x1="30" y1="45" x2="42" y2="28" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round"/>
                <circle cx="30" cy="45" r="2.5" fill="#D4AF37"/>
            </svg>
            <svg viewBox="0 0 60 60" width="90" height="90">
                <rect x="14" y="36" width="32" height="8" rx="1" fill="none" stroke="#D4AF37" stroke-width="2"/>
                <rect x="18" y="26" width="24" height="8" rx="1" fill="none" stroke="#D4AF37" stroke-width="2"/>
                <rect x="22" y="16" width="16" height="8" rx="1" fill="none" stroke="#D4AF37" stroke-width="2"/>
            </svg>
            <svg viewBox="0 0 60 60" width="90" height="90">
                <rect x="12" y="20" width="16" height="20" fill="#D4AF37"/>
                <path d="M36 24 Q44 24 44 30 Q44 36 52 36" fill="none" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round"/>
                <path d="M48 32 L52 36 L48 40" fill="none" stroke="#D4AF37" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg viewBox="0 0 60 60" width="90" height="90">
                <rect x="20" y="20" width="20" height="20" fill="#D4AF37" transform="rotate(45 30 30)"/>
                <circle cx="30" cy="46" r="7" fill="none" stroke="#D4AF37" stroke-width="2"/>
                <line x1="24" y1="46" x2="21" y2="46" stroke="#D4AF37" stroke-width="2"/>
                <line x1="39" y1="46" x2="36" y2="46" stroke="#D4AF37" stroke-width="2"/>
                <line x1="30" y1="37" x2="30" y2="40" stroke="#D4AF37" stroke-width="2"/>
                <line x1="30" y1="53" x2="30" y2="56" stroke="#D4AF37" stroke-width="2"/>
            </svg>
            <svg viewBox="0 0 60 60" width="90" height="90">
                <rect x="6" y="26" width="9" height="9" fill="#D4AF37" opacity="0.3"/>
                <rect x="17" y="26" width="9" height="9" fill="#D4AF37"/>
                <rect x="28" y="26" width="9" height="9" fill="#D4AF37"/>
                <rect x="39" y="26" width="9" height="9" fill="#D4AF37"/>
                <rect x="50" y="26" width="9" height="9" fill="#D4AF37" opacity="0.3"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        col_fuentes, col_flujo, col_herramientas = st.columns([1, 3, 1])

        with col_fuentes:
            st.markdown("<p style='font-size: 25px; font-weight: bold;'>Fuentes:</p>", unsafe_allow_html=True)
            st.markdown("- WID.world")
            st.markdown("- World Inequality Report 2026")
            st.markdown("- Our World in Data")

        with col_flujo:
            st.markdown("<p style='font-size: 22px; font-weight: bold; text-align: center;'>Flujo:</p>", unsafe_allow_html=True)
            st.markdown("""
            <div style="display: flex; align-items: stretch; justify-content: center;">
                <div style="background-color: #fffbeb; clip-path: polygon(0 0, 85% 0, 100% 50%, 85% 100%, 0 100%); padding: 30px 40px 30px 20px; width: 200px; display: flex; align-items: center;">
                    <p style="font-weight: bold; margin: 0;">EXTRACCIÓN</p>
                </div>
                <div style="background-color: #eaf2fb; clip-path: polygon(0 0, 85% 0, 100% 50%, 85% 100%, 0 100%); margin-left: -20px; padding: 30px 40px 30px 40px; width: 200px; display: flex; align-items: center;">
                    <p style="font-weight: bold; margin: 0;">LIMPIEZA</p>
                </div>
                <div style="background-color: #fffbeb; clip-path: polygon(0 0, 85% 0, 100% 50%, 85% 100%, 0 100%); margin-left: -20px; padding: 30px 40px 30px 40px; width: 200px; display: flex; align-items: center;">
                    <p style="font-weight: bold; margin: 0;">ANÁLISIS DESCRIPTIVO</p>
                </div>
                <div style="background-color: #eaf2fb; clip-path: polygon(0 0, 85% 0, 100% 50%, 85% 100%, 0 100%); margin-left: -20px; padding: 30px 40px 30px 40px; width: 200px; display: flex; align-items: center;">
                    <p style="font-weight: bold; margin: 0;">ANÁLISIS INFERENCIAL</p>
                </div>
                <div style="background-color: #fffbeb; clip-path: polygon(0 0, 85% 0, 100% 50%, 85% 100%, 0 100%); margin-left: -20px; padding: 30px 40px 30px 40px; width: 200px; display: flex; align-items: center;">
                    <p style="font-weight: bold; margin: 0;">CONCLUSIONES</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_herramientas:
            st.markdown("<p style='font-size: 25px; font-weight: bold;'>Herramientas:</p>", unsafe_allow_html=True)
            herramientas = [
                ("Python", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"),
                ("Pandas", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg"),
                ("NumPy", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg"),
                ("Plotly", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/plotly/plotly-original.svg"),
            ]
            for nombre, url in herramientas:
                col_icono, col_texto = st.columns([1, 3])
                with col_icono:
                    st.image(url, width=30)
                with col_texto:
                    st.markdown(f"<p style='margin-top: 5px;'>{nombre}</p>", unsafe_allow_html=True)

        st.markdown("<p style='font-size: 22px; font-weight: bold; margin-top: 30px; text-align: center;'>Tablas:</p>", unsafe_allow_html=True)

        fila = st.columns(6)
        tablas_datos = [
            ("df_gini", [("Entity", True), ("Code", False), ("Year", True), ("Gini coefficient", False)]),
            ("df_riqueza", [("Country", True), ("Variable", False), ("Percentile", True), ("Year", True), ("Value", False), ("Data quality", False)]),
            ("df_ingreso", [("Country", True), ("Variable", False), ("Percentile", True), ("Year", True), ("Value", False), ("Data quality", False)]),
            ("capital_share_por_region", [("year", True), ("World", False), ("Europe", False), ("Middle East & North Africa", False), ("Latin America", False), ("Sub-Saharan Africa", False), ("East Asia", False), ("South & Southeast Asia", False), ("North America & Oceania", False), ("Russia & Central Asia", False)]),
            ("labor_share_por_region", [("year", True), ("World", False), ("Europe", False), ("Middle East & North Africa", False), ("Latin America", False), ("Sub-Saharan Africa", False), ("East Asia", False), ("South & Southeast Asia", False), ("North America & Oceania", False), ("Russia & Central Asia", False)]),
            ("df_riqueza_regiones", [("Country", True), ("Variable", False), ("Percentile", True), ("Year", True), ("Value", False), ("Data quality", False)]),
        ]
        for i, (nombre, cols) in enumerate(tablas_datos):
            with fila[i]:
                mostrar_tabla_sql(nombre, cols)
@st.cache_data
def mostrar_gini():
    mostrar_indicador_parte(1, "El contexto")
    st.header("Evolución del Gini de ingreso por región (1980-2024)")

    df_gini = pd.read_csv("gini-coefficient-before-tax-wid.csv")

    regiones = df_gini[df_gini['Entity'].str.contains('WID', na=False)].copy()
    regiones = regiones[regiones['Year'] >= 1980]
    regiones['Entity'] = regiones['Entity'].str.replace(' (WID)', '', regex=False)

    colores = {
        'Europe': '#1f3b73',
        'Middle East and North Africa': '#d62728',
        'Latin America': '#2ca02c',
        'Sub-Saharan Africa': '#bcbd22',
        'East Asia': '#17becf',
        'South and South-East Asia': '#7f7f7f',
        'North America': '#6a0dad',
        'Oceania': '#ff7f0e',
        'Russia and Central Asia': '#e83e8c',
    }

    orden_1980 = regiones[regiones['Year'] == 1980].sort_values('Gini coefficient (before tax)', ascending=False)['Entity'].tolist()

    fig = px.bar(
        regiones.sort_values('Year'),
        x='Gini coefficient (before tax)',
        y='Entity',
        color='Entity',
        color_discrete_map=colores,
        animation_frame='Year',
        range_x=[0, 0.8],
        category_orders={'Entity': orden_1980}
    )
    fig.update_layout(
        xaxis_title='Gini',
        yaxis_title=None,
        showlegend=False
    )
    fig.update_yaxes(tickfont=dict(size=16, color='#444444'))
    fig.update_xaxes(tickfont=dict(size=16, color='#444444'))
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 100
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 50
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<style>.stAlert p { font-size: 19px !important; }</style>", unsafe_allow_html=True)
    st.info("Aquí es posible identificar tres patrones: unas regiones, como Europa, se mantienen estables. Otras convergen hacia un punto parecido al final. Y una, Rusia, tiene un salto brutal en los '90.")

    st.markdown("<br><br>", unsafe_allow_html=True)

def mostrar_distribucion_dolares():
    df_riqueza = pd.read_csv("wid_riqueza_1950_2025.csv", sep=';', skiprows=1)
    df_riqueza.columns = [c.strip() for c in df_riqueza.columns]
    df_riqueza['Variable_corta'] = df_riqueza['Variable'].str.split('\n').str[0].str.strip()
    tabla_limpia_riqueza = df_riqueza.pivot_table(index='Year', columns=['Variable_corta', 'Percentile'], values='Value')
    tabla_limpia_riqueza.columns = ['riqueza_promedio_adulto', 'pct50_mas_pobre', 'pct10_mas_rico', 'pct1_mas_rico', 'ratio_riqueza_ingreso']

    riqueza_promedio_adulto = tabla_limpia_riqueza['riqueza_promedio_adulto']
    cuotas_por_grupo = tabla_limpia_riqueza[['pct1_mas_rico', 'pct10_mas_rico', 'pct50_mas_pobre']]

    riqueza_por_persona_top1 = cuotas_por_grupo['pct1_mas_rico'] * riqueza_promedio_adulto / 0.01
    riqueza_por_persona_top10 = cuotas_por_grupo['pct10_mas_rico'] * riqueza_promedio_adulto / 0.10
    riqueza_por_persona_bottom50 = cuotas_por_grupo['pct50_mas_pobre'] * riqueza_promedio_adulto / 0.50

    st.header("La distribución de la riqueza, en dólares por persona")
    st.markdown("<p style='font-size: 26px; font-weight: 600;'>Riqueza media por persona en cada grupo, 1980 VS 2024</p>", unsafe_allow_html=True)
    grupos = ['Bottom 50%', 'Top 10%', 'Top 1%']
    colores = ['#1f77b4', '#ff7f0e', '#d62728']

    fig = go.Figure()
    for grupo, color, valor_1980, valor_2024 in zip(
        grupos, colores,
        [riqueza_por_persona_bottom50.loc[1980], riqueza_por_persona_top10.loc[1980], riqueza_por_persona_top1.loc[1980]],
        [riqueza_por_persona_bottom50.loc[2024], riqueza_por_persona_top10.loc[2024], riqueza_por_persona_top1.loc[2024]]
    ):
        fig.add_trace(go.Bar(
            x=['1980', '2024'], y=[valor_1980, valor_2024], name=grupo, marker_color=color,
            text=[f'${valor_1980:,.0f}', f'${valor_2024:,.0f}'], textposition='outside',
            textfont=dict(size=18, color='#444444')
        ))

    fig.update_layout(
        xaxis=dict(title=dict(text='Año', font=dict(size=18))),
        yaxis=dict(title=dict(text='Riqueza por persona (USD, escala log)', font=dict(size=18)), type='log', automargin=True),
        barmode='group', height=400, margin=dict(l=100, b=80, t=40)
    )
    fig.update_xaxes(tickfont=dict(size=16, color='#444444'))
    fig.update_yaxes(tickfont=dict(size=16, color='#444444'))
    st.plotly_chart(fig, use_container_width=True)

    col_box1, col_box2 = st.columns(2)
    with col_box1:
        st.markdown("""
        <div style="background-color: #eaf2fb; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; font-size: 19px; color: #1f77b4;">
        El Top 1% aumentó su riqueza media <b>640 veces</b> más que el Bottom 50%, <b>entre 1980 y 2024</b>.
        </div>
        """, unsafe_allow_html=True)
    with col_box2:
        st.markdown("""
        <div style="background-color: #eaf2fb; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; font-size: 19px; color: #1f77b4;">
        En <b>2024</b>, una persona del Top 1% tiene, de media, <b>809.78 veces</b> más riqueza que una del Bottom 50%.
        </div>
        """, unsafe_allow_html=True)
def mostrar_fotografia():
    st.header("Fotografía actual: ingreso VS riqueza (2024)")

    df_ingreso = pd.read_csv("WID_Data_06082026-141303.csv", sep=';', skiprows=1)
    df_ingreso.columns = [c.strip() for c in df_ingreso.columns]
    ingreso_mundo = df_ingreso[(df_ingreso['Country'].str.strip() == 'World (PPP)') & (df_ingreso['Year'] == 2024)]
    ingreso_por_percentil = ingreso_mundo.set_index('Percentile')['Value'] * 100

    df_riqueza = pd.read_csv("wid_riqueza_1950_2025.csv", sep=';', skiprows=1)
    df_riqueza.columns = [c.strip() for c in df_riqueza.columns]
    df_riqueza['Variable_corta'] = df_riqueza['Variable'].str.split('\n').str[0].str.strip()
    tabla_limpia_riqueza = df_riqueza.pivot_table(index='Year', columns=['Variable_corta', 'Percentile'], values='Value')
    tabla_limpia_riqueza.columns = ['riqueza_promedio_adulto', 'pct50_mas_pobre', 'pct10_mas_rico', 'pct1_mas_rico', 'ratio_riqueza_ingreso']
    riqueza_2024 = tabla_limpia_riqueza.loc[2024] * 100
    riqueza_middle40_2024 = 100 - riqueza_2024['pct10_mas_rico'] - riqueza_2024['pct50_mas_pobre']

    col_izq, col_der = st.columns(2)
    st.markdown("<style>.stAlert p { font-size: 19px !important; }</style>", unsafe_allow_html=True)

    with col_izq:
        st.markdown("<p style='font-size: 26px; font-weight: 600;'>Extremos: 50% más pobre | 10% más rico | 1% más rico</p>", unsafe_allow_html=True)
        comparacion_3 = pd.DataFrame({
            'Ingreso': [ingreso_por_percentil['p0p50'], ingreso_por_percentil['p90p100'], ingreso_por_percentil['p99p100']],
            'Riqueza': [riqueza_2024['pct50_mas_pobre'], riqueza_2024['pct10_mas_rico'], riqueza_2024['pct1_mas_rico']]
        }, index=['50% Inferior', 'Top 10%', 'Top 1%'])

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=comparacion_3.index, y=comparacion_3['Ingreso'], name='Ingreso',
            marker_color='#17becf', text=comparacion_3['Ingreso'].apply(lambda x: f'{x:.1f}%'), textposition='outside',
            textfont=dict(size=18, color='#444444')
        ))
        fig1.add_trace(go.Bar(
            x=comparacion_3.index, y=comparacion_3['Riqueza'], name='Riqueza',
            marker_color='#d62728', text=comparacion_3['Riqueza'].apply(lambda x: f'{x:.1f}%'), textposition='outside',
            textfont=dict(size=18, color='#444444')
        ))
        fig1.update_layout(barmode='group', height=450, yaxis=dict(title='%'))
        fig1.update_xaxes(tickfont=dict(size=18, color='#444444'))
        fig1.update_yaxes(tickfont=dict(size=16, color='#444444'))
        st.plotly_chart(fig1, use_container_width=True)
        st.info("IMPORTANTE: El Top 1% está incluido dentro del Top 10% - no son grupos independientes que se suman.")

    with col_der:
        st.markdown("<p style='font-size: 26px; font-weight: 600;'>Pastel completo: 50% más pobre | 40% Middle Class | 10% más rico</p>", unsafe_allow_html=True)
        comparacion_4 = pd.DataFrame({
            'Ingreso': [ingreso_por_percentil['p0p50'], ingreso_por_percentil['p50p90'], ingreso_por_percentil['p90p100']],
            'Riqueza': [riqueza_2024['pct50_mas_pobre'], riqueza_middle40_2024, riqueza_2024['pct10_mas_rico']]
        }, index=['50% Inferior', 'Middle 40%', 'Top 10%'])

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=comparacion_4.index, y=comparacion_4['Ingreso'], name='Ingreso',
            marker_color='#17becf', text=comparacion_4['Ingreso'].apply(lambda x: f'{x:.1f}%'), textposition='outside',
            textfont=dict(size=18, color='#444444')
        ))
        fig2.add_trace(go.Bar(
            x=comparacion_4.index, y=comparacion_4['Riqueza'], name='Riqueza',
            marker_color='#d62728', text=comparacion_4['Riqueza'].apply(lambda x: f'{x:.1f}%'), textposition='outside',
            textfont=dict(size=18, color='#444444')
        ))
        fig2.update_layout(barmode='group', height=450, yaxis=dict(title='%'))
        fig2.update_xaxes(tickfont=dict(size=18, color='#444444'))
        fig2.update_yaxes(tickfont=dict(size=16, color='#444444'))
        st.plotly_chart(fig2, use_container_width=True)
        st.info("Aquí sí están las 3 partes que suman el 100% de la población: 50% Inferior + Middle 40% + Top 10%.")

def mostrar_intro_piketty():
    col_texto, col_img = st.columns([2, 1.3])

    with col_texto:
        st.markdown("""
        <div style="height: 700px; display: flex; flex-direction: column; justify-content: flex-end; align-items: center;">
            <div style="max-width: 480px; text-align: left;">
                <p style="font-style: italic; color: #222; font-size: 34px; margin-bottom: 20px;">"El capitalismo sin regulación produce una concentración de la riqueza incontrolada que amenaza los valores meritocráticos y democráticos en los que se basan nuestras sociedades".</p>
                <div style="width: 80px; height: 5px; background-color: #d62728; margin-bottom: 20px;"></div>
                <p style="font-style: italic; color: #222; font-size: 22px; margin-bottom: 4px;">Thomas Piketty</p>
                <p style="color: #222; font-size: 16px;">El capital en el siglo XXI (2013)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_img:
        st.image("desigualdad2.jpg", width=550)

def mostrar_ratio():
    mostrar_indicador_parte(2, "La pregunta")
    st.header("El marco teórico de Thomas Piketty: el ratio riqueza/ingreso")

    tab_teoria, tab_grafico = st.tabs(["Teoría", "Gráfico"])

    with tab_teoria:
        st.markdown("""
        <div style="background-color: #fffbeb; border-left: 4px solid #D4AF37; padding: 25px; border-radius: 5px;">
            <p style="font-size: 26px; font-weight: bold; margin-bottom: 15px;">β = s/g</p>
            <p style="font-size: 18px; margin-bottom: 15px;">El ratio (riqueza/ingreso) es literalmente uno de los conceptos centrales de su libro <i>El capital en el siglo XXI</i> - lo llama β (beta), y es la pieza central de su "segunda ley fundamental del capitalismo".</p>
            <br>
            <p style="font-size: 18px; font-weight: bold; margin-bottom: 5px;">Qué significa la fórmula β = s/g:</p>
            <ul style="font-size: 18px; margin-bottom: 15px;">
                <li>β = el ratio riqueza/ingreso.</li>
                <li>s = tasa de ahorro (cuánto ahorra una economía de lo que gana).</li>
                <li>g = tasa de crecimiento económico (cuánto crece la economía cada año).</li>
            <br>
            </ul>
            <p style="font-size: 18px; margin-bottom: 15px;">Si dividimos cuánto se ahorra entre cuánto crece la economía, obtenemos hacia qué ratio tiende esa economía a largo plazo. Cuanto más se ahorra y menos crece la economía, más rápido se acumula riqueza en relación al ingreso que la economía genera cada año.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab_grafico:
        df_riqueza = pd.read_csv("wid_riqueza_1950_2025.csv", sep=';', skiprows=1)
        df_riqueza.columns = [c.strip() for c in df_riqueza.columns]
        df_riqueza['Variable_corta'] = df_riqueza['Variable'].str.split('\n').str[0].str.strip()

        tabla_limpia_riqueza = df_riqueza.pivot_table(index='Year', columns=['Variable_corta', 'Percentile'], values='Value')
        tabla_limpia_riqueza.columns = ['riqueza_promedio_adulto', 'pct50_mas_pobre', 'pct10_mas_rico', 'pct1_mas_rico', 'ratio_riqueza_ingreso']

        tabla_1980_2024 = tabla_limpia_riqueza.loc[1980:2024]
        years_r = sorted(tabla_1980_2024.index.tolist())
        valores_r = tabla_1980_2024['ratio_riqueza_ingreso']

        valor_1980 = valores_r.loc[1980]
        valor_2024 = valores_r.loc[2024]

        frames_r = []
        for year in years_r:
            x_vals = [y for y in years_r if y <= year]

            punto_1980_x = [1980] if year >= 1980 else []
            punto_1980_y = [valor_1980] if year >= 1980 else []
            punto_1980_t = [f'{valor_1980:.2f}'] if year >= 1980 else []

            punto_2024_x = [2024] if year >= 2024 else []
            punto_2024_y = [valor_2024] if year >= 2024 else []
            punto_2024_t = [f'{valor_2024:.2f}'] if year >= 2024 else []

            frames_r.append(go.Frame(data=[
                go.Scatter(x=x_vals, y=valores_r.loc[x_vals], mode='lines', line=dict(color='#333333', width=3), showlegend=False),
                go.Scatter(x=punto_1980_x, y=punto_1980_y, mode='markers+text', text=punto_1980_t, textposition='bottom right', marker=dict(size=10, color='#d62728'), textfont=dict(size=16, color='black'), cliponaxis=False, showlegend=False),
                go.Scatter(x=punto_2024_x, y=punto_2024_y, mode='markers+text', text=punto_2024_t, textposition='bottom right', marker=dict(size=10, color='#d62728'), textfont=dict(size=16, color='black'), cliponaxis=False, showlegend=False),
            ], name=str(year)))

        fig_ratio_anim = go.Figure(
            data=frames_r[0].data,
            frames=frames_r
        )

        fig_ratio_anim.update_layout(
            xaxis=dict(title='Año', range=[1980, 2024], automargin=True, showticklabels=False),
            yaxis=dict(title=dict(text='Ratio riqueza/ingreso', font=dict(size=20)), range=[valor_1980 - 0.5, valor_2024 + 0.5], automargin=True, tickfont=dict(size=16)),
            height=350,
            margin=dict(r=40),
            updatemenus=[dict(type='buttons', showactive=False,
                buttons=[dict(label='Play', method='animate',
                               args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)])])],
            sliders=[dict(steps=[dict(method='animate', args=[[str(y)], dict(frame=dict(duration=0, redraw=True), mode='immediate')], label=str(y)) for y in years_r], active=0)]
        )
        st.markdown("<p style='font-size: 16px; color: #666; margin-top: -10px;'>Este ratio mide cuántos años de ingresos anuales se necesitarían para igualar la riqueza total acumulada.</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_ratio_anim, use_container_width=True)

        st.markdown("<style>.stAlert p { font-size: 19px !important; }</style>", unsafe_allow_html=True)
        st.info(f"El ratio pasó de {valor_1980:.2f} a {valor_2024:.2f} - es decir, la riqueza acumulada pasó de equivaler a {valor_1980:.2f} años de ingreso mundial a {valor_2024:.2f} años. El mundo acumula riqueza mucho más rápido de lo que crece.")

def mostrar_capital_trabajo():
    st.header("El marco teórico de Thomas Piketty: el capital gana peso frente al trabajo")

    tab_teoria, tab_grafico = st.tabs(["Teoría", "Gráfico"])

    with tab_teoria:
        st.markdown("""
        <div style="background-color: #fffbeb; border-left: 4px solid #D4AF37; padding: 25px; border-radius: 5px;">
            <p style="font-size: 26px; font-weight: bold; margin-bottom: 15px;">El capital gana peso frente al trabajo</p>
            <br>
            <p style="font-size: 18px; margin-bottom: 30px;">El dinero que genera una economía cada año se reparte, en términos generales, entre dos "bolsillos": el capital (beneficios de empresas, dividendos, rentas de alquiler, intereses) y el trabajo (sueldos y salarios).</p>
            <br>
            <p style="font-size: 18px; margin-bottom: 30px;">Con el tiempo, según observa Piketty, una parte cada vez mayor de ese ingreso total va a parar al capital, en vez de al trabajo. Esto no significa necesariamente que los sueldos bajen en términos absolutos - significa que crecen más despacio que los beneficios del capital, así que su peso relativo dentro del total del ingreso se reduce.</p>
            <br>
            <p style="font-size: 18px; margin: 0;">Esta tendencia es la contraparte visible de la acumulación de riqueza que vimos en β = s/g: si la riqueza acumulada (en forma de capital) crece más rápido que la economía, es razonable esperar que la parte del ingreso que corresponde a esa riqueza (beneficios, rentas) también gane peso frente a los sueldos.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab_grafico:
        st.header("Capital VS Trabajo: participación en el ingreso mundial (1980-2024)")

        participacion_capital_por_region = pd.read_csv("capital_share_por_region.csv").sort_values('year').reset_index(drop=True)
        participacion_trabajo_por_region = pd.read_csv("labor_share_por_region.csv").sort_values('year').reset_index(drop=True)

        participacion_capital_por_region = participacion_capital_por_region[participacion_capital_por_region['year'] <= 2024].reset_index(drop=True)
        participacion_trabajo_por_region = participacion_trabajo_por_region[participacion_trabajo_por_region['year'] <= 2024].reset_index(drop=True)

        años_capital_trabajo = participacion_capital_por_region['year'].tolist()
        capital_world_pct = (participacion_capital_por_region['World'] * 100).tolist()
        trabajo_world_pct = (participacion_trabajo_por_region['World'] * 100).tolist()

        ultimo_año = años_capital_trabajo[-1]
        años_etiqueta_ct = [1980, 1990, 2000, 2010, 2020, ultimo_año]

        frames_ct = []
        annotations_ct = []

        for i, año in enumerate(años_capital_trabajo):
            es_primero = (año == 1980)
            es_ultimo = (año == ultimo_año)

            punto_capital_ini_x = [1980] if año >= 1980 else []
            punto_capital_ini_y = [capital_world_pct[0]] if año >= 1980 else []
            punto_trabajo_ini_x = [1980] if año >= 1980 else []
            punto_trabajo_ini_y = [trabajo_world_pct[0]] if año >= 1980 else []

            punto_capital_fin_x = [ultimo_año] if año >= ultimo_año else []
            punto_capital_fin_y = [capital_world_pct[-1]] if año >= ultimo_año else []
            punto_trabajo_fin_x = [ultimo_año] if año >= ultimo_año else []
            punto_trabajo_fin_y = [trabajo_world_pct[-1]] if año >= ultimo_año else []

            data = [
                go.Scatter(x=años_capital_trabajo[:i+1], y=capital_world_pct[:i+1], mode='lines', name='Capital', line=dict(color='#d62728', width=3)),
                go.Scatter(x=años_capital_trabajo[:i+1], y=trabajo_world_pct[:i+1], mode='lines', name='Trabajo', line=dict(color='#17becf', width=3)),
                go.Scatter(x=punto_capital_ini_x, y=punto_capital_ini_y, mode='markers', marker=dict(size=10, color='#d62728'), cliponaxis=False, showlegend=False),
                go.Scatter(x=punto_capital_fin_x, y=punto_capital_fin_y, mode='markers', marker=dict(size=10, color='#d62728'), cliponaxis=False, showlegend=False),
                go.Scatter(x=punto_trabajo_ini_x, y=punto_trabajo_ini_y, mode='markers', marker=dict(size=10, color='#17becf'), cliponaxis=False, showlegend=False),
                go.Scatter(x=punto_trabajo_fin_x, y=punto_trabajo_fin_y, mode='markers', marker=dict(size=10, color='#17becf'), cliponaxis=False, showlegend=False),
            ]
            if año in años_etiqueta_ct:
                xshift_val = 15 if (es_primero or es_ultimo) else 0
                xanchor_val = 'left' if (es_primero or es_ultimo) else 'center'
                annotations_ct.append(dict(x=año, y=capital_world_pct[i], text=f'{capital_world_pct[i]:.1f}%', showarrow=False, yshift=12, xshift=xshift_val, xanchor=xanchor_val, font=dict(size=14, color='#444444')))
                annotations_ct.append(dict(x=año, y=trabajo_world_pct[i], text=f'{trabajo_world_pct[i]:.1f}%', showarrow=False, yshift=-12, xshift=xshift_val, xanchor=xanchor_val, font=dict(size=14, color='#444444')))
            frames_ct.append(go.Frame(data=data, name=str(año), layout=go.Layout(annotations=list(annotations_ct))))

        fig_capital_trabajo_world = go.Figure(
            data=frames_ct[0].data,
            frames=frames_ct,
            layout=go.Layout(
                xaxis=dict(title='Año', range=[1980, 2024]),
                yaxis=dict(title=dict(text='% del ingreso mundial', font=dict(size=20)), range=[30, 65], tickfont=dict(size=16)),
                legend=dict(orientation='h', x=0.5, y=1.1, xanchor='center', yanchor='bottom', font=dict(size=16)),
                margin=dict(t=100, b=50, r=80),
                height=380,
                updatemenus=[dict(type='buttons', showactive=False,
                                   buttons=[dict(label='Play', method='animate',
                                                 args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)])])]
            )
        )

        st.plotly_chart(fig_capital_trabajo_world, use_container_width=True)

        st.markdown("<style>.stAlert p { font-size: 19px !important; }</style>", unsafe_allow_html=True)
        st.info(f"A nivel mundial, la parte del ingreso que va al capital (beneficios, dividendos, rentas) subió del 39% (1980) al 47% ({ultimo_año}). En paralelo, la parte que va al trabajo (sueldos) bajó del 61% al 53%.")

def mostrar_viaje():
    st.header("El viaje metodológico")

    pasos = [
        ("1", "Primer intento", 'Según la teoría de Piketty, si el capital gana peso en la economía y está concentrado en pocas manos, ese "trozo mayor del pastel" debería ir a quienes ya tienen capital. Para comprobarlo, correlacioné capital_share y top_1 directamente, año a año. Los resultados parecían fuertes - hasta 0.92 en algunas regiones, valores muy altos para ciencias sociales.', '#1f3b73'),
        ("2", "Detecté el problema", "Ambas variables suben con el tiempo por separado; eso, por sí solo, ya genera una correlación alta sin que exista relación real (correlación espuria). Lo corregí usando tasas de crecimiento, no valores absolutos.", '#d62728'),
        ("3", "Las regiones no se comportan igual", "Con el método correcto, vi que solo una región (Rusia) mostraba relación significativa. Usé un modelo de efectos mixtos, que permite que cada región tenga su propia relación, en vez de forzar a las 8 a comportarse igual.", '#2ca02c'),
        ("4", "Solo 8 grupos", "El propio modelo de efectos mixtos mostró señales de fragilidad al intentar ajustar tantos parámetros con tan pocas regiones. Con solo 8 grupos, los métodos estadísticos estándar para calcular la fiabilidad de un resultado tampoco son de fiar. Usé wild cluster bootstrap, el método diseñado específicamente para esta situación.", '#ff7f0e'),
    ]

    for numero, titulo, texto, color in pasos:
        st.markdown(f"""
        <div style="background-color: {color}15; border-left: 4px solid {color}; padding: 15px; margin-bottom: 15px; border-radius: 5px;">
            <p style="font-size: 20px; font-weight: bold; margin-bottom: 8px; color: {color};">{numero}. {titulo}</p>
            <p style="margin: 0;">{texto}</p>
        </div>
        """, unsafe_allow_html=True)

def mostrar_correlacion():
    st.header("¿Todo esto se traduce en concentración? Poniendo a prueba la teoría de Piketty")

    tab_teoria, tab_paso1, tab_paso2, tab_paso3, tab_paso4, tab_paso5, tab_paso6 = st.tabs([
        "Teoría", "Paso 1: Scatterplot", "Paso 2: Pearson", "Paso 3: Wild Cluster Bootstrap",
        "Paso 4: Scatterplot por macrorregión", "Paso 5: Pearson por macrorregión", "Paso 6: Block Bootstrap"
    ])

    with tab_teoria:
        st.markdown("""
        <div style="background-color: #fffbeb; border-left: 4px solid #D4AF37; padding: 25px; border-radius: 5px;">
            <p style="font-size: 18px; margin-bottom: 20px;">La pregunta que queda es: ¿eso se traduce en más concentración de riqueza? La teoría de Piketty se apoya en dos piezas: cuánto peso tiene el capital en la economía, y quién posee ese capital - si está repartido, o concentrado.</p>
            <br>
            <p style="font-size: 26px; font-weight: bold; margin-bottom: 15px;">r &gt; g: según Piketty, es el motor de la concentración</p>
            <br>
            <p style="font-size: 18px; margin-bottom: 15px;">Piketty lo formula así: cuando el capital rinde más (r) que lo que crece la economía (g), la riqueza tiende a concentrarse - salvo intervención política. Es lo que pasa cuando las dos piezas se juntan: si el capital gana peso y está en pocas manos, el top 1% debería concentrar más riqueza, generando desigualdad.</p>
            <br>
            <p style="font-size: 18px; margin: 0;">Cómo se conecta con este proyecto: si el capital gana peso y está concentrado en pocas manos, el top 1% debería concentrar más riqueza. Eso es lo que se comprueba a continuación.</p>
        </div>
        """, unsafe_allow_html=True)

    fig_scatter, r_obs, ci_bajo, ci_alto, p_valor_bootstrap, fig_hist, fig_grid, fig_barras_region, tabla_block = preparar_wild_bootstrap()

    with tab_paso1:
        mostrar_paso1_scatter(fig_scatter)

    with tab_paso2:
        mostrar_paso2_pearson(r_obs)

    with tab_paso3:
        mostrar_paso3_bootstrap(r_obs, p_valor_bootstrap, fig_hist)

    with tab_paso4:
        mostrar_paso4_grid(fig_grid)

    with tab_paso5:
        mostrar_paso5_barras(fig_barras_region)

    with tab_paso6:
        mostrar_paso6_block_bootstrap(tabla_block)

def circulo_paso(numero):
    st.markdown(f"""
    <div style="width:36px; height:36px; border-radius:50%; background-color:#333333; color:white;
                display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:18px;">
        {numero}
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def preparar_wild_bootstrap():
    cap = pd.read_csv("capital_share_por_region.csv").set_index('year')
    top1 = pd.read_csv("top1_riqueza_ancho_regiones.csv", index_col='Year')
    cap = cap.loc[1980:2024]
    top1 = top1.loc[1980:2024]
    regiones = [c for c in cap.columns if c != 'World']

    colores = {
        'Europe': '#1f3b73', 'Middle East & North Africa': '#d62728', 'Latin America': '#2ca02c',
        'Sub-Saharan Africa': '#bcbd22', 'East Asia': '#17becf', 'South & Southeast Asia': '#7f7f7f',
        'North America & Oceania': '#6a0dad', 'Russia & Central Asia': '#e83e8c'
    }

    fig_scatter = go.Figure()
    x_all, y_all = [], []
    for region in regiones:
        x_vals = cap[region].dropna()
        y_vals = top1[region].dropna()
        idx_comun = x_vals.index.intersection(y_vals.index)
        x_vals, y_vals = x_vals.loc[idx_comun], y_vals.loc[idx_comun]
        fig_scatter.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='markers', name=region, marker=dict(color=colores.get(region, 'gray'), size=8, opacity=0.7)))
        x_all.extend(x_vals.tolist())
        y_all.extend(y_vals.tolist())

    pendiente, intercepto = np.polyfit(x_all, y_all, 1)
    x_line = np.linspace(min(x_all), max(x_all), 100)
    fig_scatter.add_trace(go.Scatter(x=x_line, y=intercepto + pendiente * x_line, mode='lines', name='Línea de tendencia', line=dict(color='black', dash='dash', width=2)))

    fig_scatter.update_layout(
        xaxis=dict(title=dict(text='Participación del capital (fracción)', font=dict(size=18))),
        yaxis=dict(title=dict(text='Participación del top_1 en la riqueza (fracción)', font=dict(size=18))),
        height=450
    )

    filas_panel = []
    for region in regiones:
        for year in cap.index:
            x = cap.loc[year, region]
            try:
                y = top1.loc[year, region]
                if pd.notna(x) and pd.notna(y):
                    filas_panel.append({'region': region, 'year': year, 'capital': x, 'top1': y})
            except:
                pass
    panel = pd.DataFrame(filas_panel)

    r_obs, p_naive = stats.pearsonr(panel['capital'], panel['top1'])

    modelo_fit = smf.ols('top1 ~ capital', panel).fit()
    residuos = modelo_fit.resid
    ajustados = modelo_fit.fittedvalues

    modelo_nulo = smf.ols('top1 ~ 1', panel).fit()
    residuos_nulo = modelo_nulo.resid
    ajustados_nulo = modelo_nulo.fittedvalues

    regiones_unicas = panel['region'].unique()
    np.random.seed(42)
    n_replicas = 10000
    r_estrella = []
    r_estrella_nulo = []

    for b in range(n_replicas):
        signos_por_region = {region: np.random.choice([-1, 1]) for region in regiones_unicas}
        signos_fila = panel['region'].map(signos_por_region)

        top1_estrella = ajustados + residuos * signos_fila
        r_b, _ = stats.pearsonr(panel['capital'], top1_estrella)
        r_estrella.append(r_b)

        top1_estrella_nulo = ajustados_nulo + residuos_nulo * signos_fila
        r_b_nulo, _ = stats.pearsonr(panel['capital'], top1_estrella_nulo)
        r_estrella_nulo.append(r_b_nulo)

    r_estrella = np.array(r_estrella)
    r_estrella_nulo = np.array(r_estrella_nulo)

    ci_bajo, ci_alto = np.percentile(r_estrella, [2.5, 97.5])
    p_valor_bootstrap = np.mean(np.abs(r_estrella_nulo) >= np.abs(r_obs))

    bordes_hist = np.linspace(r_estrella.min(), r_estrella.max(), 51)
    ancho_bin_hist = bordes_hist[1] - bordes_hist[0]
    counts_hist, bin_edges_hist = np.histogram(r_estrella, bins=bordes_hist)
    bin_centers_hist = (bin_edges_hist[:-1] + bin_edges_hist[1:]) / 2

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Bar(
        x=bin_centers_hist, y=counts_hist, width=ancho_bin_hist * 0.85,
        marker=dict(color=bin_centers_hist, colorscale=[[0, '#2dd4bf'], [1, '#3b82f6']], line=dict(width=0))
    ))
    fig_hist.add_vline(x=r_obs, line_dash='solid', line_color='black',
                        annotation_text=f'r observado = {r_obs:.3f}', annotation_position='top',
                        annotation_font=dict(size=22))
    fig_hist.update_layout(
        xaxis=dict(title=dict(text='Pearson r (por réplica)', font=dict(size=18))),
        yaxis=dict(title=dict(text='Frecuencia', font=dict(size=18))),
        height=450
    )

        # Paso 4: grid de 8 mini-scatterplots, uno por región, con línea de tendencia propia
    fig_grid = make_subplots(rows=2, cols=4, subplot_titles=regiones)
    fig_grid.update_annotations(font_size=24)
    for i, region in enumerate(regiones):
        fila_grid = i // 4 + 1
        col_grid = i % 4 + 1
        x_vals = cap[region].dropna()
        y_vals = top1[region].dropna()
        idx_comun = x_vals.index.intersection(y_vals.index)
        x_vals, y_vals = x_vals.loc[idx_comun], y_vals.loc[idx_comun]

        fig_grid.add_trace(
            go.Scatter(x=x_vals, y=y_vals, mode='markers', showlegend=False,
                       marker=dict(size=5, color=colores.get(region, 'gray'))),
            row=fila_grid, col=col_grid
        )
        pendiente_region, intercepto_region = np.polyfit(x_vals, y_vals, 1)
        x_line_region = np.linspace(x_vals.min(), x_vals.max(), 50)
        fig_grid.add_trace(
            go.Scatter(x=x_line_region, y=intercepto_region + pendiente_region * x_line_region,
                       mode='lines', showlegend=False, line=dict(color='black', width=2, dash='dash')),
            row=fila_grid, col=col_grid
        )
    fig_grid.update_layout(height=650)

    # Paso 5: Pearson por macrorregión (r "en crudo")
    correlaciones_region = {}
    for region in regiones:
        correlaciones_region[region] = cap[region].corr(top1[region])
    correlaciones_region = pd.Series(correlaciones_region).sort_values(ascending=False)

    fig_barras_region = go.Figure()
    colores_barras_region = ['#1f77b4' if v >= 0 else '#d62728' for v in correlaciones_region.values]
    fig_barras_region.add_trace(go.Bar(
        x=correlaciones_region.values, y=correlaciones_region.index, orientation='h',
        marker_color=colores_barras_region,
        text=[f'{v:.3f}' for v in correlaciones_region.values], textposition='outside',
        textfont=dict(size=24, color='#444444')
    ))
    fig_barras_region.update_layout(
        xaxis=dict(title=dict(text='Pearson r', font=dict(size=20)), range=[-1.05, 1.05], tickvals=[-1, -0.5, 0, 0.5, 1], tickfont=dict(size=16)),
        yaxis=dict(autorange='reversed', tickfont=dict(size=18)),
        height=450
    )

    # Paso 6: Block Bootstrap - CI y p-valor por región
    np.random.seed(42)
    n_replicas_block = 10000
    longitud_bloque = 5
    resultados_block = {}

    for region in regiones:
        x_vals = cap[region].dropna()
        y_vals = top1[region].dropna()
        idx_comun = x_vals.index.intersection(y_vals.index)
        x_vals, y_vals = x_vals.loc[idx_comun], y_vals.loc[idx_comun]

        n = len(x_vals)
        n_bloques = int(np.ceil(n / longitud_bloque))
        r_observado_region, _ = stats.pearsonr(x_vals, y_vals)

        r_bloques = []
        media_y = y_vals.mean()
        residuos_nulo = (y_vals - media_y).values
        r_bloques_nulo = []

        for b in range(n_replicas_block):
            indices_remuestreados = []
            for _ in range(n_bloques):
                inicio = np.random.randint(0, n - longitud_bloque + 1)
                indices_remuestreados.extend(range(inicio, inicio + longitud_bloque))
            indices_remuestreados = indices_remuestreados[:n]

            x_b = x_vals.iloc[indices_remuestreados]
            y_b = y_vals.iloc[indices_remuestreados]
            r_b, _ = stats.pearsonr(x_b, y_b)
            r_bloques.append(r_b)

            y_b_nulo = media_y + residuos_nulo[indices_remuestreados]
            r_b_nulo, _ = stats.pearsonr(x_vals.values, y_b_nulo)
            r_bloques_nulo.append(r_b_nulo)

        r_bloques = np.array(r_bloques)
        r_bloques_nulo = np.array(r_bloques_nulo)
        ci_bajo_region, ci_alto_region = np.percentile(r_bloques, [2.5, 97.5])
        p_valor_region = np.mean(np.abs(r_bloques_nulo) >= np.abs(r_observado_region))

        resultados_block[region] = {
            'r': r_observado_region, 'CI_bajo': ci_bajo_region, 'CI_alto': ci_alto_region, 'p_valor': p_valor_region
        }

    tabla_block = pd.DataFrame(resultados_block).T
    tabla_block = tabla_block.sort_values('r', ascending=False)

    return fig_scatter, r_obs, ci_bajo, ci_alto, p_valor_bootstrap, fig_hist, fig_grid, fig_barras_region, tabla_block

def mostrar_paso1_scatter(fig_scatter):
    st.subheader("¿Suben juntas?")
    st.markdown("<p style='font-size: 16px; color: #666; margin-top: -10px;'>Eje X = qué parte del ingreso de esa economía fue a parar al capital. Eje Y = qué parte de la riqueza total tenía el 1% más rico de esa región.</p>", unsafe_allow_html=True)
    col_num, col_chart = st.columns([1, 20])
    with col_num:
        circulo_paso(1)
    with col_chart:
        st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("""
    <div style="background-color: #eaf2fb; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; font-size: 19px; color: #1f77b4;">
    Los puntos se agrupan en bloques compactos por macrorregión, cada uno ocupando un rango. La línea de tendencia sugiere una relación positiva a nivel global, pero tenemos que interpretarla con mucho cuidado.
    </div>
    """, unsafe_allow_html=True)

def mostrar_paso2_pearson(r_obs):
    col_num, col_content = st.columns([1, 20])
    with col_num:
        circulo_paso(2)

    with col_content:
        pos_marca = min(max(r_obs, 0), 1) * 100

        st.markdown(f"""
        <div style="background-color: #fffbeb; border-left: 6px solid #D4AF37; padding: 40px 56px; margin-bottom: 32px;">
            <p style="font-size: 44px; font-weight: 500; text-align: center; margin: 0 0 28px; color: #3a2f00;">Pearson r = {r_obs:.3f}</p>
            <hr style="border: none; border-top: 1px solid #D4AF37; margin: 0 0 32px;">
            <div style="max-width: 700px; margin: 0 auto 30px;">
                <div style="display: flex; margin-bottom: 4px;">
                    <div style="width: 40%; background: #eaf2fb; color: #0c447c; text-align: center; font-size: 18px; padding: 6px 0;">Débil</div>
                    <div style="width: 30%; background: #fce9d6; color: #854f0b; text-align: center; font-size: 18px; padding: 6px 0;">Moderada</div>
                    <div style="width: 30%; background: #f6d3d3; color: #a32d2d; text-align: center; font-size: 18px; padding: 6px 0;">Fuerte</div>
                </div>
                <div style="position: relative; height: 16px; background: linear-gradient(to right, #eaf2fb 0%, #eaf2fb 40%, #fce9d6 40%, #fce9d6 70%, #f6d3d3 70%, #f6d3d3 100%); margin-bottom: 8px;">
                    <div style="position: absolute; left: {pos_marca}%; top: -8px; width: 4px; height: 32px; background: #3a2f00;"></div>
                </div>
                <div style="position: relative; height: 20px; font-size: 16px; color: #5a4a00;">
                    <span style="position: absolute; left: 0%; transform: translateX(0%);">0</span>
                    <span style="position: absolute; left: 40%; transform: translateX(-50%);">0.4</span>
                    <span style="position: absolute; left: 70%; transform: translateX(-50%);">0.7</span>
                    <span style="position: absolute; left: 100%; transform: translateX(-100%);">1</span>
                </div>
            </div>
            <p style="font-size: 26px; text-align: center; margin: 0; color: #5a4a00;">La correlación de Pearson sugiere una asociación positiva moderada entre las dos variables.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-size: 28px; font-weight: 500; margin: 0 0 18px;'>Limitaciones</p>", unsafe_allow_html=True)

        col_lim1, col_lim2 = st.columns(2)
        with col_lim1:
            st.markdown("""
            <div style="background-color: #eaf2fb; border-left: 6px solid #1f77b4; padding: 22px 26px; font-size: 24px; color: #0c447c;">
            <span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background-color: #d62728; margin-right: 10px;"></span>Tenemos solo 8 clusters
            </div>
            """, unsafe_allow_html=True)
        with col_lim2:
            st.markdown("""
            <div style="background-color: #eaf2fb; border-left: 6px solid #1f77b4; padding: 22px 26px; font-size: 24px; color: #0c447c;">
            <span style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; background-color: #d62728; margin-right: 10px;"></span>Datos correlacionados dentro de cada cluster
            </div>
            """, unsafe_allow_html=True)

def mostrar_paso3_bootstrap(r_obs, p_valor_bootstrap, fig_hist):
    col_num3, col_hist = st.columns([1, 20])
    with col_num3:
        circulo_paso(3)
    with col_hist:
        st.subheader("Wild Cluster Bootstrap - 10.000 réplicas, cluster = macrorregión")
        st.plotly_chart(fig_hist, use_container_width=True)

        col_r3, col_p3, col_comentario3 = st.columns([1, 1, 2], gap="large")
        with col_r3:
            st.markdown(f"""
            <div style="background-color: #fffbeb; border-left: 4px solid #D4AF37; padding: 15px; border-radius: 5px; font-size: 26px; min-height: 100px; display: flex; align-items: center;">
            r observado: {r_obs:.3f}
            </div>
            """, unsafe_allow_html=True)
        with col_p3:
            st.markdown(f"""
            <div style="background-color: #fffbeb; border-left: 4px solid #D4AF37; padding: 15px; border-radius: 5px; font-size: 26px; min-height: 100px; display: flex; align-items: center;">
            p-valor: {p_valor_bootstrap:.4f}
            </div>
            """, unsafe_allow_html=True)
        with col_comentario3:
            st.markdown(f"""
            <div style="background-color: #eaf2fb; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; font-size: 19px; color: #1f77b4; min-height: 100px; display: flex; align-items: center;">
            El p-valor ({p_valor_bootstrap:.4f}) queda por encima del umbral habitual de 0.05 - no se puede confirmar que la asociación no se deba al azar.
            </div>
            """, unsafe_allow_html=True)

def mostrar_paso4_grid(fig_grid):
    col_num4, col_grid = st.columns([1, 20])
    with col_num4:
        circulo_paso(4)
    with col_grid:
        st.subheader("Cada macrorregión con línea de tendencia propia")
        st.markdown("<p style='font-size: 16px; color: #666; margin-top: -10px;'>En todos los gráficos: eje X = qué parte del ingreso de esa economía fue a parar al capital, eje Y = qué parte de la riqueza total tenía el 1% más rico de esa región.</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_grid, use_container_width=True)

def mostrar_paso5_barras(fig_barras_region):
    col_num5, col_barras = st.columns([1, 20])
    with col_num5:
        circulo_paso(5)
    with col_barras:
        st.subheader("Pearson por macrorregión")
        st.plotly_chart(fig_barras_region, use_container_width=True)

        st.markdown("""
        <div style="background-color: #eaf2fb; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; font-size: 18px; color: #1f77b4;">
        Vemos que las relaciones no son iguales en todas las macrorregiones. Tenemos correlaciones positivas muy altas o moderadas, pero también encontramos regiones con correlaciones negativas.
        </div>
        """, unsafe_allow_html=True)

def mostrar_paso6_block_bootstrap(tabla_block):
    col_num6, col_bloque = st.columns([1, 20])
    with col_num6:
        circulo_paso(6)
    with col_bloque:
        st.subheader("Block Bootstrap | Bloques de 5 años consecutivos | P-valor por región")

        filas_html = ""
        for region in tabla_block.index:
            r_val = tabla_block.loc[region, 'r']
            p_val = tabla_block.loc[region, 'p_valor']
            if p_val >= 0.05:
                color_fondo = '#fdf6e3'
            elif r_val >= 0:
                color_fondo = '#eaf2fb'
            else:
                color_fondo = '#fbeaea'
            filas_html += (
                f'<tr style="background-color: {color_fondo};">'
                f'<td style="padding: 20px 24px; font-size: 24px;">{region}</td>'
                f'<td style="padding: 20px 24px; font-size: 24px; font-weight: bold; text-align: center;">{r_val:.3f}</td>'
                f'<td style="padding: 20px 24px; font-size: 24px; color: #555; text-align: center;">{p_val:.4f}</td>'
                f'</tr>'
            )

        st.markdown(
            '<table style="width: 100%; border-collapse: collapse; margin-top: 20px;">'
            '<thead><tr>'
            '<th style="text-align: left; padding: 14px 24px; font-size: 24px;">Región</th>'
            '<th style="text-align: center; padding: 14px 24px; font-size: 24px;">r</th>'
            '<th style="text-align: center; padding: 14px 24px; font-size: 24px;">p-valor</th>'
            '</tr></thead>'
            f'<tbody>{filas_html}</tbody>'
            '</table>'
            '<div style="display: flex; gap: 32px; margin-top: 20px; font-size: 19px; color: #555;">'
            '<span><span style="display: inline-block; width: 18px; height: 18px; background: #eaf2fb; margin-right: 8px;"></span>Positiva, significativa (p&lt;0.05)</span>'
            '<span><span style="display: inline-block; width: 18px; height: 18px; background: #fbeaea; margin-right: 8px;"></span>Negativa, significativa (p&lt;0.05)</span>'
            '<span><span style="display: inline-block; width: 18px; height: 18px; background: #fdf6e3; margin-right: 8px;"></span>No significativa (p&ge;0.05)</span>'
            '</div>',
            unsafe_allow_html=True
        )

def mostrar_paso4_interpretacion(r_obs, ci_bajo, ci_alto, p_valor_bootstrap):
    col_num4, col_interp = st.columns([1, 20])
    with col_num4:
        circulo_paso(4)
    with col_interp:
        st.markdown(f"""
        Hay una asociación positiva entre capital_share y top_1 (r={r_obs:.3f}), pero con solo 8 macrorregiones, el intervalo de confianza [{ci_bajo:.3f}, {ci_alto:.3f}] y el p-valor ({p_valor_bootstrap:.4f}) muestran que la certeza estadística es limitada.

        **Conclusión**: los datos apoyan la idea de Piketty, pero no la confirman con la confianza estadística habitual.
        """)

def mostrar_escalado():
    st.header("Escalando el análisis")
    st.write("Con 8 regiones, la evidencia estadística era débil por sí misma. Escalé el análisis a 216 países individuales, usando datos de WID de 1980 a 2024 - esto multiplicó las observaciones de 352 a más de 9.500.")

    capital_paises = pd.read_csv("capital_share_mundo.csv", sep=';', skiprows=1)
    capital_paises.columns = [c.strip() for c in capital_paises.columns]
    capital_paises['iso2'] = capital_paises['Variable'].str.extract(r'_([A-Z]{2})\n').fillna(capital_paises['Variable'].str.extract(r'_([A-Z]{2})$')[0])

    datos_2024 = capital_paises[capital_paises['Year'] == 2024].copy()
    datos_2024['iso3'] = datos_2024['iso2'].apply(lambda x: pycountry.countries.get(alpha_2=x).alpha_3 if pycountry.countries.get(alpha_2=x) else None)
    datos_2024 = datos_2024.dropna(subset=['iso3'])

    fig = go.Figure(go.Choropleth(
        locations=datos_2024['iso3'],
        z=datos_2024['Value'] * 100,
        colorscale='RdYlGn_r',
        colorbar_title="% capital_share"
    ))
    fig.update_layout(
        geo=dict(showframe=False, projection_type='natural earth'),
        height=350,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Cada país está coloreado según qué parte de su economía va al capital (beneficios, rentas) en vez de al trabajo (sueldos), en 2024. Cuanto más rojo, mayor peso del capital sobre el trabajo en esa economía.")

    st.write("También añadí 4 variables económicas más, coherentes con el mismo marco teórico:")
    st.markdown("""
    - **Ratio riqueza/ingreso (K/Y)**: el propio β de Piketty, a nivel país
    - **National income**: el tamaño y crecimiento de la economía
    - **Inflación**: puede afectar de forma distinta según el tipo de patrimonio
    - **Capitalización bursátil**: el peso de la economía financiera
    """)

def mostrar_5variables():
    st.header("Regresión OLS con efectos fijos por país y errores estándar robustos agrupados por cluster")
    st.write("216 países + 4 variables más relacionadas con la misma teoría (Ratio K/Y, tamaño de la economía, inflación, capitalización bursátil). Solo una mostró relación significativa - y con un efecto muy pequeño.")

    nombres = ['Capital_share', 'Ratio K/Y', 'National income', 'Inflación', 'Market cap']
    coefs = [-0.00074, -0.00034, 0.0007, -0.001, 0.00041]
    errores = [0.00106*1.96, 0.00075*1.96, 0.00098*1.96, 0.00056*1.96, 0.00002*1.96]
    pvalores = [0.484, 0.6541, 0.4746, 0.0761, 0.0000]
    colores = ['#2ca02c' if p < 0.05 else '#B0B0B0' for p in pvalores]

    fig = go.Figure()
    for i, (nombre, coef, err, p, color) in enumerate(zip(nombres, coefs, errores, pvalores, colores)):
        fig.add_trace(go.Scatter(
            x=[coef], y=[nombre],
            error_x=dict(type='data', array=[err], visible=True, color='gray'),
            mode='markers', marker=dict(size=16, color=color),
            name=nombre, showlegend=False,
            text=f'p = {p:.4f}' + (' (significativa)' if p < 0.05 else ''),
            hoverinfo='text'
        ))

    fig.add_vline(x=0, line_dash='dash', line_color='red')
    fig.update_layout(
        xaxis=dict(title='Efecto sobre el crecimiento del top_1 (variables estandarizadas)'),
        yaxis=dict(title=''),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

def mostrar_sintesis():
    st.header("Síntesis")

    st.markdown("""
    Puse a prueba la hipótesis de Piketty - que el capital ganando peso frente al trabajo explica la concentración de riqueza - con ocho macrorregiones, luego con 216 países, añadiendo variables adicionales, y finalmente replicando el método de un estudio académico especializado. En ninguno de estos análisis, usando datos de riqueza, el mecanismo se sostuvo con evidencia estadística sólida. Solo apareció una relación clara al medir sobre ingreso, con una fuente de datos distinta, en un grupo reducido de países ricos - un matiz interesante y adicional, no una confirmación de la hipótesis central.
    """)

    st.divider()
    st.header("Limitaciones")

    st.markdown("""
    - **Asociación estadística, no causalidad**: incluso el resultado más riguroso obtenido con el wild cluster bootstrap - que corrige el problema de tener pocos grupos, solo confirma que capital_share y top_1 se mueven juntos con cierta fiabilidad - en ningún momento demuestra que el capital *cause* la concentración de riqueza. 
    - **El hallazgo positivo se basa en una muestra pequeña**: la base de Bengtsson-Waldenström consta de 20 países, entre ellos Argentina y Brasil no tienen dato de capital_share neto disponible, dejando 18 países - además todas economías ricas, que no representan la diversidad del análisis mundial de 216 países.
    """)

def mostrar_estancamiento():
    st.header("Cuota de riqueza mundial por grupo (1980-2024) - de año en año")

    df_riqueza = pd.read_csv("wid_riqueza_1950_2025.csv", sep=';', skiprows=1)
    df_riqueza.columns = [c.strip() for c in df_riqueza.columns]
    df_riqueza['Variable_corta'] = df_riqueza['Variable'].str.split('\n').str[0].str.strip()
    tabla_limpia_riqueza = df_riqueza.pivot_table(index='Year', columns=['Variable_corta', 'Percentile'], values='Value')
    tabla_limpia_riqueza.columns = ['riqueza_promedio_adulto', 'pct50_mas_pobre', 'pct10_mas_rico', 'pct1_mas_rico', 'ratio_riqueza_ingreso']

    tabla_1980_2024 = tabla_limpia_riqueza.loc[1980:2024]
    años = tabla_1980_2024.index.tolist()
    años_etiqueta = [1980, 1990, 2000, 2010, 2020, 2024]

    grupos = {
        'Top 10%': ('pct10_mas_rico', '#d62728'),
        'Top 1%': ('pct1_mas_rico', '#ff7f0e'),
        'Bottom 50%': ('pct50_mas_pobre', '#1f77b4'),
    }

    frames = []
    annotations_acumuladas = []

    for i, año_actual in enumerate(años):
        data = []
        for label, (col, color) in grupos.items():
            y_vals = (tabla_1980_2024[col] * 100).iloc[:i+1].tolist()
            x_vals = años[:i+1]
            data.append(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=label, line=dict(color=color, width=2)))
            if año_actual in años_etiqueta:
                val = tabla_1980_2024.loc[año_actual, col] * 100
                annotations_acumuladas.append(dict(
                    x=año_actual, y=val, text=f'{val:.1f}%',
                    showarrow=False, yshift=10, xshift=15,
                    xanchor='left', font=dict(size=9)
                ))
        frames.append(go.Frame(data=data, name=str(año_actual), layout=go.Layout(annotations=list(annotations_acumuladas))))

    fig = go.Figure(
        data=frames[0].data,
        frames=frames,
        layout=go.Layout(
            xaxis=dict(title='Año', range=[1980, 2024]),
            yaxis=dict(title='% de la riqueza mundial', range=[0, 88]),
            legend=dict(orientation='h', x=0.5, y=1.15, xanchor='center', yanchor='bottom'),
            margin=dict(t=100, l=60, r=65, b=50),
            height=500,
            updatemenus=[dict(type='buttons', showactive=False,
                               buttons=[dict(label='Play', method='animate',
                                             args=[None, dict(frame=dict(duration=150, redraw=True), fromcurrent=True)])])]
        )
    )
    st.plotly_chart(fig, use_container_width=True)

def mostrar_poblacion_riqueza():
    st.header("Medio mundo, un trocito de pastel")

    grupos = ['Bottom 50%', 'Top 10%', 'Top 1%']
    poblacion = [50, 10, 1]
    riqueza = [2.01, 74.55, 36.69]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=grupos, y=poblacion, name='% de la población', marker_color='#1f77b4',
                          text=[f'{v}%' for v in poblacion], textposition='outside'))
    fig.add_trace(go.Bar(x=grupos, y=riqueza, name='% de la riqueza mundial', marker_color='#d62728',
                          text=[f'{v}%' for v in riqueza], textposition='outside'))

    fig.update_layout(
        barmode='group',
        bargap=0.4,
        bargroupgap=0.1,
        height=450,
        yaxis=dict(title='%', range=[0, 85]),
        legend=dict(orientation='h', x=0.5, y=1.05, xanchor='center', yanchor='bottom'),
        margin=dict(t=80, l=60, r=40, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)

def mostrar_brecha_persona():
    mostrar_indicador_parte(3, "El impacto")
    st.header("La brecha y sus consecuencias")

    df_riqueza = pd.read_csv("wid_riqueza_1950_2025.csv", sep=';', skiprows=1)
    df_riqueza.columns = [c.strip() for c in df_riqueza.columns]
    df_riqueza['Variable_corta'] = df_riqueza['Variable'].str.split('\n').str[0].str.strip()
    tabla_limpia_riqueza = df_riqueza.pivot_table(index='Year', columns=['Variable_corta', 'Percentile'], values='Value')
    tabla_limpia_riqueza.columns = ['riqueza_promedio_adulto', 'pct50_mas_pobre', 'pct10_mas_rico', 'pct1_mas_rico', 'ratio_riqueza_ingreso']

    riqueza_promedio_adulto = tabla_limpia_riqueza['riqueza_promedio_adulto']
    cuotas_por_grupo = tabla_limpia_riqueza[['pct1_mas_rico', 'pct10_mas_rico', 'pct50_mas_pobre']]

    riqueza_por_persona_top1 = cuotas_por_grupo['pct1_mas_rico'] * riqueza_promedio_adulto / 0.01
    riqueza_por_persona_top10 = cuotas_por_grupo['pct10_mas_rico'] * riqueza_promedio_adulto / 0.10
    riqueza_por_persona_bottom50 = cuotas_por_grupo['pct50_mas_pobre'] * riqueza_promedio_adulto / 0.50

    col_izq, col_der = st.columns([1, 2.2])

    with col_izq:
        st.markdown("<p style='font-size: 30px; font-weight: bold;'>Menor movilidad social</p>", unsafe_allow_html=True)
        fig_mov = go.Figure()
        fig_mov.add_trace(go.Bar(x=['Ingreso', 'Riqueza'], y=[8.09, 2.25], marker_color=['#17becf', '#d62728'],
                                  text=['8.1%', '2.2%'], textposition='outside'))
        fig_mov.update_layout(title='50% Inferior (2024)', yaxis=dict(visible=False, range=[0, 12]), height=280, showlegend=False, margin=dict(t=40, b=20))
        st.plotly_chart(fig_mov, use_container_width=True)

        st.markdown("""
        <div style="background-color: #eaf2fb; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; font-size: 15px; color: #1f77b4;">
        Hemos visto que el 50% más pobre genera el <b>8.1%</b> del ingreso mundial, pero solo logra acumular el <b>2.2%</b> de la riqueza - una brecha entre lo que gana y lo que retiene.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #eaf2fb; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; font-size: 15px; color: #1f77b4; margin-top: 10px;">
        Sin margen para ahorrar o invertir, de esta forma le es muy difícil cambiar de posición económica.
        </div>
        """, unsafe_allow_html=True)

    with col_der:
        st.markdown("<p style='font-size: 30px; font-weight: bold;'>La distribución de la riqueza, en dólares por persona</p>", unsafe_allow_html=True)
        grupos = ['Bottom 50%', 'Top 10%', 'Top 1%']
        colores = ['#1f77b4', '#ff7f0e', '#d62728']

        fig = go.Figure()
        for grupo, color, valor_1980, valor_2024 in zip(
            grupos, colores,
            [riqueza_por_persona_bottom50.loc[1980], riqueza_por_persona_top10.loc[1980], riqueza_por_persona_top1.loc[1980]],
            [riqueza_por_persona_bottom50.loc[2024], riqueza_por_persona_top10.loc[2024], riqueza_por_persona_top1.loc[2024]]
        ):
            fig.add_trace(go.Bar(
                x=['1980', '2024'], y=[valor_1980, valor_2024], name=grupo, marker_color=color,
                text=[f'${valor_1980:,.0f}', f'${valor_2024:,.0f}'], textposition='outside',
                textfont=dict(size=18, color='#444444')
            ))

        fig.update_layout(
            xaxis=dict(title=dict(text='Año', font=dict(size=18))),
            yaxis=dict(title=dict(text='Riqueza por persona (USD, escala log)', font=dict(size=18)), type='log', automargin=True),
            barmode='group', height=320, margin=dict(l=100, b=80, t=40)
        )
        fig.update_xaxes(tickfont=dict(size=16, color='#444444'))
        fig.update_yaxes(tickfont=dict(size=16, color='#444444'))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div style="background-color: #eaf2fb; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; font-size: 15px; color: #1f77b4; margin-left: 70px;">
        El Top 1% aumentó su riqueza media <b>640 veces</b> más que el Bottom 50%, entre 1980 y 2024.<br><br>
        En 2024, una persona del Top 1% tiene, de media, <b>809.78 veces</b> más riqueza que una del Bottom 50%.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #eaf2fb; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; font-size: 15px; color: #1f77b4;  margin-top: 10px; margin-left: 70px;">
        Aunque el Bottom 50% también vio crecer su riqueza (de $1,112 a $5,874, un crecimiento del 428% en términos porcentuales), partía de una base tan pequeña que ese crecimiento no cierra la distancia real - la brecha en dólares no ha dejado de ampliarse.
        </div>
        """, unsafe_allow_html=True)

def mostrar_poder_adquisitivo():
    st.header("Menor poder adquisitivo del 50% más pobre")

    ingreso_bottom50 = pd.read_csv("WID_Data_12092026-163808.csv", sep=';', skiprows=1)
    ingreso_bottom50.columns = [c.strip() for c in ingreso_bottom50.columns]
    ingreso_bottom50['iso2'] = ingreso_bottom50['Variable'].str.extract(r'_([A-Z]{2})\n').fillna(ingreso_bottom50['Variable'].str.extract(r'_([A-Z]{2})$')[0])
    ingreso_bottom50['iso3'] = ingreso_bottom50['iso2'].apply(lambda x: pycountry.countries.get(alpha_2=x).alpha_3 if pd.notna(x) and pycountry.countries.get(alpha_2=x) else None)

    ingreso_ancho = ingreso_bottom50[ingreso_bottom50['iso3'].notna()].pivot_table(index='Year', columns='iso3', values='Value')

    inflacion_raw = pd.read_csv("API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_285.csv", skiprows=4)
    años_cols = [str(y) for y in range(1980, 2025)]
    inflacion_long = inflacion_raw.melt(id_vars=['Country Code'], value_vars=años_cols, var_name='Year', value_name='inflacion')
    inflacion_long['Year'] = inflacion_long['Year'].astype(int)
    inflacion_ancho = inflacion_long.pivot_table(index='Year', columns='Country Code', values='inflacion')

    resultados = {}
    for pais in ingreso_ancho.columns:
        if pais not in inflacion_ancho.columns:
            continue
        serie_ingreso = ingreso_ancho[pais].dropna()
        if len(serie_ingreso) < 20:
            continue
        año_inicio, año_fin = serie_ingreso.index.min(), serie_ingreso.index.max()
        inflacion_pais = inflacion_ancho[pais].loc[año_inicio:año_fin].dropna()
        if len(inflacion_pais) < 20:
            continue

        crecimiento_ingreso = (serie_ingreso.loc[año_fin] / serie_ingreso.loc[año_inicio] - 1) * 100
        inflacion_acumulada = ((1 + inflacion_pais / 100).prod() - 1) * 100

        resultados[pais] = {
            'crecimiento_ingreso': crecimiento_ingreso,
            'inflacion_acumulada': inflacion_acumulada,
            'gana_inflacion': inflacion_acumulada > crecimiento_ingreso
        }

    tabla = pd.DataFrame(resultados).T
    tabla['crecimiento_ingreso'] = tabla['crecimiento_ingreso'].astype(float)
    tabla['inflacion_acumulada'] = tabla['inflacion_acumulada'].astype(float)
    tabla['gana_inflacion'] = tabla['gana_inflacion'].astype(bool)
    tabla['ratio_log'] = np.log((1 + tabla['crecimiento_ingreso'] / 100) / (1 + tabla['inflacion_acumulada'] / 100))
    tabla_ordenada = tabla.sort_values('ratio_log')

    n_total = len(tabla)
    n_gana_inflacion = int(tabla['gana_inflacion'].sum())
    n_gana_ingreso = n_total - n_gana_inflacion

    colores_barras = tabla_ordenada['ratio_log'].apply(lambda x: '#2ca02c' if x > 0 else '#d62728')

    fig = go.Figure()
    fig.add_trace(go.Bar(x=tabla_ordenada.index, y=tabla_ordenada['ratio_log'], marker_color=colores_barras, showlegend=False))
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color='#2ca02c', name='Gana el ingreso'))
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color='#d62728', name='Gana la inflación'))
    fig.update_layout(
        title=dict(text=f'¿Gana el ingreso o la inflación? Por país, ordenado ({n_total} países, 1980-2024)', font=dict(size=30)),
        yaxis=dict(title='Índice'),
        xaxis=dict(showticklabels=False, title='Países, ordenados de peor a mejor'),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div style="background-color: #eaf2fb; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; font-size: 15px; color: #333;">
    En <b>{n_gana_inflacion} de {n_total} países</b> ({n_gana_inflacion/n_total*100:.0f}%), la inflación acumulada superó el crecimiento del ingreso nominal del Bottom 50% entre 1980 y 2024 - es decir, su poder adquisitivo real cayó. Solo en {n_gana_ingreso} países el ingreso creció más rápido que la inflación.
    </div>
    """, unsafe_allow_html=True)

def mostrar_sintesis():
    mostrar_indicador_parte(3, "Las conclusiones")
    st.header("Matices, no certezas")

    tab_conclusiones, tab_limitaciones, tab_next_steps = st.tabs(["Conclusiones", "Limitaciones", "Next steps"])

    with tab_conclusiones:
        st.markdown("""
        <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">CONCLUSIÓN 01</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">La relación combinada es frágil, pero no cuenta toda la historia</p>
            <p style="font-size: 18px; color: #444; margin: 0;">El Pearson combinado (r=0.484) muestra una asociación positiva moderada, pero el Wild Cluster Bootstrap no logra confirmarla con la confianza estadística habitual (p=0.1165).</p>
        </div>
        <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">CONCLUSIÓN 02</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Por macrorregiónes, la historia es distinta</p>
            <p style="font-size: 18px; color: #444; margin: 0;">El Block Bootstrap muestra que, en 6 de las 8 regiones, la relación sí es estadísticamente significativa - positiva en 4 y negativa en 2. Esta heterogeneidad explica, en parte, por qué el resultado combinado es tan poco concluyente.</p>
        </div>
        <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">CONCLUSIÓN 03</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Sobre la teoría de Piketty</p>
            <p style="font-size: 18px; color: #444; margin: 0;">Con los datos disponibles, no se puede afirmar que la teoría de Piketty se confirme de forma universal - pero tampoco se puede descartar: el mecanismo parece funcionar en la mayoría de las regiones, aunque no siempre en la dirección que predice la teoría. En cualquier caso, incluso si la relación fuera significativa en todas las regiones, una correlación nunca demuestra causalidad.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab_limitaciones:
        st.markdown("""
        <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">LIMITACIÓN 01</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Pocos clusters, poca potencia estadística</p>
            <p style="font-size: 18px; color: #444; margin: 0;">El análisis se basa en solo 8 macrorregiones - es un número reducido de clusters, lo que limita la potencia estadística de la investigación.</p>
        </div>
        <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">LIMITACIÓN 02</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Datos agregados, no experiencias individuales</p>
            <p style="font-size: 18px; color: #444; margin: 0;">El análisis trabaja con datos agregados - escondiendo la diversidad real y las peculiaridades.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab_next_steps:
        st.markdown("""
        <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">PRÓXIMO PASO 01</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Ampliar el análisis: de macrorregiones a países</p>
            <p style="font-size: 18px; color: #444; margin: 0;">Hacer el análisis a nivel de países, en vez de 8 macrorregiones, para comprobar si la teoría se sostiene a una escala más fina.</p>
        </div>
        <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">PRÓXIMO PASO 02</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Modelo predictivo de la desigualdad</p>
            <p style="font-size: 18px; color: #444; margin: 0;">Construir un modelo que proyecte cómo podría evolucionar la desigualdad en los próximos años, a partir de las tendencias observadas.</p>
        </div>
        <div style="background-color: #fffbeb; padding: 25px; border-top: 4px solid #D4AF37; margin-bottom: 20px;">
            <p style="font-size: 14px; letter-spacing: 1px; color: #888; margin-bottom: 10px;">PRÓXIMO PASO 03</p>
            <p style="font-size: 24px; font-weight: bold; margin-bottom: 14px;">Diferencias entre hombres y mujeres</p>
            <p style="font-size: 18px; color: #444; margin: 0;">Investigar si la distribución de riqueza e ingreso difiere entre géneros - una dimensión que este proyecto no ha explorado.</p>
        </div>
        """, unsafe_allow_html=True)

secciones = [mostrar_portada, mostrar_mapa, mostrar_gini, mostrar_distribucion_dolares, mostrar_fotografia, mostrar_intro_piketty, mostrar_ratio, mostrar_capital_trabajo, mostrar_correlacion, mostrar_sintesis, mostrar_gracias]

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
st.markdown("""
<style>
div[data-testid="column"]:nth-of-type(3) div[data-testid="stButton"] {
    display: flex;
    justify-content: flex-end;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    if st.session_state.seccion > 0:
        if st.button("← Anterior"):
            st.session_state.seccion -= 1
            st.rerun()
with col3:
    if st.session_state.seccion < len(secciones) - 1:
        if st.button("Siguiente →"):
            st.session_state.seccion += 1
            st.rerun()

st.divider()

secciones[st.session_state.seccion]()
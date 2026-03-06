
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 15:44:38 2026

@author: OFICINA
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# ==============================
# CONFIGURACIÓN
# ==============================
st.set_page_config(page_title="Dashboard RRHH", layout="wide")
st.title("📊 Dashboard - Analisis de Datos para el departamento de Recursos Humanos")

# ==============================
# CARGA DE DATOS
# ==============================
ruta = r"C:\Users\OFICINA\OneDrive\Escritorio\paython\Dashboard deber\employees.csv"

df = pd.read_csv(ruta)

# Renombrar columnas
df.rename(columns={
    "EMPLOYEE_ID": "ID_EMPLEADO",
    "FIRST_NAME": "NOMBRE",
    "LAST_NAME": "APELLIDO",
    "EMAIL": "EMAIL",
    "PHONE_NUMBER": "TELEFONO",
    "HIRE_DATE": "FECHA_CONTRATACION",
    "JOB_ID": "ID_PUESTO",
    "SALARY": "SALARIO",
    "COMMISSION_PCT": "PORCENTAJE_COMISION",
    "MANAGER_ID": "ID_GERENTE",
    "DEPARTMENT_ID": "ID_DEPARTAMENTO"
}, inplace=True)

# Convertir fecha
df["FECHA_CONTRATACION"] = pd.to_datetime(df["FECHA_CONTRATACION"])

# Calcular antigüedad
hoy = pd.Timestamp.today()
df["ANTIGUEDAD"] = (hoy - df["FECHA_CONTRATACION"]).dt.days / 365

st.success("Archivo cargado correctamente ✅")

# ==============================
# FILTROS SIDEBAR
# ==============================
st.sidebar.header("🔎 Filtros")

departamentos = df["ID_DEPARTAMENTO"].unique()

departamento_seleccionado = st.sidebar.multiselect(
    "Seleccionar Departamento",
    options=departamentos,
    default=departamentos
)

salario_min = int(df["SALARIO"].min())
salario_max = int(df["SALARIO"].max())

rango_salario = st.sidebar.slider(
    "Rango de Salario",
    min_value=salario_min,
    max_value=salario_max,
    value=(salario_min, salario_max)
)

# Aplicar filtros
df_filtrado = df[
    (df["ID_DEPARTAMENTO"].isin(departamento_seleccionado)) &
    (df["SALARIO"] >= rango_salario[0]) &
    (df["SALARIO"] <= rango_salario[1])
]

# ==============================
# KPIs
# ==============================
st.subheader("📌 Indicadores Clave")

col1, col2, col3 = st.columns(3)

total_empleados = df_filtrado.shape[0]
salario_promedio = df_filtrado["SALARIO"].mean()
salario_maximo = df_filtrado["SALARIO"].max()

col1.metric("👥 Total Empleados", total_empleados)
col2.metric("💰 Salario Promedio", f"${salario_promedio:,.2f}")
col3.metric("🏆 Salario Máximo", f"${salario_maximo:,.2f}")

# ==============================
# HISTOGRAMA
# ==============================
st.subheader("📊 Distribución Salarial")

fig1, ax1 = plt.subplots()
ax1.hist(df_filtrado["SALARIO"], bins=10)
ax1.set_xlabel("Salario")
ax1.set_ylabel("Frecuencia")

st.pyplot(fig1)

# ==============================
# BARRAS POR DEPARTAMENTO
# ==============================
st.subheader("📊 Empleados por Departamento")

empleados_por_depto = df_filtrado["ID_DEPARTAMENTO"].value_counts().sort_index()

fig2, ax2 = plt.subplots()
ax2.bar(empleados_por_depto.index.astype(str), empleados_por_depto.values)
ax2.set_xlabel("Departamento")
ax2.set_ylabel("Cantidad")

st.pyplot(fig2)

# ==============================
# SCATTER INTERACTIVO
# ==============================
st.subheader("📊 Antigüedad vs Salario")

fig3 = px.scatter(
    df_filtrado,
    x="ANTIGUEDAD",
    y="SALARIO",
    color="ID_DEPARTAMENTO",
    title="Antigüedad vs Salario por Departamento",
    labels={
        "ANTIGUEDAD": "Antigüedad (años)",
        "SALARIO": "Salario",
        "ID_DEPARTAMENTO": "Departamento"
    }
)

st.plotly_chart(fig3, use_container_width=True)

# ==============================
# TABLA FINAL
# ==============================
st.subheader("📋 Datos Filtrados")
st.dataframe(df_filtrado)

st.subheader("📈 Evolución de Contrataciones por Año")

# Crear columna año
df_filtrado["AÑO"] = df_filtrado["FECHA_CONTRATACION"].dt.year

contrataciones = df_filtrado["AÑO"].value_counts().sort_index()

fig_line = px.line(
    x=contrataciones.index,
    y=contrataciones.values,
    labels={"x": "Año", "y": "Número de Contrataciones"},
    title="Contrataciones por Año"
)

st.plotly_chart(fig_line, use_container_width=True)

st.subheader("📊 Salario Promedio por Departamento")

salario_depto = df_filtrado.groupby("ID_DEPARTAMENTO")["SALARIO"].mean().reset_index()

fig_bar = px.bar(
    salario_depto,
    x="ID_DEPARTAMENTO",
    y="SALARIO",
    title="Salario Promedio por Departamento"
)

st.plotly_chart(fig_bar, use_container_width=True)

st.sidebar.subheader("⏳ Filtro por Antigüedad (años)")

antiguedad_min = int(df["ANTIGUEDAD"].min())
antiguedad_max = int(df["ANTIGUEDAD"].max())

rango_antiguedad = st.sidebar.slider(
    "Seleccionar rango de antigüedad",
    min_value=antiguedad_min,
    max_value=antiguedad_max,
    value=(antiguedad_min, antiguedad_max)
)

df_filtrado = df_filtrado[
    (df_filtrado["ANTIGUEDAD"] >= rango_antiguedad[0]) &
    (df_filtrado["ANTIGUEDAD"] <= rango_antiguedad[1])
]

st.sidebar.subheader("👔 Filtro por Puesto")

puestos = df["ID_PUESTO"].unique()

puesto_seleccionado = st.sidebar.multiselect(
    "Seleccionar Puesto",
    options=puestos,
    default=puestos
)

df_filtrado = df_filtrado[df_filtrado["ID_PUESTO"].isin(puesto_seleccionado)]
    

    
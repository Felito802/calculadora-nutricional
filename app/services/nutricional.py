import pandas as pd
import unicodedata
import re
import os
from rapidfuzz import process


# ===============================
# FUNCION PARA NORMALIZAR TEXTO
# ===============================

def normalizar(texto):

    if pd.isna(texto):
        return ""

    texto = str(texto).lower()

    texto = unicodedata.normalize("NFKD", texto)

    texto = "".join(c for c in texto if not unicodedata.combining(c))

    texto = re.sub(r'[^a-z0-9\s]', '', texto)

    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto


# ===============================
# FUNCION PRINCIPAL
# ===============================

def calcular_tabla_nutricional(ingredientes, gramos):

    # ===============================
    # CARGAR BASE DE DATOS
    # ===============================

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    ruta_excel = os.path.join(BASE_DIR, "database", "Base de datos colombia.xlsx")

    df_b_d = pd.read_excel(ruta_excel)

    # eliminar filas vacías
    df_b_d = df_b_d.dropna(subset=["Nombre del Alimento"])

    # normalizar nombres
    df_b_d["nombre_normalizado"] = df_b_d["Nombre del Alimento"].apply(normalizar)

    lista_base = df_b_d["nombre_normalizado"].tolist()

    # ===============================
    # TABLA INGRESADA POR USUARIO
    # ===============================

    df_u = pd.DataFrame({
        "ingrediente": ingredientes,
        "gramos": gramos
    })

    df_u["ingrediente_norm"] = df_u["ingrediente"].apply(normalizar)

    # ===============================
    # BUSCAR INGREDIENTES
    # ===============================

    filas_encontradas = []
    ingredientes_usados = []

    for ing in df_u["ingrediente_norm"]:

        match = process.extractOne(ing, lista_base)

        if match:

            mejor = match[0]

            fila = df_b_d[df_b_d["nombre_normalizado"] == mejor]
            filas_encontradas.append(fila)
            
            nombre_real = fila["Nombre del Alimento"].values[0]
            ingredientes_usados.append(nombre_real)

    df_encontrados = pd.concat(filas_encontradas)

    df_encontrados.reset_index(drop=True, inplace=True)

    # ===============================
    # CALCULAR PROPORCIONES
    # ===============================

    total_gramos = df_u["gramos"].sum()

    df_u["proporcion"] = (df_u["gramos"] * 100) / total_gramos

    # ===============================
    # NUTRIENTES A CALCULAR
    # ===============================

    nutrientes = [
        "Energia (Kcal)",
        "Grasa total (g)",
        "Grasa Saturada (g)",
        "Grasa trans (mg)",
        "Carbohidratos Totales (g)",
        "Fibra Dietaria (g)",
        "Azúcares totales (g)",
        "Proteina (g)",
        "Sodio (mg)",
        "Vitamina A (ER)",
        "Vitamina D (µg)",
        "Hierro (mg)",
        "Calcio (mg)",
        "Zinc (mg)"
    ]

    resultados = []

    # ===============================
    # CALCULO NUTRICIONAL
    # ===============================

    for nutriente in nutrientes:

        valor_total = 0

        for i in range(len(df_encontrados)):

            valor_db = df_encontrados.iloc[i][nutriente]

            if pd.isna(valor_db):
                valor_db = 0

            peso = df_u.iloc[i]["proporcion"]

            aporte = (valor_db * peso) / 100

            valor_total += aporte

        resultados.append(round(valor_total, 2))

    # ===============================
    # TABLA FINAL
    # ===============================

    tabla = pd.DataFrame({
        "parametro": nutrientes,
        "valor": resultados
    })

    return dict(zip(tabla["parametro"], tabla["valor"])), ingredientes_usados
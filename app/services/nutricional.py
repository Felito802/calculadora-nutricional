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

def calcular_tabla_nutricional(ingredientes, gramos, nombres_azucar):

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

    # ==============================
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
    # ==============================

    total_gramos = df_u["gramos"].sum()
    df_u["proporcion"] = (df_u["gramos"] * 100) / total_gramos
        #  SOLUCIÓN CLAVE: ALINEAR DATAFRAMES
    df_encontrados["ingrediente_norm"] = df_u["ingrediente_norm"].values
    df_encontrados["proporcion"] = df_u["proporcion"].values

    
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

   
    suma_azucares_añadidos = 0

# 🔥 CONVERTIR índices a nombres reales
    # 🔥 SOPORTA índices Y nombres
    nombres_azucar_norm = []
    aportes_azucar = []

    for item in nombres_azucar:

        # Caso 1: viene como índice ("0", "1")
        if str(item).isdigit():
            idx = int(item)
            if idx < len(df_u):
                nombres_azucar_norm.append(df_u.iloc[idx]["ingrediente_norm"])

        # Caso 2: viene como texto ("azucar blanca")
        else:
            nombres_azucar_norm.append(normalizar(item))

    print("AZUCAR FINAL:", nombres_azucar_norm)  # DEBUG
    #print("APORTES AZUCAR:", aportes_azucar)
     # ===============================
    # CALCULO NUTRICIONAL
    # =============================

    for nutriente in nutrientes:

        valor_total = 0

        for _, fila in df_encontrados.iterrows():

            nombre_usuario = fila["ingrediente_norm"]
            peso = fila["proporcion"]

            valor_db = fila[nutriente]

            if pd.isna(valor_db):
                valor_db = 0

            aporte = (valor_db * peso) / 100
            valor_total += aporte

            # 👇 SOLO GUARDAMOS LOS APORTES DE AZÚCAR
            if nutriente == "Azúcares totales (g)":
                aportes_azucar.append((nombre_usuario, aporte))

        resultados.append(round(valor_total, 2))


            # ===============================
            # CALCULO AZÚCARES AÑADIDOS (SEPARADO)
            # ===============================
    suma_azucares_añadidos = 0

    for nombre_usuario, aporte in aportes_azucar:

        if any(az in nombre_usuario for az in nombres_azucar_norm):
            suma_azucares_añadidos += aporte

    print("TOTAL AZUCARES AÑADIDOS:", round(suma_azucares_añadidos, 2))

    # ===============================
    # TABLA FINAL
    # ==============================
    tabla = pd.DataFrame({
        "parametro": nutrientes,
        "valor": resultados
    })

    return dict(zip(tabla["parametro"], tabla["valor"])), ingredientes_usados, suma_azucares_añadidos
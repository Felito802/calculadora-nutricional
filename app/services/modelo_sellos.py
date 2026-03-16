import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from imblearn.under_sampling import RandomUnderSampler


# =========================
# CARGAR DATASET
# =========================

df = pd.read_excel("app/database/Base de datos colombia.xlsx")


# =========================
# LIMPIEZA DE COLUMNAS
# =========================

df = df.drop(columns=[
    'Codigo', 'Nombre del Alimento', 'Parte analizada', 'Cantidad (g)',
    'Humedad (g)', 'Energia (Kj)', 'Lipidos (g)', 'Cenizas (g)',
    'Fosforo (mg)', 'Yodo (mg)', 'Magnesio (mg)', 'Potasio (mg)',
    'Tiamina (mg)', 'Riboflavina (mg)', 'Niacina (mg)', 'Folatos (mcg)',
    'Vitamina B12 (mcg)', 'Vitamina C (mg)', 'Grasa Monoinsaturada (g)',
    'Grasa Poliinsaturada (g)', 'Colesterol (mg)', 'Parte comestible (%)',
    'Sello grasa saturada', 'Sello sodio', 'Sello trans',
    'Carbohidratos disponibles (g)'
], errors="ignore")


# =========================
# LIMPIAR VALORES NULOS
# =========================

df["SGS"] = df["SGS"].fillna(df["SGS"].median())


# =========================
# SEPARAR VARIABLES
# =========================

y = df["SGS"]
X = df.drop(columns=["SGS"])


# =========================
# SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# =========================
# ESCALADO
# =========================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)


# =========================
# BALANCEO
# =========================

rus = RandomUnderSampler(random_state=42)

X_train_res, y_train_res = rus.fit_resample(X_train_scaled, y_train)


# =========================
# MODELO
# =========================

modelo = LogisticRegression(max_iter=1000)

modelo.fit(X_train_res, y_train_res)


# =========================
# FUNCIÓN DE PREDICCIÓN
# =========================

def predecir_sello(nutrientes):

    datos = scaler.transform([nutrientes])

    prob = modelo.predict_proba(datos)[0][1]

    umbral = 0.42

    if prob >= umbral:
        return "EXCESO EN GRASA SATURADA"
    else:
        return "SIN SELLO"
    
print(X.columns)
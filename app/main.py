from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from app.services.modelo_sellos import predecir_sello
from app.services.nutricional import calcular_tabla_nutricional
from app.services.nutricional import calcular_tabla_nutricional, normalizar

app = FastAPI()

# carpeta donde esta el HTML

templates = Jinja2Templates(directory="templates")

# =========================
# PAGINA PRINCIPAL
# =========================
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tabla": None
        }
    )

# =========================
# CALCULAR TABLA
# =========================
@app.post("/calcular")
def calcular(
    request: Request,
    ingrediente: List[str] = Form(...),
    cantidad: List[float] = Form(...),
    azucar_agregado: Optional[List[str]] = Form(None),
    porcion: float = Form(None)
):
   # =========================
    
    #print("Ingredientes:", ingrediente)
    #print("Azucar agregado:", azucar_agregado)
    
# =========================
# =========================
# IDENTIFICAR AZÚCARES AÑADIDOS
# =========================
    nombres_azucar = []
    if azucar_agregado:
    # normalizar directamente los nombres
        nombres_azucar = [normalizar(a) for a in azucar_agregado if a.strip() != '']
    
    tabla, ingredientes_usados, azucares_añadidos = calcular_tabla_nutricional(ingrediente, cantidad, nombres_azucar)
    total_gramos = sum(cantidad)
    if porcion:
        tabla_porcion = {}
        for nutriente, valor in tabla.items():
            tabla_porcion[nutriente] = (valor * porcion) / 100
        porciones = round(total_gramos / porcion, 2)
    else:
        tabla_porcion = tabla
        porciones = "No especificado"
    nutrientes_modelo = [
        tabla["Energia (Kcal)"],
        tabla["Proteina (g)"],
        tabla["Grasa total (g)"],

        tabla["Carbohidratos Totales (g)"],

        tabla["Azúcares totales (g)"],

        tabla["Fibra Dietaria (g)"],

        tabla["Calcio (mg)"],

        tabla["Hierro (mg)"],

        tabla["Sodio (mg)"],

        tabla["Zinc (mg)"],

        tabla["Vitamina A (ER)"],

        tabla["Vitamina D (µg)"],

        tabla["Grasa Saturada (g)"],

        tabla["Grasa trans (mg)"]

    ]

    sello = predecir_sello(nutrientes_modelo)



    return templates.TemplateResponse(

        "index.html",

        {

            "request": request,

            "tabla": tabla,

            "tabla_porcion": tabla_porcion,

            "porcion": porcion,

            "porciones": porciones,

            "sello": sello,

            "ingredientes_usados": ingredientes_usados,

             "azucares_añadidos": azucares_añadidos

        }
    
   

    )
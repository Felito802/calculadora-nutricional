# Calculadora Nutricional con Machine Learning

## Descripción

Este proyecto es una **calculadora nutricional inteligente** que permite al usuario ingresar ingredientes y sus cantidades para generar automáticamente una **tabla nutricional**.

Además, el sistema utiliza **Machine Learning** para predecir si el alimento resultante debe llevar **sello de advertencia por exceso de grasa saturada**.

El sistema calcula los nutrientes a partir de una base de datos de alimentos colombianos y genera una etiqueta nutricional similar a las utilizadas en productos comerciales.

---

## Características principales

* Cálculo automático de **tabla nutricional**
* Predicción de **sello de exceso en grasa saturada**
* Búsqueda inteligente de ingredientes
* Generación de **etiqueta nutricional visual**
* Exportación de la etiqueta a **PDF**

---

## Tecnologías utilizadas

Backend:

* Python
* FastAPI

Machine Learning:

* scikit-learn
* Logistic Regression
* imbalanced-learn

Procesamiento de datos:

* Pandas
* RapidFuzz

Frontend:

* HTML
* CSS
* JavaScript
* Jinja2

Exportación:

* html2pdf.js

---

## Estructura del proyecto

```
calculadora-nutricional
│
├── app
│   ├── main.py
│   ├── services
│   │   ├── nutricional.py
│   │   └── modelo_sellos.py
│   │
│   └── database
│       └── Base de datos colombia.xlsx
│
├── templates
│   └── index.html
│
├── requirements.txt
└── README.md
```

---

## Cómo ejecutar el proyecto

1. Clonar el repositorio

```
git clone https://github.com/Felito802/calculadora-nutricional.git
```

2. Entrar al proyecto

```
cd calculadora-nutricional
```

3. Crear entorno virtual

```
python -m venv venv
```

4. Activar entorno virtual

Windows

```
venv\Scripts\activate
```

5. Instalar dependencias

```
pip install -r requirements.txt
```

6. Ejecutar la aplicación

```
uvicorn app.main:app --reload
```

7. Abrir en el navegador

```
http://127.0.0.1:8000
```

---

## Dataset

El proyecto utiliza una **base de datos de composición de alimentos colombianos**, que contiene información nutricional de más de 800 alimentos.

Los nutrientes utilizados incluyen:

* Energía
* Proteína
* Grasa total
* Grasa saturada
* Carbohidratos
* Azúcares
* Fibra
* Sodio
* Vitaminas y minerales

---

## Autor

Dairo Bolaños
Jailer Olaya
Daniel Lopez

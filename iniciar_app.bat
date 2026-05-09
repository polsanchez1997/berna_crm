@echo off
echo Iniciando Control Estetica Bernardita Driollet...

if not exist entorno (
    python -m venv entorno
)

call entorno\Scripts\activate

pip install -r requisitos.txt

streamlit run aplicacion.py

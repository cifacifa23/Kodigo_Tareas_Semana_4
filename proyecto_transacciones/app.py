# app.py
import json
import os
import streamlit as st
from normalizer import normalize_transaction
from validator import validate_transaction
from metrics import calculate_metrics

# Configuración de la página web
st.set_page_config(
    page_title="Gestión de Transacciones",
    page_icon="💳",
    layout="wide"
)

# Cargar los datos JSON de manera segura
@st.cache_data
def load_data(filename="transactions.json"):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Procesar y normalizar transacciones
def process_transactions():
    raw_data = load_data()
    valid_transactions = []
    invalid_transactions = []

    for raw in raw_data:
        norm = normalize_transaction(raw)
        is_valid, errors = validate_transaction(norm)
        
        if is_valid:
            valid_transactions.append(norm)
        else:
            norm["errors"] = ", ".join(errors)
            invalid_transactions.append(norm)
            
    return valid_transactions, invalid_transactions

valid_txs, invalid_txs = process_transactions()

# --- BARRA LATERAL (MENÚ) ---
st.sidebar.title("Menú de Navegación")
menu = st.sidebar.radio(
    "Selecciona una vista:", 
    ["Métricas Globales", "Transacciones Válidas", "Transacciones Inválidas"]
)

# --- VISTA 1: MÉTRICAS GLOBALES ---
if menu == "Métricas Globales":
    st.title("📊 Panel de Métricas Globales")
    st.markdown("Resumen estadístico del procesamiento de transacciones.")
    
    metrics = calculate_metrics(valid_txs, len(invalid_txs))
    
    # Tarjetas métricas superiores
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Procesadas", metrics["total_processed"])
    col2.metric("Válidas", metrics["valid_count"])
    col3.metric("Inválidas", metrics["invalid_count"])
    
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Conteo por Estado")
        st.json(metrics["status_counts"])
        
    with col_b:
        st.subheader("Totales por Moneda")
        st.json(metrics["currency_totals"])

# --- VISTA 2: TRANSACCIONES VÁLIDAS ---
elif menu == "Transacciones Válidas":
    st.title("✅ Transacciones Válidas y Normalizadas")
    
    # Filtro interactivo por estado
    estado_filtro = st.selectbox(
        "Filtrar por Estado:", 
        ["Todos", "SUCCESS", "FAILED", "PENDING"]
    )
    
    filtered_data = valid_txs
    if estado_filtro != "Todos":
        filtered_data = [t for t in valid_txs if t["status"] == estado_filtro]
        
    if filtered_data:
        st.dataframe(filtered_data, use_container_width=True)
    else:
        st.info("No hay transacciones que coincidan con este filtro.")

# --- VISTA 3: TRANSACCIONES INVÁLIDAS ---
elif menu == "Transacciones Inválidas":
    st.title("⚠️ Transacciones con Errores")
    st.markdown("Registros que no pasaron las reglas de validación.")
    
    if invalid_txs:
        st.dataframe(invalid_txs, use_container_width=True)
    else:
        st.success("¡Excelente! No se encontraron transacciones inválidas en el archivo.")
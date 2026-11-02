# main.py
import json
from normalizer import normalize_transaction
from validator import validate_transaction
from metrics import calculate_metrics

def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    raw_data = load_data("transactions.json")
    if not raw_data:
        print("No se encontró el archivo transactions.json o está vacío.")
        return

    valid_transactions = []
    invalid_transactions = []

    # Proceso de normalización y validación
    for raw in raw_data:
        norm = normalize_transaction(raw)
        is_valid, errors = validate_transaction(norm)
        
        if is_valid:
            valid_transactions.append(norm)
        else:
            norm["errors"] = errors
            invalid_transactions.append(norm)

    # Menú Interactivo CLI
    while True:
        print("\n========================================")
        print("      SISTEMA DE GESTION DE TRANSACCIONES")
        print("========================================")
        print("1. Ver transacciones válidas")
        print("2. Ver transacciones inválidas / con errores")
        print("3. Filtrar transacciones por Estado (SUCCESS/FAILED)")
        print("4. Ver métricas globales")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            print("\n--- TRANSACCIONES VALIDAS ---")
            for t in valid_transactions:
                print(t)
                
        elif opcion == "2":
            print("\n--- TRANSACCIONES INVALIDAS ---")
            for t in invalid_transactions:
                print(f"ID: {t['id']} | Errores: {t['errors']}")
                
        elif opcion == "3":
            estado_input = input("Ingresa el estado a buscar (SUCCESS, FAILED, PENDING): ").upper()
            print(f"\n--- FILTRADO POR ESTADO: {estado_input} ---")
            encontrados = [t for t in valid_transactions if t['status'] == estado_input]
            for t in encontrados:
                print(t)
            if not encontrados:
                print("No se encontraron transacciones con ese estado.")
                
        elif opcion == "4":
            metrics = calculate_metrics(valid_transactions, len(invalid_transactions))
            print("\n--- MÉTRICAS GLOBALES ---")
            print(f"Total procesadas: {metrics['total_processed']}")
            print(f"Válidas: {metrics['valid_count']}")
            print(f"Inválidas: {metrics['invalid_count']}")
            print(f"Conteo por estado: {metrics['status_counts']}")
            print(f"Totales por moneda: {metrics['currency_totals']}")
            
        elif opcion == "5":
            print("\n¡Saliendo del sistema. Éxito con tu entrega!")
            break
        else:
            print("\nOpción no válida. Por favor, elige del 1 al 5.")

if __name__ == "__main__":
    main()
# validator.py

def validate_transaction(tx):
    errors = []
    
    if not tx["id"] or tx["id"] == "None":
        errors.append("ID faltante o inválido")
    
    if not isinstance(tx["amount"], (int, float)) or tx["amount"] <= 0:
        errors.append("Monto inválido o negativo")
        
    if tx["status"] not in ["SUCCESS", "FAILED", "PENDING"]:
        errors.append("Estado no reconocido")
        
    if not tx["timestamp"]:
        errors.append("Fecha inválida")
        
    is_valid = len(errors) == 0
    return is_valid, errors
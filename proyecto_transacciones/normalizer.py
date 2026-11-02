# normalizer.py
from datetime import datetime
from config import STATE_MAPPING

def detect_source(tx):
    if "id" in tx and "timestamp" in tx:
        return "source_1"
    elif "transaction_id" in tx and "created_at" in tx:
        return "source_2"
    elif "ref" in tx and "date" in tx:
        return "source_3"
    return "unknown"

def normalize_transaction(raw_tx):
    source = detect_source(raw_tx)
    normalized = {
        "id": None,
        "amount": 0.0,
        "currency": "USD",
        "timestamp": None,
        "status": "PENDING",
        "source": source
    }
    
    try:
        if source == "source_1":
            normalized["id"] = str(raw_tx.get("id"))
            normalized["amount"] = float(raw_tx.get("amount", 0))
            normalized["currency"] = raw_tx.get("currency", "USD").upper()
            normalized["timestamp"] = raw_tx.get("timestamp")
            raw_status = raw_tx.get("status", "pending")
            normalized["status"] = STATE_MAPPING.get(raw_status, "PENDING")

        elif source == "source_2":
            normalized["id"] = str(raw_tx.get("transaction_id"))
            total_cents = raw_tx.get("total", 0)
            normalized["amount"] = float(total_cents) / 100.0
            normalized["currency"] = raw_tx.get("currency_code", "USD").upper()
            
            dt_str = raw_tx.get("created_at")
            dt_obj = datetime.strptime(dt_str, "%d/%m/%Y %H:%M")
            normalized["timestamp"] = dt_obj.isoformat()
            
            raw_status = raw_tx.get("state", "PEND")
            normalized["status"] = STATE_MAPPING.get(raw_status, "PENDING")

        elif source == "source_3":
            normalized["id"] = str(raw_tx.get("ref"))
            raw_amount = str(raw_tx.get("amount", "0"))
            clean_amount = raw_amount.replace("€", "").replace("$", "").replace(",", ".")
            normalized["amount"] = float(clean_amount)
            normalized["currency"] = "EUR"
            normalized["timestamp"] = raw_tx.get("date")
            
            raw_status = raw_tx.get("result", "pending")
            normalized["status"] = STATE_MAPPING.get(raw_status, "PENDING")
            
    except Exception as e:
        normalized["status"] = "INVALID_PARSE"
        
    return normalized
# metrics.py

def calculate_metrics(valid_txs, invalid_count):
    total_processed = len(valid_txs) + invalid_count
    valid_count = len(valid_txs)
    
    status_counts = {"SUCCESS": 0, "FAILED": 0, "PENDING": 0}
    currency_totals = {}
    
    for tx in valid_txs:
        # Conteo por estado
        st = tx["status"]
        if st in status_counts:
            status_counts[st] += 1
            
        # Totales por moneda
        curr = tx["currency"]
        amt = tx["amount"]
        currency_totals[curr] = currency_totals.get(curr, 0.0) + amt
        
    return {
        "total_processed": total_processed,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "status_counts": status_counts,
        "currency_totals": currency_totals
    }
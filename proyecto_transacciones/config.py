# config.py

STATE_MAPPING = {
    # Fuente 1
    "completed": "SUCCESS",
    "failed": "FAILED",
    "pending": "PENDING",
    # Fuente 2
    "OK": "SUCCESS",
    "ERROR": "FAILED",
    "PEND": "PENDING",
    # Fuente 3
    "success": "SUCCESS",
    "failure": "FAILED"
}

SUPPORTED_CURRENCIES = ["USD", "EUR"]
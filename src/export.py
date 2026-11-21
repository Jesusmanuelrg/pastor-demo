import json
from dataclasses import asdict

from src.payments import Ledger


def payments_json(ledger: Ledger) -> str:
    return json.dumps([asdict(payment) for payment in ledger.payments.values()], indent=1)

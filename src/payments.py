from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional


class PaymentError(Exception):
    pass


@dataclass
class Payment:
    id: str
    customer: str
    amount_cents: int
    currency: str = "EUR"
    refunded_cents: int = 0


@dataclass(frozen=True)
class Refund:
    id: str
    payment_id: str
    amount_cents: int
    currency: str
    created_at: str


@dataclass
class Ledger:
    payments: Dict[str, Payment] = field(default_factory=dict)
    refunds: List[Refund] = field(default_factory=list)

    def add(self, payment: Payment) -> Payment:
        self.payments[payment.id] = payment
        return payment


def refund(ledger: Ledger, payment_id: str, amount_cents: Optional[int] = None) -> Refund:
    """Refund part of a payment, or all that is left when amount_cents is None."""
    payment = ledger.payments.get(payment_id)
    if payment is None:
        raise PaymentError(f"unknown payment {payment_id}")
    left = payment.amount_cents - payment.refunded_cents
    amount = left if amount_cents is None else amount_cents
    if amount <= 0 or amount > left:
        raise PaymentError(f"can refund 1 to {left} cents of {payment_id}, not {amount}")
    payment.refunded_cents += amount
    made = Refund(
        id=f"rf_{len(ledger.refunds) + 1}",
        payment_id=payment_id,
        amount_cents=amount,
        currency=payment.currency,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    ledger.refunds.append(made)
    return made

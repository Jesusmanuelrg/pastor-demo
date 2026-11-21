import json
from dataclasses import asdict, dataclass

from src.export import payments_json
from src.payments import Ledger, PaymentError, refund


@dataclass(frozen=True)
class Response:
    status: int
    content_type: str
    body: str


def _json(status: int, value) -> Response:
    return Response(status, "application/json", json.dumps(value))


def _refund_route(ledger: Ledger, payment_id: str, body: str) -> Response:
    try:
        request = json.loads(body or "{}")
    except ValueError:
        request = None
    amount = request.get("amount_cents") if isinstance(request, dict) else "invalid"
    if amount is not None and (type(amount) is not int):
        return _json(400, {"error": "send a JSON object with an optional integer amount_cents"})
    try:
        made = refund(ledger, payment_id, amount)
    except PaymentError as exc:
        return _json(409, {"error": str(exc)})
    return _json(201, asdict(made))


def handle(ledger: Ledger, method: str, path: str, body: str = "") -> Response:
    parts = path.strip("/").split("/")
    if method == "GET" and parts == ["payments"]:
        return Response(200, "application/json", payments_json(ledger))
    if method == "POST" and len(parts) == 3 and parts[0] == "payments" and parts[2] == "refund":
        return _refund_route(ledger, parts[1], body)
    return _json(404, {"error": f"no route for {method} {path}"})

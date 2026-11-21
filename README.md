# Payments demo

A small payments service that Pastor's demo runs on. It uses only the Python standard library.

- `src/payments.py` keeps payments and refunds in an in-memory `Ledger`. `refund()` records a refund.
- `src/api.py` has the HTTP routes as one `handle()` function: `GET /payments` and `POST /payments/<id>/refund`.
- `src/export.py` turns the ledger into JSON.

The tests use a fresh in-memory `Ledger`. There is no test database. Run them from this folder:

```sh
python3 -m unittest
```

## Open task

Finance wants a refunds CSV export. It needs three parts:

1. A `GET /refunds.csv` endpoint in `src/api.py`.
2. A CSV writer for refunds in `src/export.py`, with a `reason` column.
3. Tests for both, in `tests/test_export.py`.

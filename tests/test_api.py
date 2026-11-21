import json
import unittest

from src.api import handle
from src.payments import Ledger, Payment


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.ledger = Ledger()
        self.ledger.add(Payment("pay_1", "ana", 5000))

    def test_post_refund_returns_the_refund(self):
        response = handle(self.ledger, "POST", "/payments/pay_1/refund", '{"amount_cents": 1200}')
        self.assertEqual(response.status, 201)
        self.assertEqual(json.loads(response.body)["amount_cents"], 1200)

    def test_listing_payments_shows_what_was_refunded(self):
        handle(self.ledger, "POST", "/payments/pay_1/refund", "")
        response = handle(self.ledger, "GET", "/payments")
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(response.body)[0]["refunded_cents"], 5000)

    def test_bad_requests_are_rejected(self):
        self.assertEqual(handle(self.ledger, "POST", "/payments/pay_1/refund", "not json").status, 400)
        self.assertEqual(handle(self.ledger, "POST", "/payments/pay_1/refund", '{"amount_cents": "5"}').status, 400)
        self.assertEqual(handle(self.ledger, "POST", "/payments/pay_1/refund", '{"amount_cents": 9999}').status, 409)
        self.assertEqual(handle(self.ledger, "GET", "/refunds.csv").status, 404)


if __name__ == "__main__":
    unittest.main()

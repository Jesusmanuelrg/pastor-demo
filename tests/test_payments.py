import unittest

from src.payments import Ledger, Payment, PaymentError, refund


class RefundTest(unittest.TestCase):
    def setUp(self):
        self.ledger = Ledger()
        self.ledger.add(Payment("pay_1", "ana", 5000))

    def test_without_an_amount_refunds_what_is_left(self):
        refund(self.ledger, "pay_1", 1500)
        made = refund(self.ledger, "pay_1")
        self.assertEqual(made.amount_cents, 3500)
        self.assertEqual(self.ledger.payments["pay_1"].refunded_cents, 5000)

    def test_each_refund_is_recorded_with_the_payment_currency(self):
        first = refund(self.ledger, "pay_1", 1000)
        second = refund(self.ledger, "pay_1", 2000)
        self.assertEqual(self.ledger.refunds, [first, second])
        self.assertNotEqual(first.id, second.id)
        self.assertEqual(second.currency, "EUR")

    def test_refusing_more_than_is_left_changes_nothing(self):
        refund(self.ledger, "pay_1", 4000)
        with self.assertRaises(PaymentError):
            refund(self.ledger, "pay_1", 1001)
        self.assertEqual(self.ledger.payments["pay_1"].refunded_cents, 4000)
        self.assertEqual(len(self.ledger.refunds), 1)

    def test_zero_and_unknown_payments_are_refused(self):
        with self.assertRaises(PaymentError):
            refund(self.ledger, "pay_1", 0)
        with self.assertRaises(PaymentError):
            refund(self.ledger, "pay_404", 100)


if __name__ == "__main__":
    unittest.main()

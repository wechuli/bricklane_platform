import unittest
from datetime import datetime

from bricklane_platform.models.payment import Payment
from bricklane_platform.models.card import Card


class TestPayment(unittest.TestCase):

    def test_init(self):
        payment = Payment()

        self.assertIsNone(payment.customer_id)
        self.assertIsNone(payment.date)
        self.assertIsNone(payment.amount)
        self.assertIsNone(payment.fee)
        self.assertIsNone(payment.card_id)

    def test_init_with_data(self):

        data = {
            "amount": "2000",
            "card_id": "45",
            "card_status": "processed",
            "customer_id": "123",
            "date": "2019-02-01",
        }

        payment = Payment("card", data)

        self.assertEqual(payment.customer_id, 123)
        self.assertEqual(payment.date, datetime(2019, 2, 1))
        self.assertEqual(payment.amount, 1960)
        self.assertEqual(payment.fee, 40)

        card = payment.card

        self.assertIsInstance(card, Card)
        self.assertEqual(card.card_id, 45)
        self.assertEqual(card.status, "processed")

    def test_is_successful(self):

        data = {
            "amount": "2000",
            "card_id": "45",
            "card_status": "processed",
            "customer_id": "123",
            "date": "2019-02-01",
        }
        payment = Payment("card", data)
        self.assertTrue(payment.is_successful())

    def test_is_successful_declined(self):

        data = {
            "amount": "2000",
            "card_id": "45",
            "card_status": "declined",
            "customer_id": "123",
            "date": "2019-02-01",
        }

        payment = Payment("card", data)

        self.assertFalse(payment.is_successful())

    def test_is_successful_errored(self):

        data = {
            "amount": "2000",
            "card_id": "45",
            "card_status": "errored",
            "customer_id": "123",
            "date": "2019-02-01",
        }

        payment = Payment("card", data)

        self.assertFalse(payment.is_successful())

    def test_is_successful_bank_payment(self):
        data = {
            "amount": "2000",
            "bank_account_id": "12345",
            "customer_id": "123",
            "date": "2019-02-01"
        }
        payment = Payment("bank", data)
        self.assertTrue(payment.is_successful())

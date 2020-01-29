from decimal import Decimal
from dateutil.parser import parse


from bricklane_platform.models.card import Card
from bricklane_platform.models.bank_account import BankAccount
from bricklane_platform.config import PAYMENT_FEE_RATE


class Payment(object):

    customer_id = None
    date = None
    amount = None
    fee = None
    card_id = None
    bank_account_id = None
    payment_successful = False

    def __init__(self, source, data=None):

        if not data:
            return

        self.customer_id = int(data["customer_id"])
        self.date = parse(data["date"])

        total_amount = Decimal(data["amount"])
        self.fee = total_amount * PAYMENT_FEE_RATE
        self.amount = total_amount - self.fee

        if source == "card":
            card = Card()
            card.card_id = int(data["card_id"])
            card.status = data["card_status"]
            self.card = card
            self.payment_successful = self.card.status == "processed"
        elif source == "bank":
            bank_account = BankAccount()
            bank_account.bank_account_id = int(data["bank_account_id"])
            self.bank_account = bank_account
            self.payment_successful = True
        else:
            raise ValueError('Unsupported payment method')

    def is_successful(self):
        return self.payment_successful

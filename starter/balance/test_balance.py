import unittest
from unittest.mock import MagicMock
from balance.balance import Balance
from transaction.transaction import BaseTransaction
from transaction.transaction_category import TransactionCategory
from balance.balance_observer import IBalanceObserver
from datetime import datetime
import uuid


class TestBalance(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_initial_balance(self):
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_singleton_instance(self):
        balance1 = Balance.get_instance()
        balance2 = Balance.get_instance()
        self.assertIs(balance1, balance2)

    def test_add_income(self):
        self.balance.add_income(100)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_add_expense(self):
        self.balance.add_expense(40)
        self.assertEqual(self.balance.get_balance(), -40)

    def test_apply_transaction_income(self):
        t = BaseTransaction(150, TransactionCategory.INCOME)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), 150)
        self.assertEqual(len(self.balance._transactions), 1)

    def test_apply_transaction_expense(self):
        t = BaseTransaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), -60)
        self.assertEqual(len(self.balance._transactions), 1)

    def test_fractional_transaction_amounts(self):
        t = BaseTransaction(100.50, TransactionCategory.INCOME)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), 100.50)

        t = BaseTransaction(27.50, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), 73.00)

    def test_negative_balance_amount(self):
        t = BaseTransaction(100, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), -100)

    def test_transaction_id(self):
        t = BaseTransaction(100, TransactionCategory.INCOME)
        self.assertIsInstance(t._id, uuid.UUID)

    def test_transaction_timestamp(self):
        t = BaseTransaction(100, TransactionCategory.INCOME)
        self.assertIsInstance(t._timestamp, datetime)

    def test_reset(self):
        self.balance.add_income(100)
        self.balance.add_expense(50)
        self.balance.reset()
        self.assertEqual(self.balance.get_balance(), 0.0)
        self.assertEqual(len(self.balance._observers), 0)
        self.assertEqual(len(self.balance._transactions), 0)

    def test_register_observer(self):
        observer = MagicMock(spec=IBalanceObserver)
        self.balance.register_observer(observer)
        self.assertEqual(len(self.balance._observers), 1)

    def test_unregister_observer(self):
        observer = MagicMock(spec=IBalanceObserver)
        self.balance.register_observer(observer)
        self.assertEqual(len(self.balance._observers), 1)
        self.balance.unregister_observer(observer)
        self.assertEqual(len(self.balance._observers), 0)


if __name__ == "__main__":
    unittest.main()

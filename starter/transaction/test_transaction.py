import unittest
from transaction.transaction import BaseTransaction, ValidTransaction
from transaction.transaction_category import TransactionCategory


class TestTransaction(unittest.TestCase):

    def test_transaction_creation(self):
        t = BaseTransaction(100, TransactionCategory.EXPENSE)
        self.assertEqual(t.amount, 100)
        self.assertEqual(t.category, TransactionCategory.EXPENSE)

    def test_transaction_str(self):
        t = BaseTransaction(50, TransactionCategory.INCOME)
        self.assertEqual(
            str(t), "BaseTransaction($50, category='TransactionCategory.INCOME')"
        )

    def test_transaction_equality(self):
        t1 = BaseTransaction(20, TransactionCategory.EXPENSE)
        t2 = BaseTransaction(20, TransactionCategory.EXPENSE)
        t3 = BaseTransaction(30, TransactionCategory.EXPENSE)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)

    def test_valid_transaction(self):
        # Valid transctions
        t = BaseTransaction(100, TransactionCategory.INCOME)
        valid_t = ValidTransaction(t).validate()
        self.assertIsInstance(valid_t, BaseTransaction)

        t = BaseTransaction(100, TransactionCategory.EXPENSE)
        valid_t = ValidTransaction(t).validate()
        self.assertIsInstance(valid_t, BaseTransaction)

    def test_invalid_transaction(self):

        # Invalid transactions
        t = BaseTransaction(-100, TransactionCategory.INCOME)
        with self.assertRaisesRegex(ValueError, "Amount must be positive"):
            ValidTransaction(t).validate()

        t = BaseTransaction(100, "Invalid category")
        with self.assertRaisesRegex(ValueError, "Invalid category"):
            ValidTransaction(t).validate()


if __name__ == "__main__":
    unittest.main()

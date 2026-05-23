import unittest
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction import BaseTransaction
from transaction.transaction_category import TransactionCategory


class TestTransactionAdapter(unittest.TestCase):

    def test_adapter_converts_freelance_income(self):
        ext_txn = ExternalFreelanceIncome(500, "INV-12345", "Website development")
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()
        self.assertEqual(txn, BaseTransaction(500, TransactionCategory.INCOME))

    def test_adapter_fails_with_empty_transaction_type(self):
        ext_txn = ExternalFreelanceIncome(500, "INV-12345", "Website development")
        ext_txn.typ = None
        adapter = TransactionAdapter(ext_txn)
        with self.assertRaises(ValueError):
            adapter.to_transaction()

    def test_adapter_fails_with_unknown_transaction_type(self):
        ext_txn = ExternalFreelanceIncome(500, "INV-12345", "Website development")
        ext_txn.typ = "bonus"
        adapter = TransactionAdapter(ext_txn)

        with self.assertRaises(ValueError):
            adapter.to_transaction()


if __name__ == "__main__":
    unittest.main()

# transaction_adapter.py

from transaction.transaction import BaseTransaction
from transaction.transaction_category import TransactionCategory


class TransactionAdapter:
    def __init__(self, external_transaction):
        self.external_transaction = external_transaction

    def to_transaction(self):
        """Convert an external transaction to a standard BaseTransaction."""

        transaction_type = getattr(self.external_transaction, "typ", None)
        if transaction_type is None:
            raise ValueError(f"Please provide a transaction type")

        if transaction_type.lower() == TransactionCategory.INCOME.value.lower():
            return BaseTransaction(
                self.external_transaction.amount, TransactionCategory.INCOME
            )
        elif transaction_type.lower() == TransactionCategory.EXPENSE.value.lower():
            return BaseTransaction(
                self.external_transaction.amount, TransactionCategory.EXPENSE
            )

# transaction.py
from abc import ABC, abstractmethod
from transaction.transaction_category import TransactionCategory
from datetime import datetime
import uuid


class Transaction(ABC):
    @abstractmethod
    def validate(self):
        pass


class BaseTransaction(Transaction):
    """Represents a financial transaction with an amount and category. Base class for all transactions."""

    def __init__(self, amount, category: TransactionCategory):
        self._id = uuid.uuid4()
        self.amount = amount
        self.category = category
        self._timestamp = datetime.now()

    def __neg__(self):
        if self.category == TransactionCategory.INCOME:
            return BaseTransaction(self.amount, TransactionCategory.EXPENSE)
        elif self.category == TransactionCategory.EXPENSE:
            return BaseTransaction(self.amount, TransactionCategory.INCOME)

    def __str__(self):
        return f"BaseTransaction(${self.amount}, category='{self.category}')"

    def __eq__(self, other):
        return self.amount == other.amount and self.category == other.category

    def validate(self):
        return self


class TransactionDecorator(Transaction):
    def __init__(self, transaction: Transaction):
        self._transaction = transaction

    def validate(self):
        return self._transaction


class ValidTransaction(TransactionDecorator):
    def validate(self):
        if self._transaction.amount < 0:
            raise ValueError("Amount must be positive")
        elif self._transaction.category not in [
            TransactionCategory.INCOME,
            TransactionCategory.EXPENSE,
        ]:
            raise ValueError("Invalid category")
        return self._transaction

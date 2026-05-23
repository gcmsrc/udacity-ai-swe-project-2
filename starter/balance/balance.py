# balance.py

from transaction.transaction_category import TransactionCategory
from transaction.transaction import BaseTransaction, ValidTransaction


class Balance:
    """Singleton to track the balance."""

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, transaction):
        for observer in self._observers:
            observer.update(self.balance, transaction)

    def __init__(self):
        """Initialize the balance. Prevent direct instantiation."""
        self.balance = 0.0
        self._transactions = []
        self._observers = []

    def reset(self):
        """Reset the net balance to zero."""
        self.balance = 0.0
        self._transactions = []
        self._observers = []

    def add_income(self, amount):
        """Add income to the balance."""
        self.balance += amount

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self.balance -= amount

    def apply_transaction(self, transaction):
        """
        Apply a transaction object to update the balance.

        Args:
            transaction (BaseTransaction): The transaction to apply.
        """

        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
        self._transactions.append(transaction)
        self.notify_observers(transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self.balance

    def transactions_statement(self):
        """Return a statement of the transactions."""
        return "\n".join([str(transaction) for transaction in self._transactions])

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Balance: ${self.balance:.2f}"

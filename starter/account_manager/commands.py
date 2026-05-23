from abc import ABC, abstractmethod
from balance.balance import Balance
from transaction.transaction import BaseTransaction
from notification.notification import Notification


# Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class ApplyTransactionCommand(Command):
    def __init__(self, balance: Balance, transaction: BaseTransaction):
        self._balance = balance
        self._transaction = transaction

    def execute(self):
        self._balance.apply_transaction(self._transaction)

    def undo(self):
        # Apply the opposite transaction
        self._balance.apply_transaction(-self._transaction)
        return ApplyTransactionCommand(self._balance, -self._transaction)


class GenerateTransactionStatementsCommand(Command):
    def __init__(self, balance: Balance, delivery_method: Notification):
        self._balance = balance
        self._delivery_method = delivery_method

    def execute(self):
        self._delivery_method.send(
            f"This is the history of your transactions:\n{self._balance.transactions_statement()}"
            + "\n"
            + "Your current balance is: "
            + self._balance.summary(),
        )

    def undo(self):
        return None

import unittest
from unittest.mock import MagicMock
from balance.balance import Balance
from account_manager.account_manager import AccountManager
from account_manager.commands import (
    ApplyTransactionCommand,
    GenerateTransactionStatementsCommand,
)
from transaction.transaction import BaseTransaction
from transaction.transaction_category import TransactionCategory
from notification.notification import Notification


class TestCommands(unittest.TestCase):
    def setUp(self):
        self._balance = Balance.get_instance()
        self._balance.reset()
        self._account_manager = AccountManager()
        self._account_manager.reset()

    def test_apply_transaction_commands(self):
        t1 = BaseTransaction(100, TransactionCategory.INCOME)
        t2 = BaseTransaction(50, TransactionCategory.EXPENSE)

        command1 = ApplyTransactionCommand(self._balance, t1)
        self._account_manager.execute_command(command1)
        command2 = ApplyTransactionCommand(self._balance, t2)
        self._account_manager.execute_command(command2)

        self.assertEqual(self._balance.get_balance(), 50)
        self.assertEqual(len(self._balance._transactions), 2)
        self.assertEqual(len(self._account_manager._commands), 2)

    def test_apply_and_undo_transaction_commands(self):
        t1 = BaseTransaction(100, TransactionCategory.INCOME)
        self._account_manager.execute_command(
            ApplyTransactionCommand(self._balance, t1)
        )
        self.assertEqual(self._balance.get_balance(), 100)
        self.assertEqual(len(self._balance._transactions), 1)
        self.assertEqual(len(self._account_manager._commands), 1)

        # Undo the command
        self._account_manager.undo_last_command()
        self.assertEqual(self._balance.get_balance(), 0)
        self.assertEqual(
            len(self._balance._transactions), 2
        )  # An undo, from a transaction perspetive, is kept in the history
        self.assertEqual(len(self._account_manager._commands), 2)

    def test_apply_and_undo_and_redo_transaction_commands(self):
        t1 = BaseTransaction(100, TransactionCategory.INCOME)
        self._account_manager.execute_command(
            ApplyTransactionCommand(self._balance, t1)
        )
        self.assertEqual(self._balance.get_balance(), 100)
        self.assertEqual(len(self._balance._transactions), 1)
        self.assertEqual(len(self._account_manager._commands), 1)

        # Undo the command
        self._account_manager.undo_last_command()
        self.assertEqual(self._balance.get_balance(), 0)
        self.assertEqual(
            len(self._balance._transactions), 2
        )  # An undo, from a transaction perspetive, is kept in the history
        self.assertEqual(len(self._account_manager._commands), 2)

        # Redo the command
        self._account_manager.undo_last_command()
        self.assertEqual(self._balance.get_balance(), 100)
        self.assertEqual(
            len(self._balance._transactions), 3
        )  # An undo, from a transaction perspetive, is kept in the history
        self.assertEqual(len(self._account_manager._commands), 3)

    def test_generate_transaction_statements_command(self):
        notification = MagicMock(spec=Notification)

        command = GenerateTransactionStatementsCommand(self._balance, notification)
        self._account_manager.execute_command(command)
        self.assertEqual(len(self._account_manager._commands), 1)

    def test_undo_generate_transaction_statements_command(self):
        notification = MagicMock(spec=Notification)

        command = GenerateTransactionStatementsCommand(self._balance, notification)
        self._account_manager.execute_command(command)
        self.assertEqual(len(self._account_manager._commands), 1)

        self._account_manager.undo_last_command()
        self.assertEqual(
            len(self._account_manager._commands), 0
        )  # No new command added

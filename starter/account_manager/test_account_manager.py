import unittest
from unittest.mock import MagicMock
from account_manager.account_manager import (
    AccountManager,
)
from account_manager.commands import Command


class TestAccountManager(unittest.TestCase):

    def setUp(self):
        self.account_manager = AccountManager()

    def test_execute_and_undo_command_if_undo_returns_new_command(self):
        mock_command = MagicMock(spec=Command)

        self.account_manager.execute_command(mock_command)

        mock_command.execute.assert_called_once()
        self.assertEqual(len(self.account_manager._commands), 1)
        self.assertIs(self.account_manager._commands[0], mock_command)

        # Set the undo method to return a Command (in this case, we add a new command to the history)
        mock_command.undo.return_value = Command
        self.account_manager.undo_last_command()
        mock_command.undo.assert_called_once()
        self.assertEqual(len(self.account_manager._commands), 2)

    def test_execute_and_undo_command_if_undo_returns_None(self):
        mock_command = MagicMock(spec=Command)

        self.account_manager.execute_command(mock_command)

        mock_command.execute.assert_called_once()
        self.assertEqual(len(self.account_manager._commands), 1)
        self.assertIs(self.account_manager._commands[0], mock_command)

        # Set the undo method to return None (we add no command to the history)
        mock_command.undo.return_value = None
        self.account_manager.undo_last_command()

        mock_command.undo.assert_called_once()
        self.assertEqual(len(self.account_manager._commands), 0)

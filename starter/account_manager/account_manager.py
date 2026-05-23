# Account manager

from account_manager.commands import Command


class AccountManager:

    def __init__(self):
        self._commands = []

    def execute_command(self, command):
        command.execute()
        self._commands.append(command)

    def undo_last_command(self):
        if self._commands:
            command = self._commands[-1]
            new_command = command.undo()
            if new_command is not None:
                self._commands.append(
                    new_command
                )  # If the undo command does something, then we add the undo
            else:
                self._commands.pop()  # If the undo method returns None, then we drop the command

    def reset(self):
        self._commands = []

"""This module serves as the entry point for the program."""

from account_manager.account_manager import AccountManager
from account_manager.commands import (
    ApplyTransactionCommand,
    GenerateTransactionStatementsCommand,
)
from notification.notification import NotificationFactory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver
from balance.balance_observer import PrintObserver
from transaction.transaction import BaseTransaction, ValidTransaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.external_income_transaction import ExternalFreelanceIncome
from argparse import ArgumentParser

SCENARIOS = {
    "valid": {
        "transactions": [
            BaseTransaction(100, TransactionCategory.INCOME),
            BaseTransaction(50, TransactionCategory.EXPENSE),
            BaseTransaction(200, TransactionCategory.INCOME),
            BaseTransaction(75, TransactionCategory.EXPENSE),
        ],
    },
    "invalid": {
        "transactions": [
            BaseTransaction(100, TransactionCategory.INCOME),
            BaseTransaction(50, TransactionCategory.EXPENSE),
            BaseTransaction(-100, TransactionCategory.EXPENSE),
            BaseTransaction(75, TransactionCategory.EXPENSE),
        ],
    },
    "low_balance": {
        "transactions": [
            BaseTransaction(100, TransactionCategory.INCOME),
            BaseTransaction(80, TransactionCategory.EXPENSE),
            BaseTransaction(200, TransactionCategory.INCOME),
            BaseTransaction(75, TransactionCategory.EXPENSE),
        ],
    },
}


def main(notification_method: str, scenario: str, threshold: float):
    print("Adding transactions...")

    # Preferred notification method
    notification = NotificationFactory.create_notification(notification_method)

    # Create balance and add observers
    manager = AccountManager()
    balance = Balance.get_instance()

    # Add print observer
    balance.register_observer(PrintObserver())

    # LowBalancealertObserver wuld always have at leas SMS notification
    low_balance_alert_notification_methods = set(["sms"] + [notification_method])
    low_balance_alert_notifications = [
        NotificationFactory.create_notification(method)
        for method in low_balance_alert_notification_methods
    ]
    balance.register_observer(
        LowBalanceAlertObserver(low_balance_alert_notifications, threshold)
    )

    # Create standard transactions
    transactions = SCENARIOS[scenario]["transactions"]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    # Apply all transactions to the account manager and, at the end, print
    # the transaction statements

    for transaction in all_transactions:
        command = ApplyTransactionCommand(
            balance, ValidTransaction(transaction).validate()
        )
        manager.execute_command(command)

    # Undo the last transaction as it was a mistake
    manager.undo_last_command()

    command = GenerateTransactionStatementsCommand(
        balance,
        delivery_method=notification,
    )
    manager.execute_command(command)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "--scenario",
        "-s",
        type=str,
        default="valid",
        choices=["valid", "invalid", "low_balance"],
    )
    parser.add_argument(
        "--notification-method",
        "-n",
        type=str,
        default="email",
        choices=["email", "sms", "in_app"],
    )
    parser.add_argument(
        "--threshold",
        "-t",
        type=float,
        default=50.0,
        help="Threshold for low balance alert",
    )
    args = parser.parse_args()

    main(args.notification_method, args.scenario, args.threshold)

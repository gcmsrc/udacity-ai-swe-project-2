import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from transaction.transaction import BaseTransaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver
from notification.notification import Notification


class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_alert_triggers_on_low_balance(self):

        threshold = 50
        expected_message = f"Alert: Balance is below threshold of {threshold}"
        mock_notification_email = MagicMock(spec=Notification)
        mock_notification_sms = MagicMock(spec=Notification)
        observer = LowBalanceAlertObserver(
            notifications=[mock_notification_email, mock_notification_sms], threshold=50
        )

        self.balance.register_observer(observer)

        # Add income
        self.balance.apply_transaction(BaseTransaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        # Add expense that triggers alert
        self.balance.apply_transaction(BaseTransaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)
        mock_notification_email.send.assert_called_with(expected_message)
        mock_notification_sms.send.assert_called_with(expected_message)

        # Add higher income
        self.balance.apply_transaction(BaseTransaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        # Add expense that does not trigger alert
        self.balance.apply_transaction(BaseTransaction(60, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)

        # Add expense that triggers alert
        self.balance.apply_transaction(
            BaseTransaction(200, TransactionCategory.EXPENSE)
        )
        self.assertTrue(observer.alert_triggered)
        mock_notification_email.send.assert_called_with(expected_message)
        mock_notification_sms.send.assert_called_with(expected_message)


class TestPrintObserver(unittest.TestCase):
    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_update_prints_balance_message(self):
        observer = PrintObserver()
        self.balance.register_observer(observer)
        transaction = BaseTransaction(100, TransactionCategory.INCOME)

        with patch("builtins.print") as mock_print:
            self.balance.apply_transaction(transaction)

        mock_print.assert_called_once_with(
            f"{transaction} applied. New balance: {self.balance.get_balance()}"
        )


if __name__ == "__main__":
    unittest.main()

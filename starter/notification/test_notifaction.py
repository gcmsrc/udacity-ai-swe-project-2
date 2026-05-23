import unittest
from unittest.mock import patch
from notification.notification import (
    NotificationFactory,
    EmailNotification,
    SMSNotification,
    InAppNotification,
)


class TestNotification(unittest.TestCase):

    def setUp(self):
        self.notification_factory = NotificationFactory

    def test_email_notification(self):
        notification = self.notification_factory.create_notification("email")
        self.assertIsInstance(notification, EmailNotification)
        with patch("builtins.print") as mock_print:
            notification.send("Hello, world!")
        mock_print.assert_called_once_with(
            "*** E-mail from the Finance Team ***\nDear Customer,\n\nHello, world!\n\nBest regards,\nThe Finance Team\n***"
        )

    def test_sms_notification(self):
        notification = self.notification_factory.create_notification("sms")
        self.assertIsInstance(notification, SMSNotification)
        with patch("builtins.print") as mock_print:
            notification.send("Hello, world!")
        mock_print.assert_called_once_with(
            "*** SMS from the Finance Team ***\nHello, world!\n***"
        )

    def test_in_app_notification(self):
        notification = self.notification_factory.create_notification("in_app")
        self.assertIsInstance(notification, InAppNotification)
        with patch("builtins.print") as mock_print:
            notification.send("Hello, world!")
        mock_print.assert_called_once_with(
            "*** In-App Notification ***\nHello, world!\n***"
        )

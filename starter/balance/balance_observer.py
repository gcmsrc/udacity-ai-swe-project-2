# balance_observer.py
from notification.notification import Notification
from typing import List


class IBalanceObserver:

    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message."""
        print(f"{transaction} applied. New balance: {balance}")


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, notifications: List[Notification], threshold: float = 50.0):
        super().__init__()
        self.threshold = threshold
        self.alert_triggered = False
        self.notifications = notifications

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        if balance < self.threshold:
            self.alert_triggered = True
            for notification in self.notifications:
                notification.send(
                    f"Alert: Balance is below threshold of {self.threshold}"
                )
        else:
            self.alert_triggered = False

class Notification:

    def send(self, message: str):
        pass


class EmailNotification(Notification):
    def send(self, message):
        print(
            f"""*** E-mail from the Finance Team ***
Dear Customer,

{message}

Best regards,
The Finance Team
***"""
        )


class SMSNotification(Notification):
    def send(self, message):
        print(
            f"""*** SMS from the Finance Team ***
{message}
***"""
        )


class InAppNotification(Notification):
    def send(self, message):
        print(
            f"""*** In-App Notification ***
{message}
***"""
        )


class NotificationFactory:

    @staticmethod
    def create_notification(delivery_method: str):
        if delivery_method == "email":
            return EmailNotification()
        elif delivery_method == "sms":
            return SMSNotification()
        elif delivery_method == "in_app":
            return InAppNotification()
        else:
            raise ValueError(f"Invalid delivery method: {delivery_method}")

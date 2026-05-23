# Purpose of this Folder

The repository is structured as follows:

```
starter/
├── main.py
├── README.md
│
├── account_manager/          # Command pattern
│   ├── __init__.py
│   ├── account_manager.py
│   ├── commands.py
│   ├── test_account_manager.py
│   └── test_commands.py
│
├── balance/                  # Singleton + Observer
│   ├── __init__.py
│   ├── balance.py
│   ├── balance_observer.py
│   ├── test_balance.py
│   └── test_balance_observer.py
│
├── notification/             # Factory pattern
│   ├── __init__.py
│   ├── notification.py
│   └── test_notifaction.py
│
└── transaction/              # Adapter + Decorator
    ├── __init__.py
    ├── transaction.py
    ├── transaction_category.py
    ├── transaction_adapter.py
    ├── external_income_transaction.py
    ├── test_transaction.py
    └── test_transaction_adapter.py
```

## Design patterns
## Design Patterns Implemented

This repository demonstrates the use of multiple design patterns:

### Creational Patterns
- **Singleton**  
- **Factory**

#### Singleton Design Pattern
The `Singleton` design pattern is implemented in the `Balance` class.
This ensures that only one instance of the `Balance` class exists throughout the application.
Throughout my impoementaton of the balance class, I have added the following edits:
- the @classmethod `get_instance` is the core of the Singleton design pattern. It ensures that only one instance of the `Balance` class exists throughout the application.
- I have added two attributes to the class: `_transactions` and `_observers`. These are used to store the transactions and observers respectively.

Default behaviours:
* The `Balance` class does not run any validation on the transactions themselves. The task of transaction validation is performed by the `ValidTransaction` class (technically a decorator) in the `transaction` module.
* The `transactions_statement` method returns a string representation of the history of the transactions.
* The `apply_transaction` is actually called by the `ApplyTransactionCommand` class in the `commands` module (Command Design Pattern). Here we assume that a transaction can never be removed from the balance. When "un-doing" a transaction, what we actually do is adding a transaction which is the *negation* of the last one (hence the `__neg__` method in the `BaseTransaction` class).

#### Factor Design Pattern
The `NotificationFactory` class is an example of the Factory design pattern. It is used to create instances of the `Notification` class to handle communications across multiple channels.
The `create_notification` static method is the core of the Factory design pattern. It is used to create instances of the `Notification` class to handle communications across multiple channels.
Each class implements its own `send` method - in our case it is just a different print statement.

### Structural Patterns
- **Adapter**  
- **Decorator**

#### Adapter Design Pattern
The `TransactionAdapter` class acts as the adapter layer between the `BaseTransaction` class and the `ExternalFreelanceIncome` class. The two classes implement a different interface (e.g., a different `init` method in this case). Because our `Balance` class expects a `BaseTransaction` object, we need to adapt the `ExternalFreelanceIncome` object to a `BaseTransaction` object.

I have to admit the starting scenario and instructions were not that "generalisable", but I have implemented something that checks for the `typ` (type) of the extrernal transaction and returns a `BaseTransaction` object with the approriate category (in theory, however, Udacity specified that the external transaction would always be an income transaction so what I implemented may feel a bit redundant).

#### Decorator Design Pattern
I have re-shuffled the `transaction` module quite a bit. Right now we have the following classes:
* `Transaction` abstract class
* `BaseTransaction` class
* `TransactionDecorator` class
* `ValidTransaction` class - the implementation of a dectorator
The `Transaction` class is an abstract class with a single abstract method: `validate`.
The `BaseTransaction` class is a concrete implementation of the `Transaction` abstract class. In particular it has the following constructors:
* `__neg__` method - returns a `BaseTransaction` object with the opposite category (this is useful to do `undo` operations on the balance)
* `__eq__` method - returns True if two `BaseTransaction` objects have the same amount and category
* `validate` method - returns the `BaseTransaction` object itself

The `TransactionDecorator` class is a high-level decorator used to wrap a `Transaction` and implement the `validate` method - by default it returns the wrapped `Transaction` object itself.
The `ValidTransaction` class contains the business logic for validating a transaction. The two condidtions are:
* the amount must be non-negative (the "sign" of the transaction is handled by the category)
* the category must be either `TransactionCategory.INCOME` or `TransactionCategory.EXPENSE`

The `validate` method, if one of the two conditions is not met, raises a `ValueError` with the appropriate message.

As said before, please notice that the `Balance` class does not run any validation on the transactions themselves. The actual validation is performed, for example, within the `main.py` where we create a `Command` for each trasaction on the validated transaction itself.

### Behavioral Patterns
- **Observer**  
- **Command**

#### Observer Design Pattern
The `Balance` class is the subject of the Observer design pattern. It has the following methods:
* `register_observer` - registers an observer to the subject
* `unregister_observer` - unregisters an observer from the subject
* `notify_observers` - notifies all observers of a change

The `IBalanceObserver` interface is the observer interface with a single method: `update`.
We have two concrete implementations:
* `PrintObserver` - prints the new balance and transaction
* `LowBalanceAlertObserver` - alerts the user if the balance is below a certain threshold

Every time the `apply_transaction` method is called, the `notify_observers` method is called to notify all observers of the change. This is a for-loop where each observer receives the transaction (and the balance amount) and runs its own `update` method.

#### Command Design Pattern
Here I decided to implement an `AccountManager` class that could somehow simulate a sort of UI where entitled users could execute commands on the balance.
The `AccountManager` is structured as follows:
1. It contains a history of commands executed
2. I has a method to execute a command
3. It has a method to undo the last command
4. It has `reset` method to reset the history of commands

The `Command` abstract class is defined in `commands.py` - it has two abstract methods: `execute` and `undo`.
We then have two concrete implementations:
* `ApplyTransactionCommand` - applies a transaction to the balance
* `GenerateTransactionStatementsCommand` - generates a transaction statements and sends it to the user

The `ApplyTransactionCommand` class is peculiar. The execution of a command would simply call the `apply_transaction` method on the balance. But the `undo` method does the following:
1. Apply the negation of the transaction
2. Return a new `ApplyTransactionCommand` itself

The second step is important because it allows to "undo the undo" (i.e. a re-do) by (re-)negating the negation of the transaction.

The `GenerateTransactionStatementsCommand` class is a simple command that generates a transaction statements and sends it to the user. The `undo` method returns `None` because we cannot undo a transaction statements. But shiuw would pop the latest commands from the `_commands` history in the `AccountManager` class otherwise, if that was not the case, we would never be able to undo the command and we would be stuck with the last command in the history.

## Local test in `main.py`
You can use the `main.py` to test the application. You can specify three parameters:
* `notification_method` - the method to use for notifications (e.g., `email`, `sms`, `print`)
* `scenario` - the scenario to test (e.g., `basic`, `advanced`)
* `threshold` - the threshold for the low balance alert

The `notification_method` specify the method to use for notifications (e.g., `email`, `sms`, `print`). For situations where the balance goes below a certain threshold, independently of the `notification_method` used, the `LowBalanceAlertObserver` will always send an SMS notification.

The `scenario` specifies the scenario to test (e.g., `valid`, `invalid`, `low_balance`).

Let us look at the `valid` scenario. In this scenario, we have the following transactions:
* 100 income
* 50 expense
* 200 income
* 75 expense

The `valid` scenario is the default scenario.
To run the `valid` scenario, you can use the following command:

```
python main.py --scenario valid
```

The `main.py` does the following:
1. Instantiate an `AccountManager` class
2. Register the two observers (`PrintObserver` and `LowBalanceAlertObserver`)
3. Pull the `transactions` from the `SCENARIOS` dictionary (using the `scenario` parameter)
4. Create an external income transaction (via Adapter pattern)
5. Create the `ApplyTransactionCommand` for each transaction - better, a `validated` transaction - and ask the `AccountManager` to execute it
6. Undo the last transaction (the External Income transaction)
7. Generate a transaction statements and send it to the user

The `main.py` is the entry point of the application. It is used to test the application.
This is the outcome you should see:

```
Adding transactions...
BaseTransaction($100, category='TransactionCategory.INCOME') applied. New balance: 100.0
BaseTransaction($50, category='TransactionCategory.EXPENSE') applied. New balance: 50.0
BaseTransaction($200, category='TransactionCategory.INCOME') applied. New balance: 250.0
BaseTransaction($75, category='TransactionCategory.EXPENSE') applied. New balance: 175.0
BaseTransaction($1200, category='TransactionCategory.INCOME') applied. New balance: 1375.0
BaseTransaction($1200, category='TransactionCategory.EXPENSE') applied. New balance: 175.0
*** E-mail from the Finance Team ***
Dear Customer,

This is the history of your transactions:
BaseTransaction($100, category='TransactionCategory.INCOME')
BaseTransaction($50, category='TransactionCategory.EXPENSE')
BaseTransaction($200, category='TransactionCategory.INCOME')
BaseTransaction($75, category='TransactionCategory.EXPENSE')
BaseTransaction($1200, category='TransactionCategory.INCOME')
BaseTransaction($1200, category='TransactionCategory.EXPENSE')
Your current balance is: Balance: $175.00

Best regards,
The Finance Team
***
```
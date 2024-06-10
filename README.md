# Logical View of the 4+1 Model for a Banking Application

```mermaid
classDiagram
    class Customer {
        +String name
        +String address
        +String email
        +createAccount()
        +login()
    }

    class Account {
        +int accountNumber
        +double balance
        +deposit(amount: double)
        +withdraw(amount: double)
        +getBalance() double
    }

    class Transaction {
        +int transactionId
        +Date date
        +double amount
        +String type
        +execute()
    }

    class Bank {
        +String name
        +List~Customer~ customers
        +List~Account~ accounts
        +createCustomer(name: String, address: String, email: String) Customer
        +createAccount(customer: Customer) Account
        +getCustomerDetails(customerId: int) Customer
        +getAccountDetails(accountNumber: int) Account
    }

    Customer --> Account : creates
    Customer --> Transaction : initiates
    Account --> Transaction : records
    Bank --> Customer : manages
    Bank --> Account : manages
    Bank --> Transaction : oversees

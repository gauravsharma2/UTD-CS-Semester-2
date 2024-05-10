package org.example.presentation;

/*
public class Account {
    private String accountId;
    private boolean isActive;

    public Account(String accountId, boolean isActive) {
        this.accountId = accountId;
        this.isActive = isActive;
    }

    public boolean isActive() {
        return isActive;
    }

    public static void main(String[] args) {
        Account account = new Account("AC123", true);
        if (account.isActive()) {
            System.out.println("Account is active");
        } else {
            System.out.println("Account is inactive");
        }
    }
}
*/


// Primitive Obsession Example
//In this example, we're using a boolean type (isActive) to represent the status of an account (active or inactive).
//While this code works, it demonstrates primitive obsession because using a boolean for status flags can lead to unclear code and
//limited expressiveness, especially when dealing with more than two states (e.g., active, inactive, suspended).

// Parameter Object Example
//In this updated example, we've introduced an AccountStatus class as a Parameter Object to represent the status of an account.
// This allows us to use enums to define different states (e.g., active, inactive, suspended) and provides a more expressive and maintainable way to handle account statuses.

//By using Parameter Objects, we've addressed the issues related to primitive obsession by encapsulating related parameters into dedicated classes, which leads to more readable,
// maintainable, and flexible code.

class AccountStatus {
    public enum Status {
        ACTIVE, INACTIVE, SUSPENDED
    }

    private Status status;

    public AccountStatus(Status status) {
        this.status = status;
    }

    // Getter for status
    public Status getStatus() {
        return status;
    }
}

public class Account {
    private String accountId;
    private AccountStatus accountStatus; // Using Parameter Object for status

    public Account(String accountId, AccountStatus accountStatus) {
        this.accountId = accountId;
        this.accountStatus = accountStatus;
    }

    public AccountStatus getAccountStatus() {
        return accountStatus;
    }

    // Getters and setters omitted for brevity

    public static void main(String[] args) {
        AccountStatus status = new AccountStatus(AccountStatus.Status.SUSPENDED);
        Account account = new Account("AC123", status);

        if (account.getAccountStatus().getStatus() == AccountStatus.Status.SUSPENDED) {
            System.out.println("Account is Suspended");
        } else {
            System.out.println("Account is inactive");
        }
    }
}





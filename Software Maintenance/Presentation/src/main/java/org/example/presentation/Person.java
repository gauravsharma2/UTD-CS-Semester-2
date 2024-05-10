package org.example.presentation;
/*
public class Person {
    private int age; // Primitive obsession: using int for age

    public Person(int age) {
        this.age = age;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public static void main(String[] args) {
        // Creating a person instance with primitive obsession
        Person person = new Person(25);

        // Printing the person's age
        System.out.println("Person's age: " + person.getAge());

        // Modifying the age directly (primitive obsession)
        person.setAge(-30);
        System.out.println("Updated age: " + person.getAge());
    }
}
*/

//While adding age validation in the constructor can help ensure that invalid age values are not set during object creation,
// there are several reasons why using a Parameter Object might still be beneficial:
//Single Responsibility Principle (SRP): By separating concerns, a Parameter Object allows the Person class to focus solely on representing a person's data
// (including age) without the additional responsibility of validation logic.
//Reusability: A Parameter Object like Age could be reused in other classes or contexts where age validation is required, promoting code reusability and
// avoiding duplication of validation logic.
//Encapsulation: Using a dedicated Age class allows you to encapsulate age-related behavior and validation rules within that class, improving code organization and readability.
//Flexibility: If age validation rules change in the future (e.g., minimum age requirement changes), modifying the validation logic within the Age class
// would not require changes to the Person class, promoting code maintenance and flexibility.

public class Person {
    private Age age;

    public Person(Age age) {
        this.age = age;
    }

    public Age getAge() {
        return age;
    }

    public void setAge(Age age) {
        if (isValidAge(age)) {
            this.age = age;
        } else {
            throw new IllegalArgumentException("Invalid age value");
        }
    }

    private boolean isValidAge(Age age) {
        return age != null && age.getValue() >= 0 && age.getValue() <= 150; // Assuming a reasonable age range
    }

    public static void main(String[] args) {
        // Valid age value
        Age validAge = new Age(25);
        Person person = new Person(validAge);
        System.out.println("Person's age: " + person.getAge().getValue());

        // Invalid age value (negative age)
        try {
            Age invalidAge = new Age(-5);
            person.setAge(invalidAge); // This should throw an IllegalArgumentException
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }

        // Invalid age value (age outside reasonable range)
        try {
            Age invalidAge = new Age(300);
            person.setAge(invalidAge); // This should throw an IllegalArgumentException
            System.out.println("Person's age: " + person.getAge().getValue());
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}

class Age {
    private int value;

    public Age(int value) {
        if (value < 0 || value > 150) { // Assuming a reasonable age range
            throw new IllegalArgumentException("Invalid age value");
        }
        this.value = value;
    }

    public int getValue() {
        return value;
    }
}





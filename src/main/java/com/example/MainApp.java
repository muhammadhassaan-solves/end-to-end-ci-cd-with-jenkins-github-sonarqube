package com.example;

public class MainApp {
    private static final String PASSWORD = "12345"; // Hardcoded password (Security issue)

    public static void main(String[] args) {
        System.out.println("Hello, This is end-to-end-ci-cd-with-jenkins-github-sonarqube!");

        int unusedVar = 42; // Unused variable (Code smell)
        int result = 10 / 0; // Division by zero (Bug)
    }
}

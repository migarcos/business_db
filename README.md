# Overview

Repetition is the mother of skill. This time, I'll use Python and SQLite3 to simulate human resource management within a company. The database schema will likely change depending on the growth needs of a real business.

I'll start by managing employees and departments. Later, I will add projects and job titles or positions (with their respective salary ranges).


[Software Demo Video](https://youtu.be/4FnHwycCOEk?si=pizuA41kvlGuG7OG)

# Relational Database

Employee  N  <-------- 1  departements

Employee Table
employee_id PK, fname, lname, email, hire_date, status, salary, department_id FK

Department Table
deparment_id PK, department_name, department_code

## Future tables 
Level (to calculate position salary)
Project 
Employee_Story (to track positions and salaries)


# Development Environment

The application will operate as a CLI, using Python and SQLite3 as programming languages. It will begin by using DDL (Data Definition Language) to create and modify the table structure. The goal is to create an environment that allows CRUD (Create, Read, Update, Delete) operations using DML (Data Manipulation Language), ultimately generating the necessary reports using DQL (Data Query Language) commands.

# Useful Websites

* [SQLite3 & Python](https://docs.python.org/3/library/sqlite3.html)
* [ORACLE Relational DB](https://www.oracle.com/database/what-is-a-relational-database/)
* [Wikipedia SQL](https://en.wikipedia.org/wiki/SQL)
* [SQLite site](https://www.sqlite.org/index.html)


[Markdown Language Cheatsheet](https://www.markdownguide.org/cheat-sheet/)
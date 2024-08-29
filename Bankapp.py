# This project was created as part of a learning exercise and for practice purposes.
# Make sure you have installed XAMPP in your system, as it are required for the code to work.

import os
import mysql.connector
from datetime import date

# Start XAMPP services (MySQL and Apache)
print("Starting XAMPP...\n")
os.system(r'C:\\xampp\\xampp_start.exe')

# Connect to MySQL server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = mydb.cursor()

# Create the 'bank_account' database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS bank_account;")

# Now connect to the 'bank_account' database
mydb.database = 'bank_account'

# Create the 'userdetails' table if it doesn't already exist
# This table stores the list of usernames, passwords, and balances for users.
sql="CREATE TABLE IF NOT EXISTS userdetails(username VARCHAR(20), password VARCHAR(20), balance FLOAT);"
cursor.execute(sql)


# Function to deposit an amount into a user's account
def deposit(username, amount):
    # Update the user's balance by adding the deposit amount
    sql = "UPDATE userdetails SET BALANCE = BALANCE + %s WHERE username = '%s';" % (amount, username)
    cursor.execute(sql)
    
    # Retrieve the updated balance
    sql = "SELECT BALANCE FROM userdetails WHERE username = '%s';" % (username)
    cursor.execute(sql)
    row = cursor.fetchone()
    balance = row[0]
    
    # Determine the next serial number for the transaction record
    sql = "SELECT SLNO FROM " + username + " ORDER BY SLNO DESC LIMIT 1;"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is None:
        sl = 1
    else:
        sl = row[0] + 1
    cdate = str(date.today().strftime('%d-%m-%Y'))
    
    # Insert the deposit transaction into the user's transaction table
    sql = "INSERT INTO " + username + " (SLNO, CDate, WITHDRAWAL, DEPOSIT, BALANCE) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (sl, cdate, 0.00, amount, balance))
    
    print("Rs.", amount, "Deposited Successfully")
    mydb.commit()

# Function to withdraw an amount from a user's account
def withdraw(username, amount):
    # Retrieve the current balance
    sql = "SELECT BALANCE FROM userdetails WHERE username = '%s';" % (username)
    cursor.execute(sql)
    row = cursor.fetchone()
    balance = row[0]
    
    # Check if there is sufficient balance for the withdrawal
    if balance < amount:
        print("Insufficient Balance")
    else:
        # Update the balance by subtracting the withdrawal amount
        sql = "UPDATE userdetails SET BALANCE = BALANCE - %s WHERE username = '%s';" % (amount, username)
        cursor.execute(sql)
        balance -= amount
        
        # Determine the next serial number for the transaction record
        sql = "SELECT SLNO FROM " + username + " ORDER BY SLNO DESC LIMIT 1;"
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is None:
            print("Insufficient Balance")
        else:
            sl = row[0] + 1
        
        cdate = str(date.today().strftime('%d-%m-%Y'))
        
        # Insert the withdrawal transaction into the user's transaction table
        sql = "INSERT INTO " + username + " (SLNO, CDate, WITHDRAWAL, DEPOSIT, BALANCE) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (sl, cdate, amount, 0.00, balance))
        
        print("Rs.", amount, "Withdrawn Successfully")
        mydb.commit()

# Function to check the balance of a user's account
def checkbalance(username):
    sql = "SELECT BALANCE FROM userdetails WHERE username = '%s';" % (username)
    cursor.execute(sql)
    row = cursor.fetchone()
    balance = row[0]
    print("Your current balance is: Rs.", balance)

# Function to display the transaction history (passbook)
def passbook(username):
    sql = "SELECT * FROM " + username + ";"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        print("Slno\tDate\tWithdraw\tDeposit\tBalance")
        print("**********************************************")
        for row in result:
            print(row[0], "\t", row[1], "\t", row[2], "\t", row[3], "\t", row[4])
    else:
        print("No transaction yet..")

# Function to handle user operations
def operation():
    while True:
        print("\nWELCOME")
        print("1.Deposit\n2.Withdraw\n3.Check Balance\n4.e-Passbook\n5.Delete Account\n6.Exit")
        choice = int(input("Please choose any option:"))
        
        if choice == 1:
            amount = float(input("Enter the amount to be deposited: "))
            deposit(username, amount)
        elif choice == 2:
            amount = float(input("Enter the Withdraw amount: "))
            withdraw(username, amount)
        elif choice == 3:
            checkbalance(username)
        elif choice == 4:
            passbook(username)
        elif choice == 5:
            dlt = input("Are you sure you want to delete Account?\nEnter 'Y' if yes otherwise press 'N': ")
            if dlt in ["Y", "y"]:
                # Drop the user's transaction table and delete the user from the userdetails table
                sql = f"DROP TABLE IF EXISTS {username};"
                cursor.execute(sql)
                sql = "DELETE FROM userdetails WHERE username = '%s';" % (username)
                cursor.execute(sql)
                mydb.commit()
                print("Account Deleted Successfully")
                break
            elif dlt in ["N", "n"]:
                operation()
        elif choice == 6:
            exit(0)
        else:
            print("Invalid Input")

# Main loop for user sign-in and login
try:
    while True:
        try:
            print("\n1.SignIn\n2.LogIn\n3.Exit")
            userstatus = int(input("Enter your choice: "))
    
            if userstatus == 1:
                username = input("Enter your Username: ").strip()
                if not username:
                    print("Username cannot be empty, Please enter valid username")
                    continue

                sql = "SELECT * FROM userdetails WHERE username = '%s';" % (username)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    print("Username already exists")
                else:
                    password = input("Enter the password: ").strip()
                    if not password:
                        print("Password cannot be empty, Please enter valid password")
                    sql = "INSERT INTO userdetails (username, password, BALANCE) VALUES ('%s', '%s', %d);" % (username, password, 0)
                    cursor.execute(sql)
                    sql = "CREATE TABLE " + username + " (SLNO INT, CDate VARCHAR(20), WITHDRAWAL FLOAT, DEPOSIT FLOAT, BALANCE FLOAT);"
                    cursor.execute(sql)
                    operation()

            elif userstatus == 2:
                username = input("Enter your Username: ").strip()
                if not username:
                    print("Username cannot be empty, Please enter valid username")
                    continue
                sql = "SELECT * FROM userdetails WHERE username = '%s';" % (username)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    password = input("Enter the password: ").strip()
                    if not password:
                        print("Password cannot be empty, Please enter valid password")
                    sql = "SELECT password FROM userdetails WHERE username = '%s';" % (username)
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    if row[0] == password:
                        operation()
                    else:
                        print("Wrong Password")
                else:
                    print("User Doesn't exist")

            elif userstatus == 3:
                print("Thank you for using our bank!!")
                break
            else:
                print("Invalid choice")

        except Exception:
            print("Please Enter valid entry")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the database connection
    mydb.close()
    
    # Stop XAMPP services (MySQL and Apache)
    os.system(r'C:\\xampp\\xampp_stop.exe')

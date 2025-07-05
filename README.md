# 🏦 Simple CLI Banking System (Python + MySQL)

This project is a **Command-Line Banking System** built using **Python** and **MySQL**, designed for learning and practice purposes. It allows users to create accounts, deposit and withdraw money, check balances, view an e-passbook (transaction history), and delete accounts.

The system connects to a **MySQL server via XAMPP**, so make sure XAMPP is installed and running.

---

## 📦 Features

- ✅ Sign Up and Login system
- 💰 Deposit & Withdraw money
- 📄 e-Passbook (transaction history)
- 📊 Balance check
- ❌ Account deletion
- 🛠️ Starts and stops XAMPP services automatically
- 🗃️ Stores data in MySQL (`bank_account` database)

---

## 🧰 Requirements

- Python 3.x
- MySQL (via XAMPP)
- `mysql-connector-python`  
  Install via pip:  
  ```
  pip install mysql-connector-python
  ```

---

## 🚀 How to Run

1. ✅ Install **[XAMPP](https://www.apachefriends.org/index.html)** and start **MySQL** and **Apache** manually once (or let the script auto-start them).
2. 📁 Save the Python file anywhere on your system.
3. ▶️ Run the script:
   ```bash
   python bank_system.py
   ```

The script will:
- Start XAMPP services
- Connect to MySQL
- Create a database `bank_account` (if not exists)
- Allow user interaction via terminal

---

## 🗃️ Database Structure

### 📁 Database: `bank_account`

#### Table: `userdetails`

| Column   | Type         | Description                 |
|----------|--------------|-----------------------------|
| username | VARCHAR(20)  | Primary key (login ID)      |
| password | VARCHAR(20)  | User password (plaintext)   |
| balance  | FLOAT        | Current account balance     |

#### Per-user transaction table  
Each user has a dedicated table created using their username. Example: `john123`

| Column     | Type        | Description                 |
|------------|-------------|-----------------------------|
| SLNO       | INT         | Serial number (auto count)  |
| CDate      | VARCHAR(20) | Date of transaction         |
| WITHDRAWAL | FLOAT       | Amount withdrawn            |
| DEPOSIT    | FLOAT       | Amount deposited            |
| BALANCE    | FLOAT       | Account balance after txn   |

---

## ⚠️ Notes

- ❗ This project is for **learning purposes only**.
- ❗ Passwords are stored as **plaintext** (not secure).
- ⚙️ The script uses `os.system()` to control XAMPP (`xampp_start.exe`, `xampp_stop.exe`) — make sure the paths are correct and you’re using Windows.

---

## 👨‍💻 Author

- A.U Yashas 
 yashas.a.u@gmail.com

---

## 📜 License

This project is licensed for personal and educational use only. Not recommended for production environments.

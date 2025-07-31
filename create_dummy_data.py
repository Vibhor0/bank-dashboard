import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
faker = Faker()

# Connect to SQLite database
conn = sqlite3.connect("bank_data.db")
cursor = conn.cursor()

# Drop tables if they already exist (for rerun purposes)
cursor.execute("DROP TABLE IF EXISTS BankStatement")
cursor.execute("DROP TABLE IF EXISTS BankAccount")
cursor.execute("DROP TABLE IF EXISTS Company")
cursor.execute("DROP TABLE IF EXISTS Client")

# Create tables
cursor.execute("""
CREATE TABLE Client (
    client_id INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT,
    contact_email TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE Company (
    company_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    name TEXT,
    industry TEXT,
    FOREIGN KEY (client_id) REFERENCES Client(client_id)
)
""")

cursor.execute("""
CREATE TABLE BankAccount (
    account_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    bank_name TEXT,
    ifsc_code TEXT,
    account_number TEXT,
    account_type TEXT,
    FOREIGN KEY (company_id) REFERENCES Company(company_id)
)
""")

cursor.execute("""
CREATE TABLE BankStatement (
    entry_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    date TEXT,
    amount REAL,
    type TEXT,
    description TEXT,
    FOREIGN KEY (account_id) REFERENCES BankAccount(account_id)
)
""")

# Insert Dummy Data
client_count = 25
for i in range(client_count):
    name = faker.name()
    address = faker.address().replace('\n', ', ')
    email = faker.email()
    phone = faker.phone_number()
    cursor.execute("INSERT INTO Client (name, address, contact_email, phone) VALUES (?, ?, ?, ?)",
                   (name, address, email, phone))
    client_id = cursor.lastrowid

    for j in range(random.randint(1, 3)):  # 1 to 3 companies per client
        company_name = faker.company()
        industry = random.choice(["Finance", "Tech", "Retail", "Logistics", "Healthcare"])
        cursor.execute("INSERT INTO Company (client_id, name, industry) VALUES (?, ?, ?)",
                       (client_id, company_name, industry))
        company_id = cursor.lastrowid

        for k in range(random.randint(2, 4)):  # 2 to 4 bank accounts per company
            bank_name = random.choice(["HDFC", "ICICI", "SBI", "Axis", "Kotak"])
            ifsc = faker.bothify(text='????0#####')
            acc_num = faker.bban()
            acc_type = random.choice(["Savings", "Current"])
            cursor.execute("INSERT INTO BankAccount (company_id, bank_name, ifsc_code, account_number, account_type) VALUES (?, ?, ?, ?, ?)",
                           (company_id, bank_name, ifsc, acc_num, acc_type))
            account_id = cursor.lastrowid

            for l in range(random.randint(20, 50)):  # 20 to 50 transactions
                trans_date = faker.date_between(start_date='-1y', end_date='today').isoformat()
                amount = round(random.uniform(100.0, 50000.0), 2)
                trans_type = random.choice(["Credit", "Debit"])
                desc = faker.sentence(nb_words=5)
                cursor.execute("INSERT INTO BankStatement (account_id, date, amount, type, description) VALUES (?, ?, ?, ?, ?)",
                               (account_id, trans_date, amount, trans_type, desc))

# Commit and close connection
conn.commit()
conn.close()

print("✅ Dummy data successfully created in bank_data.db")

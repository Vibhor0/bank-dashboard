import csv
from faker import Faker
import random
from datetime import datetime, timedelta

faker = Faker()

clients = []
companies = []
bank_accounts = []
bank_statements = []

client_count = 25
client_id_counter = 1
company_id_counter = 1
account_id_counter = 1
entry_id_counter = 1

for _ in range(client_count):
    client_id = client_id_counter
    clients.append([
        client_id,
        faker.name(),
        faker.address().replace('\n', ', '),
        faker.email(),
        faker.phone_number()
    ])
    client_id_counter += 1

    for _ in range(random.randint(1, 3)):  # 1 to 3 companies per client
        company_id = company_id_counter
        companies.append([
            company_id,
            client_id,
            faker.company(),
            random.choice(["Finance", "Tech", "Retail", "Logistics", "Healthcare"])
        ])
        company_id_counter += 1

        for _ in range(random.randint(2, 4)):  # 2 to 4 accounts per company
            account_id = account_id_counter
            bank_accounts.append([
                account_id,
                company_id,
                random.choice(["HDFC", "ICICI", "SBI", "Axis", "Kotak"]),
                faker.bothify(text='????0#####'),
                faker.bban(),
                random.choice(["Savings", "Current"])
            ])
            account_id_counter += 1

            for _ in range(random.randint(20, 50)):  # Transactions
                bank_statements.append([
                    entry_id_counter,
                    account_id,
                    faker.date_between(start_date='-1y', end_date='today').isoformat(),
                    round(random.uniform(100.0, 50000.0), 2),
                    random.choice(["Credit", "Debit"]),
                    faker.sentence(nb_words=5)
                ])
                entry_id_counter += 1

# Write CSV files
with open('Client.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["client_id", "name", "address", "contact_email", "phone"])
    writer.writerows(clients)

with open('Company.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["company_id", "client_id", "name", "industry"])
    writer.writerows(companies)

with open('BankAccount.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["account_id", "company_id", "bank_name", "ifsc_code", "account_number", "account_type"])
    writer.writerows(bank_accounts)

with open('BankStatement.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["entry_id", "account_id", "date", "amount", "type", "description"])
    writer.writerows(bank_statements)

print("✅ Dummy data saved as CSV files: Client.csv, Company.csv, BankAccount.csv, BankStatement.csv")

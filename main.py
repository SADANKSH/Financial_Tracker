import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description

class CSV:
    CSV_FILE="finance_data.csv"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        with open(cls.CSV_FILE, mode='a', newline='') as csv_file:
            fieldnames = ['Date', 'Amount', 'Category', 'Description']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(new_entry)
        print("Entry added successfully")

def add():
    CSV.initialize_csv()
    date = get_date("Enter date of Transaction(DD-MM-YYYY) or Enter Today: ",allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


add()

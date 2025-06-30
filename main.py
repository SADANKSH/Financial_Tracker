import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt

from data_entry import get_date, get_amount, get_category, get_description


class CSV:
    CSV_FILE = "finance_data.csv"
    FORMAT = "%d-%m-%Y"

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

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found between the given dates")
            return None
        else:
            print(f"Transactions between {start_date.strftime(CSV.FORMAT)} and {end_date.strftime(CSV.FORMAT)}:")
            print(filtered_df.to_string(index=False, formatters={"Date": lambda x: x.strftime(CSV.FORMAT)}))
            total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"]["Amount"].sum()
            print(f"Total Income: {total_income:.2f}")
            print(f"Total Expense: {total_expense:.2f}")
            print(f"Net Balance: {(total_income - total_expense):.2f}")
            return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter date of Transaction(DD-MM-YYYY) or Enter Today: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    if df is None or df.empty:
        print("No data to plot")
        return

    df_copy = df.copy()
    df_copy.set_index("Date", inplace=True)

    date_range = pd.date_range(start=df_copy.index.min(), end=df_copy.index.max(), freq='D')

    income_df = df_copy[df_copy["Category"] == "Income"]
    expense_df = df_copy[df_copy["Category"] == "Expense"]

    if not income_df.empty:
        income_daily = income_df.resample("D")["Amount"].sum()
    else:
        income_daily = pd.Series(dtype=float)

    if not expense_df.empty:
        expense_daily = expense_df.resample("D")["Amount"].sum()
    else:
        expense_daily = pd.Series(dtype=float)

    income_daily = income_daily.reindex(date_range, fill_value=0)
    expense_daily = expense_daily.reindex(date_range, fill_value=0)

    plt.figure(figsize=(12, 6))
    plt.plot(income_daily.index, income_daily.values, label="Income", color="g", marker='o')
    plt.plot(expense_daily.index, expense_daily.values, label="Expense", color="r", marker='o')
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n" + "=" * 30)
        print("Personal Finance Tracker")
        print("=" * 30)
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Exit")
        print("=" * 30)

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            add()
        elif choice == "2":
            try:
                start_date = input("Enter start date (DD-MM-YYYY): ").strip()
                end_date = input("Enter end date (DD-MM-YYYY): ").strip()

                # Validate date format
                datetime.strptime(start_date, CSV.FORMAT)
                datetime.strptime(end_date, CSV.FORMAT)

                df = CSV.get_transactions(start_date, end_date)

                if df is not None and not df.empty:
                    plot_choice = input("\nDo you want to plot the transactions? (y/n): ").lower().strip()
                    if plot_choice == "y":
                        plot_transactions(df)

            except ValueError as e:
                print(f"Invalid date format. Please use DD-MM-YYYY format.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
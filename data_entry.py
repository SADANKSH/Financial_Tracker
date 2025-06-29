from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORY= {"I":"Income", "E":"Expense"}
def get_date(prompt,allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter date in the format DD-MM-YYYY")
        return get_date(prompt,allow_default)

def get_amount():
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter category( I for Income, E for Expense): ").upper()
    if category in CATEGORY:
        return CATEGORY[category]
    print("Invalid category. Please enter I or E")
    return get_category()

def get_description():
    return input("Enter a description:" )

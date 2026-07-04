from expense import Expense
import calendar
import datetime


def main():
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000

    # Get user input for expense.
    expense = get_user_expense()

    # Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expenses.
    summarize_expenses(expense_file_path, budget, expense)


def get_user_expense():
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount ($): "))
    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}. {category_name}")

        selected_index = int(input(f"Enter a category number: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")


def save_expense_to_file(expense: Expense, expense_file_path):
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path, budget, new_expense):
    expenses: list[Expense] = []
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
            )
            expenses.append(line_expense)

    total_spent = sum([x.amount for x in expenses])
    print(f"You've added {new_expense.name} (${new_expense.amount:.2f}) to your expenses.")
    print(f"You have {len(expenses)} expenses totalling ${total_spent:.2f}.")

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print()
    print("📈 Expenses by category")
    for key, amount in amount_by_category.items():
        print(f"{key}: ${amount:.2f}")

    remaining_budget = budget - total_spent

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days

    print()
    print("💵 Budget")
    print(pink(f"You have ${remaining_budget:.2f} left to spend this month."))
    print(pink(f"That's roughly ${daily_budget:.2f} per day."))


def pink(text):
    return f"\033[38;5;198m{text}\033[0m"


if __name__ == "__main__":
    main()
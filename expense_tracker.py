from expense import Expense


def main():
  print(f"📌 Running Pocket Buddy!")

  # Get users input for expense
  expense = get_user_expense()
  print(expense)

  # Write their expense to a file
  save_expense_to_file()

  # Read file and summarize their expenses
  summarize_expense()
  


def get_user_expense():
  print(f"📌 Getting User Expense")
  expense_name = input("Enter expense name: ")
  expense_amount = float(input("Enter expense amount: "))
  expense_categories = [
    "🍛 Food", 
    "🏘️  Home", 
    "💼 Work", 
    "🎉 Fun", 
    "👌 Misc"
  ]

  while True:
    print("Selcet a category: ")
    for i, category_name in enumerate(expense_categories):
      print(f" {i + 1}. {category_name}")
    
    value_range = f"[1 - {len(expense_categories)}]"
    selceted_index = int(input(f"Enter a category number {value_range}: ")) - 1

    if selceted_index in range(len(expense_categories)):
      selected_category = expense_categories[selceted_index]
      new_expense = Expense(name=expense_categories, category=selected_category, amount=expense_amount)
      return 
    else: 
      print("Invalid category. Please try again!")

  

def save_expense_to_file():
  print(f"📌 Saving user Expense")
 

def summarize_expense():
  print(f"📌 Summarizing User Expense")
 



if __name__ == "__main__":
  main()

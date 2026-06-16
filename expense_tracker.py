def main():
  print(f"📌 Running Pocket Buddy!")

  # Get the users input for expense
  get_user_expense()

  # Write their expense to a file
  save_expense_to_file()

  # Read file and summarize their expenses
  summarize_expense()
  


def get_user_expense():
  print(f"📌 Getting User Expense")
  expense_name = input("Enter expense name: ")
  print(f"You've entered {expense_name}")
  

def save_expense_to_file():
  print(f"📌 Saving user Expense")
 

def summarize_expense():
  print(f"📌 Summarizing User Expense")
 



if __name__ == "__main__":
  main()

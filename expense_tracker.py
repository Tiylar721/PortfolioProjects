from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu
from tkinter import messagebox
import pandas as pd
import openpyxl
from expense import Expense
import datetime
import calendar

expense_categories = ["Food", "Bills", "Shopping", "Going Out", "Misc"]

def main():
    expense_file_path = "expenses.csv"
    expense_excel_path = "expenses.xlsx"
    budget = 4300

    # Create the main window
    window = Tk()
    window.title("Expense Tracker")

    # Create labels and entry fields for expense input
    expense_name_label = Label(window, text="Expense Name:")
    expense_name_label.grid(row=0, column=0, padx=10, pady=10)
    expense_name_entry = Entry(window)
    expense_name_entry.grid(row=0, column=1, padx=10, pady=10)

    expense_amount_label = Label(window, text="Expense Amount:")
    expense_amount_label.grid(row=1, column=0, padx=10, pady=10)
    expense_amount_entry = Entry(window)
    expense_amount_entry.grid(row=1, column=1, padx=10, pady=10)

    expense_category_label = Label(window, text="Expense Category:")
    expense_category_label.grid(row=2, column=0, padx=10, pady=10)
    expense_category_var = StringVar(window)
    expense_category_var.set(expense_categories[0])
    expense_category_menu = OptionMenu(window, expense_category_var, *expense_categories)
    expense_category_menu.grid(row=2, column=1, padx=10, pady=10)

    # Create a button to save the expense
    save_button = Button(window, text="Save Expense", command=lambda: save_expense(expense_name_entry.get(), expense_amount_entry.get(), expense_category_var.get(), expense_file_path))
    save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Create a button to summarize expenses
    summarize_button = Button(window, text="Summarize Expenses", command=lambda: summarize_expenses(expense_file_path, expense_excel_path, budget))
    summarize_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Run the main event loop
    window.mainloop()


def save_expense(name, amount, category, expense_file_path):
    if not name or not amount:
        messagebox.showwarning("Missing Information", "Please enter both expense name and amount.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Invalid Amount", "Please enter a valid expense amount.")
        return

    expense_data = {
        "Category": [category],
        "Name": [name],
        "Amount": [amount]
    }
    expense_df = pd.DataFrame(expense_data)

    # Append the expense to the CSV file
    expense_df.to_csv(expense_file_path, mode="a", header=False, index=False)

    messagebox.showinfo("Expense Saved", "Expense has been saved successfully.")


def summarize_expenses(expense_file_path, expense_excel_path, budget):
    expenses_df = pd.read_csv(expense_file_path, names=["Category", "Name", "Amount"])

    amount_by_category = expenses_df.groupby("Category")["Amount"].sum().reset_index()

    summary_text = "Expenses by category:\n"
    for _, row in amount_by_category.iterrows():
        summary_text += f"  {row['Category']}: ${row['Amount']:.2f}\n"

    total_spent = expenses_df["Amount"].sum()
    summary_text += f"\nYou've spent ${total_spent:.2f} this month!"

    remaining_budget = budget - total_spent
    summary_text += f"\nBudget Remaining: ${remaining_budget:.2f} this month!"

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    summary_text += f"\nRemaining days in the current month: {remaining_days}"

    daily_budget = remaining_budget / remaining_days
    summary_text += f"\nBudget Per Day: ${daily_budget:.2f}"

    # Save expenses to an Excel file
    expenses_df.to_excel(expense_excel_path, index=False)

    messagebox.showinfo("Expense Summary", summary_text)


if __name__ == "__main__":
    main()

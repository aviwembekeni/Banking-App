import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import string
import json
import os
from datetime import datetime
 
class Account:
    def __init__(self, username, password, name, surname, email):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email
        self.balance = 0
        self.transaction_history = []
 
    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                self.balance += amount
                timestamp = self.get_current_datetime()
                self.transaction_history.append(f"{timestamp} - Deposit: +R{amount}")
                return True
            else:
                raise ValueError("Deposit amount must be positive.")
        except ValueError:
            raise ValueError("Invalid input for deposit amount.")
 
    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                if self.balance >= amount:
                    self.balance -= amount
                    timestamp = self.get_current_datetime()
                    self.transaction_history.append(f"{timestamp} - Withdrawal: -R{amount}")
                    return True
                else:
                    raise ValueError("Insufficient funds.")
            else:
                raise ValueError("Withdrawal amount must be positive.")
        except ValueError:
            raise ValueError("Invalid input for withdrawal amount.")
 
    def transfer(self, amount, recipient_account):
        try:
            amount = float(amount)
            if amount > 0:
                if self.balance >= amount:
                    self.balance -= amount
                    timestamp = self.get_current_datetime()
                    self.transaction_history.append(
                        f"{timestamp} - Transfer to {recipient_account.username}: -R{amount}")
                    recipient_account.balance += amount
                    recipient_account.transaction_history.append(
                        f"{timestamp} - Transfer from {self.username}: +R{amount}")
                    return True
                else:
                    raise ValueError("Insufficient funds.")
            else:
                raise ValueError("Transfer amount must be positive.")
        except ValueError:
            raise ValueError("Invalid input for transfer amount.")
 
    def bill_payment(self, bill_type, amount):
        try:
            amount = float(amount)
            if amount > 0:
                if self.balance >= amount:
                    self.balance -= amount
                    timestamp = self.get_current_datetime()
                    self.transaction_history.append(
                        f"{timestamp} - Bill Payment: -R{amount} for {bill_type}")
                    return True
                else:
                    raise ValueError("Insufficient funds.")
            else:
                raise ValueError("Bill payment amount must be positive.")
        except ValueError:
            raise ValueError("Invalid input for bill payment amount.")
 
    def generate_statement(self):
        statement = f"Bank Statement for {self.username}:\n"
        for transaction in self.transaction_history:
            timestamp, details = transaction.split(' - ', 1)  # Split at the first occurrence of ' - '
            date_part = timestamp.split()[0]  # Extract only the date part
            statement += f"{date_part} - <{details}>\n"  # Construct the statement without time
        statement += f"Current Balance: R{self.balance}\n"
        return statement
 
    def save_data(self):
        data = {
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "balance": self.balance,
            "transaction_history": self.transaction_history
        }
        filename = f"{self.username}.json"
        with open(filename, 'w') as file:
            json.dump(data, file)
 
    @staticmethod
    def load_account(username):
        filename = f"{username}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
                account = Account(data["username"], data["password"], data["name"], data["surname"], data["email"])
                account.balance = data["balance"]
                account.transaction_history = data["transaction_history"]
                return account
        else:
            return None
 
    @staticmethod
    def get_current_datetime():
        return datetime.now().strftime("%Y-%m-%d")
 
 
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank App - Login")
        self.root.geometry("400x300")
        self.root.configure(bg="light grey")
 
        self.frame = tk.Frame(self.root, bg="light grey")
        self.frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
 
        self.label_title = tk.Label(self.frame, text="TECH-CON TRADERS BANK APP", bg="light grey", fg="dark green",
                                    font=("Times New Roman", 20, "bold"))
        self.label_title.place(relx=0.5, rely=0.1, anchor="n")
 
        self.label_username = tk.Label(self.frame, text="Username", bg="light grey", fg="dark green",
                                       font=("Times New Roman", 16))
        self.label_username.place(relx=0.2, rely=0.3)
 
        self.entry_username = tk.Entry(self.frame, bg="white", fg="black", font=("Helvetica", 14))
        self.entry_username.place(relx=0.4, rely=0.3)
 
        self.label_password = tk.Label(self.frame, text="Password", bg="light grey", fg="dark green",
                                       font=("Times New Roman", 16))
        self.label_password.place(relx=0.2, rely=0.4)
 
        self.entry_password = tk.Entry(self.frame, bg="white", fg="#333", font=("Helvetica", 14), show="*")
        self.entry_password.place(relx=0.4, rely=0.4)
 
        self.button_login = tk.Button(self.frame, text="Login", bg="dark green", fg="#fff", font=("Helvetica", 12),
                                      command=self.login)
        self.button_login.place(relx=0.35, rely=0.5)
 
        self.button_register = tk.Button(self.frame, text="Register", bg="dark green", fg="#fff",
                                         font=("Helvetica", 12),
                                         command=self.register)
        self.button_register.place(relx=0.55, rely=0.5)
 
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
 
        # Check username and password
        account = Account.load_account(username)
        if account and account.password == password:
            self.root.destroy()  # Close login window
            banking_app = BankSystem(account)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
 
    def register(self):
        # Function to generate a random password
        def generate_password():
            letters = string.ascii_letters
            digits = string.digits
            symbols = string.punctuation
 
            password_characters = letters + digits + symbols
            generated_password = ''.join(random.choice(password_characters) for i in range(12))
            return generated_password
 
        # Function to handle registration
        def register_user():
            username = username_entry.get()
            password = password_entry.get()
            name = name_entry.get()
            surname = surname_entry.get()
            email = email_entry.get()
 
            try:
                account = Account(username, password, name, surname, email)
                account.save_data()
                registration_window.destroy()  # Close registration window after successful registration
                # Show registration success message with username and current date/time
                message = f"Thank you, {name}, for registering with Tech-Con Traders Banking App.\n"
                message += f"Registration Date: {Account.get_current_datetime()}"
                messagebox.showinfo("Registration Successful", message)
            except Exception as e:
                messagebox.showerror("Registration Failed", str(e))
 
        # Create the registration window
        registration_window = tk.Toplevel(self.root)
        registration_window.title("Register - Bank App")
        registration_window.geometry("500x300")
        registration_window.configure(bg="light grey")
 
        frame = ttk.Frame(registration_window, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
 
        # Labels and entries for Name, Surname, Email
        name_label = ttk.Label(frame, text="Name:")
        name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
 
        name_entry = ttk.Entry(frame, font=("Helvetica", 14))
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
 
        surname_label = ttk.Label(frame, text="Surname:")
        surname_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
 
        surname_entry = ttk.Entry(frame, font=("Helvetica", 14))
        surname_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
 
        email_label = ttk.Label(frame, text="Email:")
        email_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
 
        email_entry = ttk.Entry(frame, font=("Helvetica", 14))
        email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
 
        username_label = ttk.Label(frame, text="Enter Username:")
        username_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
 
        username_entry = ttk.Entry(frame, font=("Helvetica", 14))
        username_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
 
        password_label = ttk.Label(frame, text="Enter Password:")
        password_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
 
        password_entry = ttk.Entry(frame, font=("Helvetica", 14))
        password_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
 
        # Button to generate a random password
        generate_button = ttk.Button(frame, text="Generate Password",
                                     command=lambda: password_entry.insert(tk.END, generate_password()))
        generate_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
 
        register_button = ttk.Button(frame, text="Register", command=register_user)
        register_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
 
 
class BankSystem(tk.Tk):
    def __init__(self, account):
        super().__init__()
        self.title("Bank App")
        self.configure(bg="light grey")
 
        self.account = account
 
        # Create a frame for centralizing widgets
        frame = tk.Frame(self, bg="light grey")
        frame.pack(expand=True, fill="both")
 
        self.label_balance = tk.Label(frame, text=f"Current Balance: R{self.account.balance:.2f}",
                                      font=("Times New Roman", 30),
                                      bg="light grey", fg="dark green")
        self.label_balance.pack(pady=20)
 
        button_frame = tk.Frame(frame, bg="light grey")
        button_frame.pack(pady=20)
 
        # Adjust button sizes and spacing
        button_style = {"bg": "dark green", "fg": "#fff", "font": ("Helvetica", 18)}
 
        self.button_deposit = tk.Button(button_frame, text="Deposit", **button_style, command=self.ask_deposit)
        self.button_deposit.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
 
        self.button_withdraw = tk.Button(button_frame, text="Withdraw", **button_style, command=self.ask_withdraw)
        self.button_withdraw.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
 
        self.button_transfer = tk.Button(button_frame, text="Transfer", **button_style, command=self.ask_transfer)
        self.button_transfer.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
 
        self.button_statement = tk.Button(button_frame, text="Statement", **button_style,
                                          command=self.generate_statement)
        self.button_statement.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
 
        self.button_bills = tk.Button(button_frame, text="Pay Bills", **button_style, command=self.pay_bills)
        self.button_bills.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
 
        self.button_logout = tk.Button(frame, text="Log Out", bg="dark red", fg="#fff", font=("Helvetica", 18),
                                       command=self.log_out)
        self.button_logout.pack(fill="x", padx=10, pady=10)
 
        # Center the window on the screen
        self.center_window()
 
    def center_window(self):
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
 
        # Calculate x and y coordinates to center the window
        x = (screen_width - self.winfo_reqwidth()) / 2
        y = (screen_height - self.winfo_reqheight()) / 2
 
        # Set the window position
        self.geometry("+%d+%d" % (x, y))
 
    def ask_deposit(self):
        response = messagebox.askyesno("Deposit", "Would you like to make a deposit?")
        if response:
            amount = simpledialog.askfloat("Deposit", "Enter deposit amount:")
            if amount:
                try:
                    self.account.deposit(amount)
                    self.update_balance()
                    self.account.save_data()
                    messagebox.showinfo("Deposit", f"Successfully deposited R{amount}.")
                except ValueError as e:
                    messagebox.showerror("Deposit Error", str(e))
        else:
            messagebox.showinfo("Deposit", "Thank you for using the Tech-Con Traders banking app.")
 
    def ask_withdraw(self):
        response = messagebox.askyesno("Withdraw", "Would you like to make a withdrawal?")
        if response:
            amount = simpledialog.askfloat("Withdraw", "Enter withdrawal amount:")
            if amount:
                try:
                    self.account.withdraw(amount)
                    self.update_balance()
                    self.account.save_data()
                    messagebox.showinfo("Withdraw", f"Successfully withdrew R{amount}.")
                except ValueError as e:
                    messagebox.showerror("Withdraw Error", str(e))
        else:
            messagebox.showinfo("Withdraw", "Thank you for using the Tech-Con Traders banking app.")
 
    def ask_transfer(self):
        # Step 1: Ask if the user wants to make a transfer
        response = messagebox.askyesno("Transfer", "Would you like to make a transfer?")
        if response:
            # Step 2: Ask for recipient's username
            recipient_username = simpledialog.askstring("Transfer", "Enter recipient's username:")
            if recipient_username:
                recipient_account = Account.load_account(recipient_username)
                if recipient_account:
                    # Step 3: Ask for transfer amount
                    amount = simpledialog.askfloat("Transfer", f"Enter transfer amount to {recipient_username}:")
                    if amount:
                        try:
                            self.account.transfer(amount, recipient_account)
                            self.update_balance()
                            self.account.save_data()
                            messagebox.showinfo("Transfer",
                                                f"Successfully transferred R{amount} to {recipient_username}.")
                        except ValueError as e:
                            messagebox.showerror("Transfer Error", str(e))
                else:
                    messagebox.showerror("Transfer Error", f"Recipient '{recipient_username}' not found.")
            else:
                messagebox.showinfo("Transfer", "Transfer canceled.")
        else:
            messagebox.showinfo("Transfer", "Thank you for using the Tech-Con Traders banking app.")
 
    def pay_bills(self):
        bill_type = simpledialog.askstring("Pay Bills", "Select bill type: Water, Electricity, or Prepaid Mobile")
        if bill_type:
            if bill_type.lower() == "water" or bill_type.lower() == "electricity":
                meter_number = simpledialog.askstring("Pay Bills", f"Enter {bill_type} meter number:")
                if meter_number:
                    amount = simpledialog.askfloat("Pay Bills", f"Enter amount for {bill_type} bill payment:")
                    if amount:
                        try:
                            self.account.bill_payment(f"{bill_type.capitalize()} Bill", amount)
                            self.update_balance()
                            self.account.save_data()
                            messagebox.showinfo("Bill Payment", f"Successfully paid R{amount} for {bill_type} bill.")
                        except ValueError as e:
                            messagebox.showerror("Bill Payment Error", str(e))
                    else:
                        messagebox.showinfo("Bill Payment", "Bill payment canceled.")
                else:
                    messagebox.showinfo("Bill Payment", "Bill payment canceled.")
            elif bill_type.lower() == "prepaid mobile":
                network = simpledialog.askstring("Pay Bills", "Select mobile network: TELKOM, MTN, VODACOM, or CELL C")
                if network:
                    cellphone = simpledialog.askstring("Pay Bills", "Enter cellphone number:")
                    if cellphone:
                        amount = simpledialog.askfloat("Pay Bills", f"Enter amount for {network} prepaid recharge:")
                        if amount:
                            try:
                                self.account.bill_payment(f"{network.capitalize()} Prepaid", amount)
                                self.update_balance()
                                self.account.save_data()
                                messagebox.showinfo("Bill Payment",
                                                    f"Successfully recharged R{amount} for {network} prepaid.")
                            except ValueError as e:
                                messagebox.showerror("Bill Payment Error", str(e))
                        else:
                            messagebox.showinfo("Bill Payment", "Bill payment canceled.")
                    else:
                        messagebox.showinfo("Bill Payment", "Bill payment canceled.")
                else:
                    messagebox.showinfo("Bill Payment", "Bill payment canceled.")
            else:
                messagebox.showerror("Bill Payment", "Invalid bill type selected.")
        else:
            messagebox.showinfo("Bill Payment", "Bill payment canceled.")
 
    def generate_statement(self):
        statement = self.account.generate_statement()
        messagebox.showinfo("Bank Statement", statement)
 
    def log_out(self):
        self.destroy()  # Close current banking app window
        root = tk.Tk()  # Create new login window
        login_page = LoginPage(root)
        root.mainloop()
 
    def update_balance(self):
        self.label_balance.config(text=f"Current Balance: R{self.account.balance:.2f}")
 
 
def main():
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()
 
 
if __name__ == "__main__":
    main()
 
 
import tkinter as tk
from tkinter import messagebox, simpledialog
from database import create_connection
from datetime import datetime,date
import random
from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageTk
from docx import Document
import os
import re
from admin_management import AdminLogin
import mysql.connector
from mysql.connector import Error
 

class welcomeScreen:
	def __init__(self, window=None):
		self.master = window
		window.attributes('-fullscreen', True)
		window.title("Welcome to BANK")
		
		self.bg_image = Image.open("background.jpg")
		self.bg_image = self.bg_image.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.LANCZOS)
		self.bg_photo = ImageTk.PhotoImage(self.bg_image)
		self.bg_label = tk.Label(window, image=self.bg_photo)
		self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

		tk.Label(window, text="WELCOME TO BANK", font=("Arial", 24, "bold"), fg="white", bg="#023047").place(relx=0.3, rely=0.4, anchor="center")
		
		# Buttons centered below the welcome message
		self.create_button("EMPLOYEE", self.select_employee, 0.3, 0.5)
		self.create_button("CUSTOMER", self.select_customer, 0.3, 0.6)
		self.create_button("CLOSE", window.quit, 0.3, 0.7, bg="powderblue")

	def create_button(self, text, command, relx, rely, bg="#161179"):
		btn = tk.Button(self.master, text=text, font=("Arial", 14, "bold"), command=command, bg=bg, fg="white", relief="raised", bd=4, padx=20, pady=10)
		btn.place(relx=relx, rely=rely, anchor="center")

	def select_employee(self):
		self.master.destroy()
		AdminLogin(tk.Tk())

	def select_customer(self):
		self.master.destroy()
		CustomerSelection(tk.Tk())

class CustomerSelection:
	def __init__(self, window=None):
		self.master = window
		window.attributes('-fullscreen', True)
		window.title("Customer Selection")

		self.set_background("customer_bg.jpg")

		tk.Label(window, text="Are you a New or Existing User?", font=("Arial", 20, "bold"), bg="#000000", fg="white").place(x=575, y=280)
		
		# Align buttons to the left-center
		self.create_button("New User", self.new_user, 0.3)
		self.create_button("Existing User", self.existing_user, 0.4)
		self.create_button("Back", self.back, 0.5, bg="#f77f00")

	def set_background(self, image_path):
		self.bg_image = Image.open(image_path)
		self.bg_image = self.bg_image.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.LANCZOS)
		self.bg_photo = ImageTk.PhotoImage(self.bg_image)
		self.bg_label = tk.Label(self.master, image=self.bg_photo)
		self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

	def create_button(self, text, command, rely, bg="#0081a7"):
		"""Place button on the left-center side of the screen."""
		btn = tk.Button(self.master, text=text, font=("Arial", 14, "bold"), command=command, bg=bg, fg="white", relief="ridge", bd=5, padx=20, pady=10)
		btn.place(relx=0.1, rely=rely, anchor="w")  # Adjust `relx` to keep buttons on the left


		

	def new_user(self):
		self.master.destroy()
		CustomerRegistration(tk.Tk())

	def existing_user(self):
		self.master.destroy()
		CustomerLogin(tk.Tk())

	def back(self):
		self.master.destroy()
		welcomeScreen(tk.Tk())

class CustomerLogin:
	def __init__(self, window=None):
		self.master = window
		window.attributes('-fullscreen', True)
		window.title("Customer Login")

		# Set Background Image Fullscreen
		self.set_background("login_bg.jpg")

		# Title Label (Left Center)
		tk.Label(window, text="Customer Login", font=("Arial", 24, "bold"), bg="#000000", fg="white").place(x=100, y=100)

		# Input Fields (Left Center)
		self.entry1 = self.create_entry("Account Number:", y_pos=180)
		self.entry2 = self.create_entry("PIN:", show='*', y_pos=260)

		# Buttons (Left Center)
		self.create_button("Login", self.login, y_pos=340)
		self.create_button("Back", self.back, y_pos=420, bg="#f77f00")

	def set_background(self, image_path):
		"""Resize and set the background image to fullscreen."""
		bg_image = Image.open(image_path)
		bg_image = bg_image.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.LANCZOS)
		self.bg_photo = ImageTk.PhotoImage(bg_image)

		self.bg_label = tk.Label(self.master, image=self.bg_photo)
		self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

	def create_entry(self, text, y_pos, show=None):
		tk.Label(self.master, text=text, font=("Arial", 16), bg="#023047", fg="white").place(x=100, y=y_pos)
		entry = tk.Entry(self.master, show=show, bg="white", font=("Arial", 14), bd=4, relief="groove", width=30)
		entry.place(x=100, y=y_pos + 40)
		return entry

	def create_button(self, text, command, y_pos, bg="#0081a7"):
		btn = tk.Button(self.master, text=text, font=("Arial", 14, "bold"), command=command,
						bg=bg, fg="white", relief="ridge", bd=5, padx=30, pady=10)
		btn.place(x=100, y=y_pos)

	def login(self):
		account_number = self.entry1.get().strip()
		pin = self.entry2.get().strip()

		connection = create_connection()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM customers WHERE account_number = %s AND pin = %s", (account_number, pin))
		result = cursor.fetchone()
		cursor.close()
		connection.close()

		if result:
			messagebox.showinfo("Login Successful", "Welcome to your account!")
			self.master.destroy()
			root = tk.Tk()
			CustomerDashboard(root, account_number)
			root.mainloop()
		else:
			messagebox.showerror("Login Failed", "Invalid Account Number or PIN!")

	def back(self):
		self.master.destroy()
		CustomerSelection(tk.Tk())


class CustomerRegistration:
	def __init__(self, window=None):
		self.master = window
		window.attributes('-fullscreen', True)  # Fullscreen mode
		window.title("Customer Registration")

		# Load and set the background image
		self.bg_image = Image.open("register_bg.jpg")
		self.bg_image = self.bg_image.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.LANCZOS)
		self.bg_photo = ImageTk.PhotoImage(self.bg_image)
		self.bg_label = tk.Label(window, image=self.bg_photo)
		self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover entire window

		# Title Label
		tk.Label(window, text="Customer Registration", font=("Arial", 20, "bold"), bg="#023047", fg="white").pack(pady=20)

		# Create entry fields and store references
		self.entries = {}
		self.create_label_entry("Name")
		self.create_label_entry("DOB (YYYY-MM-DD)")
		self.create_label_entry("Aadhar Number")
		self.create_label_entry("Mobile Number")
		self.create_label_entry("Nationality")
		self.create_label_entry("Annual Income")
		self.create_label_entry("PIN", show='*')

		# Create Register and Back buttons
		self.create_button("Register", self.register)
		self.create_button("Back", self.back)

	def create_label_entry(self, label_text, show=None):
		"""Create a label and entry field and store entry in a dictionary."""
		key = label_text.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")  # Normalize key name
		label = tk.Label(self.master, text=label_text, font=("Arial", 14), bg="#023047", fg="white")
		label.pack(anchor="w", padx=20, pady=5)
		entry = tk.Entry(self.master, font=("Arial", 12), bg="#03055B", fg="white", bd=3, relief="groove", show=show)
		entry.pack(anchor="w", padx=20, pady=5)
		self.entries[key] = entry  # Store entry in a dictionary

	def create_button(self, text, command):
		"""Create a button aligned to the left and slightly indented."""
		btn = tk.Button(self.master, text=text, font=("Arial", 14, "bold"), command=command,
						bg="#03055B", fg="white", relief="ridge", bd=5, padx=20, pady=10)
		btn.pack(anchor="w", padx=20, pady=10)

	def register(self):
		try:
			name = self.entries["name"].get().strip()
			dob = self.entries["dob_yyyy_mm_dd"].get().strip()
			aadhar = self.entries["aadhar_number"].get().strip()
			mobile = self.entries["mobile_number"].get().strip()
			nationality = self.entries["nationality"].get().strip()
			annual_income = self.entries["annual_income"].get().strip()
			pin = self.entries["pin"].get().strip()

			# Validate input
			if not all([name, dob, aadhar, mobile, nationality, annual_income, pin]):
				messagebox.showerror("Error", "All fields must be filled.")
				return

			if not re.fullmatch(r"\d{12}", aadhar):
				messagebox.showerror("Error", "Aadhar number must be exactly 12 digits.")
				return

			if not re.fullmatch(r"\d{10}", mobile):
				messagebox.showerror("Error", "Mobile number must be exactly 10 digits.")
				return

			if not re.fullmatch(r"\d{4}", pin):
				messagebox.showerror("Error", "PIN must be exactly 4 digits.")
				return

			try:
				annual_income = float(annual_income)
			except ValueError:
				messagebox.showerror("Error", "Annual income must be a valid number.")
				return

			# Insert into database
			connection = create_connection()
			cursor = connection.cursor()
			cursor.execute("""
				INSERT INTO account_requests (name, dob, aadhar, mobile_number, nationality, annual_income, pin) 
			VALUES (%s, %s, %s, %s, %s, %s, %s)
		""", (name, dob, aadhar, mobile, nationality, annual_income, pin))
			connection.commit()
			cursor.close()
			connection.close()

			messagebox.showinfo("Registration Successful", "Your request has been sent to the admin.")
			self.master.after(500, self.master.destroy)  # Fix: Wait 500ms before destroying window
			from customer_management import CustomerSelection  # Avoid circular imports
			CustomerSelection(self.master)  

		except Exception as e:
			messagebox.showerror("Error", f"Registration failed: {str(e)}")




	def back(self):
		"""Clear window and return to Customer Selection."""
		from customer_management import CustomerSelection  # Avoid circular imports
		for widget in self.master.winfo_children():
			widget.destroy()
		CustomerSelection(self.master)  # Reload previous screen



class CustomerDashboard:
	def __init__(self, window, account_number):
		self.master = window
		self.account_number = account_number
		window.attributes('-fullscreen', True)  # Fullscreen Mode
		window.title("Customer Dashboard")
		window.configure(bg="#023047")  # Background Color

		# Title Label
		tk.Label(window, text="Customer Dashboard", font=("Arial", 24, "bold"), fg="white", bg="#023047").pack(pady=20)

		# Buttons with Styling
		self.create_button("Apply for ATM Card", self.apply_atm)
		self.create_button("Apply for Loan", self.apply_loan)
		self.create_button("Generate Transaction Report", self.generate_report)
		self.create_button("Deposit", self.deposit)
		self.create_button("Withdraw", self.withdraw)
		self.create_button("Back", self.back, bg="#d62828")  # Red for Back button

	def create_button(self, text, command, bg="#0081a7"):
		"""Creates a styled button with hover effect"""
		btn = tk.Button(
			self.master, text=text, font=("Arial", 16, "bold"), command=command,
			bg=bg, fg="white", relief="ridge", bd=5, padx=20, pady=10, width=25
		)
		btn.pack(pady=10)

		# Hover Effect
		def on_enter(e): btn.config(bg="#005f73")  # Darker on hover
		def on_leave(e): btn.config(bg=bg)  # Original color on leave

		btn.bind("<Enter>", on_enter)
		btn.bind("<Leave>", on_leave)

	def apply_atm(self):
		try:
			connection = create_connection()
			cursor = connection.cursor()

		# Check if an ATM request already exists for this account
			cursor.execute("SELECT * FROM atm_requests WHERE account_number = %s", (self.account_number,))
			existing_request = cursor.fetchone()

			if existing_request:
				messagebox.showinfo("Request Exists", "You have already requested an ATM card.")
			else:
			# Insert a new ATM request
				cursor.execute(
				"INSERT INTO atm_requests (account_number, status) VALUES (%s, 'Pending')",
				(self.account_number,)
			)
				connection.commit()
				messagebox.showinfo("Request Sent", "ATM request sent to admin.")

			cursor.close()
			connection.close()

		except mysql.connector.Error as e:
			messagebox.showerror("Database Error", f"Error: {e}")




	def apply_loan(self):
		amount = simpledialog.askinteger("Loan Application", "Enter loan amount:")
		if not amount or amount <= 0:
			messagebox.showerror("Invalid Amount", "Please enter a valid loan amount.")
			return

		connection = create_connection()
		cursor = connection.cursor()

	# Fetch DOB and annual income from database
		cursor.execute("SELECT dob, annual_income FROM customers WHERE account_number = %s", (self.account_number,))
		customer_data = cursor.fetchone()

		if not customer_data:
			messagebox.showerror("Error", "Account not found.")
			cursor.close()
			connection.close()
			return

		dob, annual_income = customer_data

	# Convert dob to datetime if necessary
		if isinstance(dob, str):
			dob = datetime.strptime(dob, "%Y-%m-%d").date()  # Convert string to date
		elif isinstance(dob, date):  
			dob = datetime(dob.year, dob.month, dob.day)  # Convert date to datetime
		else:
			messagebox.showerror("Error", "Invalid date of birth format.")
			cursor.close()
			connection.close()
			return

	# Convert annual_income to float for comparison
			annual_income = float(annual_income)

	# Calculate age
		today = date.today()
		age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

	# Check eligibility
		if age < 21:
			messagebox.showerror("Loan Denied", "You must be at least 21 years old to apply for a loan.")
			cursor.close()
			connection.close()
			return
		if annual_income < 200000:
			messagebox.showerror("Loan Denied", "Annual income must be greater than ₹2,00,000 to apply for a loan.")
			cursor.close()
			connection.close()
			return

	# Convert dob to string before inserting into MySQL
		dob_str = dob.strftime("%Y-%m-%d")

	# Insert loan request into database
		cursor.execute("INSERT INTO loan_requests (account_number, dob, amount, status) VALUES (%s, %s, %s, 'Pending')",
				   (self.account_number, dob_str, amount))

		connection.commit()
		cursor.close()
		connection.close()

		messagebox.showinfo("Success", "Loan request submitted successfully!")

	def generate_report(self):
		connection = create_connection()
		cursor = connection.cursor()
		cursor.execute("INSERT INTO report_requests (account_number, status) VALUES (%s, 'Pending')", (self.account_number,))
		connection.commit()
		cursor.close()
		connection.close()
		messagebox.showinfo("Report Request", "Your transaction report request has been sent to admin.")

	def deposit(self):
		amount = simpledialog.askinteger("Deposit", "Enter deposit amount:")
		if amount and amount > 0:
			connection = create_connection()
			cursor = connection.cursor()
			cursor.execute("UPDATE customers SET balance = balance + %s WHERE account_number = %s", (amount, self.account_number))
			cursor.execute("SELECT balance FROM customers WHERE account_number = %s", (self.account_number,))
			new_balance = cursor.fetchone()[0]
			cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount, transaction_date, balance) VALUES (%s, 'Deposit', %s, NOW(), %s)",
						   (self.account_number, amount, new_balance))
			connection.commit()
			cursor.close()
			connection.close()
			messagebox.showinfo("Deposit Successful", f"{amount} deposited successfully. New Balance: {new_balance}")
		else:
			messagebox.showerror("Deposit Failed", "Enter a valid deposit amount.")

	def withdraw(self):
		amount = simpledialog.askinteger("Withdraw", "Enter withdrawal amount:")
		if amount and amount > 0:
			connection = create_connection()
			cursor = connection.cursor()
			cursor.execute("SELECT balance FROM customers WHERE account_number = %s", (self.account_number,))
			result = cursor.fetchone()

			if result and result[0] >= amount:
				new_balance = result[0] - amount
				cursor.execute("UPDATE customers SET balance = %s WHERE account_number = %s", (new_balance, self.account_number))
				cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount, transaction_date, balance) VALUES (%s, 'Withdrawal', %s, NOW(), %s)",
							   (self.account_number, amount, new_balance))
				connection.commit()
				cursor.close()
				connection.close()
				messagebox.showinfo("Withdrawal Successful", f"{amount} withdrawn successfully. New Balance: {new_balance}")
			else:
				messagebox.showerror("Withdrawal Failed", "Insufficient balance.")
				cursor.close()
				connection.close()
		else:
			messagebox.showerror("Withdrawal Failed", "Enter a valid withdrawal amount.")

	def back(self):
		from customer_management import CustomerSelection  # Import inside function to avoid circular import
		for widget in self.master.winfo_children():  # Clear the window
			widget.destroy()
		CustomerSelection(self.master)  # Reload previous screen




if __name__ == "__main__":
	root = tk.Tk()
	app = welcomeScreen(root)
	root.mainloop()
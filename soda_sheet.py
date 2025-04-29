import tkinter as tk
from tkinter import messagebox
import gspread
from google.oauth2.service_account import Credentials

# Setup the connection
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("dulcet-voyager-458320-q7-e2a0bf866635.json", scopes=scopes)
client = gspread.authorize(creds)

gs = client.open_by_key('18ic5xlTyEdNp60P5Bw4Grb9X6r_HuD4MdW3gwLLOElY')
sheet = gs.worksheet('Order')

# Predefined drink menu
drink_menu = ["Milk Tea", "Green Tea", "Thai Tea", "Coffee"]
fixed_price = 30

# Submit handler
def submit():
    # cust_name = cust_entry.get()
    item = selected_drink.get()
    quantity = quantity_entry.get()
    coupon = coupon_entry.get()

    if not quantity:
        messagebox.showerror("Input Error", "Please enter quantity.")
        return

    try:
        quantity_val = int(quantity)
    except ValueError:
        messagebox.showerror("Input Error", "Quantity must be an integer.")
        return

    try:
        coupon_val = float(coupon) if coupon else 0.0
    except ValueError:
        messagebox.showerror("Input Error", "Coupon must be a number.")
        return

    total = (fixed_price * quantity_val) - coupon_val

    try:
        sheet.append_row([item, quantity_val, fixed_price, coupon_val, total])
        messagebox.showinfo("Success", f"Added! Total = {total:.2f}")
        quantity_entry.delete(0, tk.END)
        coupon_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Google Sheets Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Drink Order Entry")
root.geometry("400x400")

label_font = ("Arial", 10)
entry_font = ("Arial", 10)
button_font = ("Arial", 8, "bold")
width=15

# Drink dropdown
tk.Label(root, text="Item Name", font=label_font).pack()
selected_drink = tk.StringVar(root)
selected_drink.set(drink_menu[0])  # default

option_menu = tk.OptionMenu(root, selected_drink, *drink_menu)
option_menu.config(font=("Arial", 10), width=10)
option_menu.pack(pady=5)

# Quantity
tk.Label(root, text="Quantity", font=label_font).pack()
quantity_entry = tk.Entry(root, font=entry_font, width=width)
quantity_entry.pack(pady=5)

# Fixed Price (read-only)
tk.Label(root, text="Price (Fixed)", font=label_font).pack()
price_label = tk.Label(root, text=str(fixed_price), font=entry_font, width=width)
price_label.pack(pady=5)

# Coupon
tk.Label(root, text="Coupon/Discount", font=label_font).pack()
coupon_entry = tk.Entry(root, font=entry_font, width=width)
coupon_entry.pack(pady=10)

# Submit button
tk.Button(root, text="Add to sheet", command=submit, font=button_font, width=10).pack(pady=10)

root.mainloop()

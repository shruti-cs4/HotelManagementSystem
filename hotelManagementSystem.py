import tkinter as tk
from tkinter import messagebox

def add_item_to_order(item, quantity_entry):
    try:
        quantity = int(quantity_entry.get())
        if quantity > 0:
            orders[item] = quantity
    except ValueError:
        pass 

def save_bill_to_file(bill): 
    with open("past_records.txt", 'a', encoding='utf-8') as f: 
        f.write(bill + "\n")

def show_bill_popup():
    customer_name = customer_name_var.get().strip()
    customer_contact = customer_contact_var.get().strip()

    if not customer_name:
        messagebox.showwarning("Warning", "Please enter customer name.")
        return

    selected_items = []
    total_price = 0

    for item, quantity in orders.items():
        selected_items.append((item, quantity))
        total_price += items[item] * quantity

    if not selected_items:
        messagebox.showwarning("Warning", "Please select at least one item.")
        return

    gst_amount = (total_price * gst_percentage) / 100

    bill = f"Customer Name: {customer_name}\n"
    bill += f"Customer Contact: {customer_contact}\n\n"
    bill += "Selected Items:\n"
    for item, quantity in selected_items:
        bill += f"{item} x {quantity} - {convert_to_inr(items[item] * quantity)}\n"
    bill += f"\nTotal Price: {convert_to_inr(total_price)}\n"
    bill += f"GST ({gst_percentage}%): {convert_to_inr(gst_amount)}\n"
    bill += f"Grand Total: {convert_to_inr(total_price + gst_amount)}"

    save_bill_to_file(bill)
    messagebox.showinfo("Bill", bill)

def past_records():
    try:
        with open("past_records.txt", 'r', encoding='utf-8') as f:
            records = f.read()
            if records:
                records_window = tk.Toplevel(root)
                records_window.title("Past Records")
                records_text = tk.Text(records_window, wrap="word",bg="#fed9d7")
                records_text.pack(expand=True, fill="both")
                records_text.insert("1.0", records)
            else:
                messagebox.showinfo("Past Records", "No past records found.")
    except FileNotFoundError:
        messagebox.showinfo("Past Records", "No past records found.")

def clear_selection():
    for item in orders:
        orders[item] = 0
        order_entries[item].delete(0, tk.END)
    update_sample_bill()

def update_sample_bill():
    selected_items = []
    total_price = 0

    for item, quantity in orders.items():
        if quantity > 0:
            selected_items.append((item, quantity))
            total_price += items[item] * quantity

    gst_amount = (total_price * gst_percentage) / 100

    bill = f"Customer Name: {customer_name_var.get()}\n"
    bill += f"Customer Contact: {customer_contact_var.get()}\n\n"
    bill += "Selected Items:\n"
    for item, quantity in selected_items:
        bill += f"{item} x {quantity} - {convert_to_inr(items[item] * quantity)}\n"
    bill += f"\nTotal Price: {convert_to_inr(total_price)}\n"
    bill += f"GST ({gst_percentage}%): {convert_to_inr(gst_amount)}\n"
    bill += f"Grand Total: {convert_to_inr(total_price + gst_amount)}\n"

    sample_bill_text.delete("1.0", tk.END)  
    sample_bill_text.insert(tk.END, bill)

def validate_contact(value):
    return value.isdigit() or value == ""

def convert_to_inr(amount):
    return "₹" + str(amount)


root = tk.Tk()
root.title("Restaurant Management System")
root.configure(bg='#ff9b9b')
root.geometry("600x650")

customer_name_var = tk.StringVar()
customer_contact_var = tk.StringVar()

items = {
    "Burger": 100,
    "Pizza": 200,
    "Pasta": 150,
    "Sandwich": 80,
    "Salad": 90
}

orders = {}
order_entries = {}
gst_percentage = 18


details_frame = tk.LabelFrame(root, text="Customer Details", bg="#fed9d7")
details_frame.pack(fill="x", padx=10, pady=10)

name_label = tk.Label(details_frame, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
name_entry = tk.Entry(details_frame, textvariable=customer_name_var)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

contact_label = tk.Label(details_frame, text="Contact:")
contact_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
contact_entry = tk.Entry(details_frame, textvariable=customer_contact_var)
contact_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
vcmd = (root.register(validate_contact), '%P')
contact_entry.config(validate='key', validatecommand=vcmd)


menu_frame = tk.LabelFrame(root, text="Menu", bg="#fed9d7")
menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

item_header = tk.Label(menu_frame, text="Items")
item_header.grid(row=0, column=0, padx=5, pady=5, sticky="w")
quantity_header = tk.Label(menu_frame, text="Quantity")
quantity_header.grid(row=0, column=1, padx=5, pady=5, sticky="w")

row = 1
for item, price in items.items():
    item_label = tk.Label(menu_frame, text=f"{item} - {convert_to_inr(price)}")
    item_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

    quantity_entry = tk.Entry(menu_frame, width=5)
    quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
    quantity_entry.bind("<FocusOut>", lambda event, item=item, entry=quantity_entry: add_item_to_order(item, entry))
    quantity_entry.bind("<Return>", lambda event, item=item, entry=quantity_entry: add_item_to_order(item, entry))
    quantity_entry.bind("<KeyRelease>", lambda event, item=item, entry=quantity_entry: add_item_to_order(item, entry))
    
    orders[item] = 0
    order_entries[item] = quantity_entry

    row += 1


buttons_frame = tk.Frame(root, bg="#fed9d7")
buttons_frame.pack(fill="x", padx=10, pady=10)

print_bill_button = tk.Button(buttons_frame, text="Print Bill", command=show_bill_popup)
print_bill_button.pack(side="left", padx=5, expand=True, fill="both")

past_record_button = tk.Button(buttons_frame, text="Past Records", command=past_records)
past_record_button.pack(side="left", padx=5, expand=True, fill="both")

clear_selection_button = tk.Button(buttons_frame, text="Clear Selection", command=clear_selection)
clear_selection_button.pack(side="left", padx=5, expand=True, fill="both")


sample_bill_text = tk.Text(root, height=10, bg="#fed9d7")
sample_bill_text.pack(fill="x", padx=10, pady=10)

root.mainloop()


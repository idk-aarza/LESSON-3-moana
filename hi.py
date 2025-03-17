import tkinter as tk
from tkinter import ttk, messagebox

class RestaurantOrderManagement:
    def __init__(self, root):
        self.root = root  # The main window of an app
        self.root.title("Restaurant Order Management")  # Fixed typo in title
        # A dictionary to store the menu items and their prices
        self.menu_items = {
            "FRIES MEAL": 2,
            "BURGER MEAL": 2,
            "PIZZA MEAL": 3,
            "LUNCH MEAL": 4,
            "DINNER MEAL": 5,
            "BEVERAGE": 1
        }
        self.exchange_rate = 82  # EXCHANGE RATE FOR CURRENCY CONVERSION
        self.setup_background(root)  # SET UP BG IMAGE
        # CREATE A FRAME
        frame = ttk.Frame(root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Fixed typo (anchoor -> anchor)
        # PLACE IT AT THE CENTER OF THE WINDOW
        # CREATE A LABEL
        ttk.Label(frame, text="Restaurant Order Management", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)  # Fixed typo in the label text
        self.menu_labels = {}  # TO STORE REFERENCES TO MENU ITEMS LABELS
        self.menu_quantities = {}  # TO STORE REFERENCES TO QUANTITY ENTRY WIDGETS
        # CREATE LABELS AND ENTRY WIDGETS FOR EACH MENU ITEM
        for i, (item, price) in enumerate(self.menu_items.items(), start=1):
            label = ttk.Label(frame, text=f"{item} (${price}):", font=("Arial", 12))  # Fixed item formatting
            label.grid(row=i, column=0, padx=10, pady=10)
            self.menu_labels[item] = label
           
            quantity_entry = ttk.Entry(frame, width=5)
            quantity_entry.grid(row=i, column=1, padx=10, pady=10)
            self.menu_quantities[item] = quantity_entry
       
        # CURRENT SELECTION
        self.currency_var = tk.StringVar()
        ttk.Label(frame, text="Currency:", font=("Arial", 12)).grid(row=len(self.menu_items) + 1, column=0, padx=10, pady=5)
        # DROPDOWN FOR CURRENCY SELECTION
        currency_dropdown = ttk.Combobox(frame, textvariable=self.currency_var, state="readonly", width=18, values=("USD", "INR"))
        currency_dropdown.grid(row=len(self.menu_items) + 1, column=1, padx=10, pady=5)
        currency_dropdown.current(0)  # SET DEFAULT CURRENCY
        # UPDATE PRICES WHEN CURRENCY CHANGES
        self.currency_var.trace("w", self.update_menu_prices)
        # BUTTON TO CALCULATE TOTAL
        order_button = ttk.Button(frame,
                                  text="Place Order",
                                  command=self.place_order)
        order_button.grid(row=len(self.menu_items) + 2,
                          columnspan=3,
                          padx=10,
                          pady=10)

    # Method to set up the background image
    def setup_background(self, root):
        bg_width, bg_height = 800, 600
        canvas = tk.Canvas(root, width=bg_width, height=bg_height)
        canvas.pack()
        original_image = tk.PhotoImage(file="food.jpg")

        background_image = original_image.subsample(2, 2)  # Simplified subsampling, adjust as necessary
        canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
        canvas.image = background_image

    # Method to update the menu prices based on the selected currency
    def update_menu_prices(self, *args):
        currency = self.currency_var.get()
        symbol = "₹" if currency == "INR" else "$"
        rate = self.exchange_rate if currency == "INR" else 1
        for item, label in self.menu_labels.items():
            price = self.menu_items[item] * rate
            label.config(text=f"{item} ({symbol}{price}):")

    # Method to place an order
    def place_order(self):
        total_cost = 0
        order_summary = "Order Summary:\n"
        currency = self.currency_var.get()
        symbol = "₹" if currency == "INR" else "$"
        rate = self.exchange_rate if currency == "INR" else 1
        for item, entry in self.menu_quantities.items():
            quantity = entry.get()
            if quantity.isdigit():
                quantity = int(quantity)
                price = self.menu_items[item] * rate
                cost = quantity * price
                total_cost += cost
                if quantity > 0:
                    order_summary += f"{item}: {quantity} x {symbol}{price} = {symbol}{cost}\n"
        if total_cost > 0:
            order_summary += f"\nTotal Cost: {symbol}{total_cost}"
            messagebox.showinfo("Order Placed", order_summary)  # Show order summary in a message box
        else:
            # Show error if no items are ordered
            messagebox.showerror("Error", "Please order at least one item.")


# Main block to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantOrderManagement(root)
    root.geometry("800x600")  # Set the size of the window
    root.mainloop()  # Start the GUI loop
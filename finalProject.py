import tkinter as tk
from tkinter import ttk, messagebox


# Product class
class Product:
    def __init__(self, productID, name, basePrice, quantityInStock):
        self.productID = str(productID).strip()
        self.name = str(name).strip()
        self.basePrice = float(basePrice)
        self.quantityInStock = int(quantityInStock)

        if self.basePrice < 0:
            raise ValueError("Base price cannot be negative.")
        if self.quantityInStock < 0:
            raise ValueError("Quantity cannot be negative.")

    def update_quantity(self, newQuantity):
        newQuantity = int(newQuantity)
        if newQuantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantityInStock = newQuantity

    def apply_discount(self):
        q = self.quantityInStock

        if q > 50:
            discount = 0.0
        elif 20 <= q <= 50:
            discount = 0.05
        elif 10 <= q < 20:
            discount = 0.10
        else:
            discount = 0.20

        return self.basePrice * (1 - discount)

    def info(self):
        return {
            "id": self.productID,
            "name": self.name,
            "base_price": self.basePrice,
            "qty": self.quantityInStock,
            "discounted_price": self.apply_discount()
        }


# Inventory class
class Inventory:
    def __init__(self):
        self.products = {}   # productID -> Product
        self.totalRevenue = 0.0

    def add_product(self, product):
        if product.productID in self.products:
            raise ValueError("Product ID already exists.")
        self.products[product.productID] = product

    def findProduct(self, productID):
        productID = str(productID).strip()
        return self.products.get(productID)

    def sellProduct(self, productID, quantity):
        product = self.findProduct(productID)
        if product is None:
            raise ValueError("Product not found.")

        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Invalid quantity.")

        if quantity > product.quantityInStock:
            raise ValueError("Not enough stock.")

        priceEach = product.apply_discount()
        total = priceEach * quantity

        product.quantityInStock -= quantity
        self.totalRevenue += total
        return total

    def stock_value(self):
        total = 0
        for p in self.products.values():
            total += p.basePrice * p.quantityInStock
        return total

    def low_stock(self, threshold=10):
        low = []
        for p in self.products.values():
            if p.quantityInStock < threshold:
                low.append(p)
        return low

    def total_revenue(self):
        return self.totalRevenue

    def show_all(self):
        return [p.info() for p in self.products.values()]


# GUI
class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Inventory & Sales Management System")
        self.geometry("1000x600")

        self.inv = Inventory()
        self.build_ui()

    def build_ui(self):
        # -------- Top: Product Input --------
        top = ttk.LabelFrame(self, text="Product Input")
        top.pack(fill="x", padx=10, pady=10)

        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_price = tk.StringVar()
        self.var_qty = tk.StringVar()

        ttk.Label(top, text="Product ID:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(top, textvariable=self.var_id, width=20).grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(top, text="Name:").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        ttk.Entry(top, textvariable=self.var_name, width=25).grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(top, text="Base Price:").grid(row=1, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(top, textvariable=self.var_price, width=20).grid(row=1, column=1, padx=6, pady=6)

        ttk.Label(top, text="Quantity:").grid(row=1, column=2, padx=6, pady=6, sticky="w")
        ttk.Entry(top, textvariable=self.var_qty, width=25).grid(row=1, column=3, padx=6, pady=6)

        ttk.Button(top, text="Add Product", command=self.add_product).grid(row=0, column=4, padx=6, pady=6)
        ttk.Button(top, text="Update Quantity", command=self.update_quantity).grid(row=1, column=4, padx=6, pady=6)

        ttk.Button(top, text="Search Product", command=self.search_product).grid(row=0, column=5, padx=6, pady=6)
        ttk.Button(top, text="Clear", command=self.clear_inputs).grid(row=1, column=5, padx=6, pady=6)

        # -------- Middle: Sell Product --------
        mid = ttk.LabelFrame(self, text="Sell Product")
        mid.pack(fill="x", padx=10, pady=5)

        self.var_sell_id = tk.StringVar()
        self.var_sell_qty = tk.StringVar()

        ttk.Label(mid, text="Product ID:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(mid, textvariable=self.var_sell_id, width=20).grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(mid, text="Quantity to Sell:").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        ttk.Entry(mid, textvariable=self.var_sell_qty, width=20).grid(row=0, column=3, padx=6, pady=6)

        ttk.Button(mid, text="Sell", command=self.sell_product).grid(row=0, column=4, padx=6, pady=6)

        # -------- Bottom: Table + Reports --------
        bottom = ttk.Frame(self)
        bottom.pack(fill="both", expand=True, padx=10, pady=10)

        table_frame = ttk.LabelFrame(bottom, text="Products Table")
        table_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "name", "base_price", "qty", "discounted_price"),
            show="headings",
            height=16
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("base_price", text="Base Price")
        self.tree.heading("qty", text="Qty")
        self.tree.heading("discounted_price", text="Discounted Price")

        self.tree.column("id", width=90, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("base_price", width=110, anchor="center")
        self.tree.column("qty", width=70, anchor="center")
        self.tree.column("discounted_price", width=140, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        reports = ttk.LabelFrame(bottom, text="Reports (All Inventory Methods)")
        reports.pack(side="right", fill="y")

        ttk.Button(reports, text="Show All (show_all)", command=self.refresh_table).pack(fill="x", padx=10, pady=(10, 6))
        ttk.Button(reports, text="Stock Value (stock_value)", command=self.stock_value_popup).pack(fill="x", padx=10, pady=6)
        ttk.Button(reports, text="Low Stock (low_stock)", command=self.low_stock_popup).pack(fill="x", padx=10, pady=6)
        ttk.Button(reports, text="Total Revenue (total_revenue)", command=self.revenue_popup).pack(fill="x", padx=10, pady=6)

        self.status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status).pack(fill="x", padx=10, pady=(0, 10))

    # -------- Helpers --------
    def clear_inputs(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.status.set("Cleared inputs.")

    def on_row_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        self.var_id.set(values[0])
        self.var_name.set(values[1])
        self.var_price.set(values[2])
        self.var_qty.set(values[3])
        self.status.set(f"Selected product {values[0]}.")

    # -------- Table --------
    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for info in self.inv.show_all():
            self.tree.insert("", "end", values=(
                info["id"],
                info["name"],
                f"{info['base_price']:.2f}",
                info["qty"],
                f"{info['discounted_price']:.2f}"
            ))

        self.status.set("Table updated (show_all).")

    # -------- Actions --------
    def add_product(self):
        try:
            p = Product(
                self.var_id.get(),
                self.var_name.get(),
                self.var_price.get(),
                self.var_qty.get()
            )
            self.inv.add_product(p)
            self.refresh_table()
            self.status.set(f"Added product {p.productID}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_quantity(self):
        try:
            product = self.inv.findProduct(self.var_id.get())
            if product is None:
                raise ValueError("Product not found.")

            product.update_quantity(self.var_qty.get())
            self.refresh_table()
            self.status.set(f"Updated quantity for {product.productID}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_product(self):
        try:
            pid = self.var_id.get().strip()
            if not pid:
                raise ValueError("Enter Product ID to search.")

            product = self.inv.findProduct(pid)
            if product is None:
                messagebox.showinfo("Search", "Product not found.")
                return

            # fill fields
            self.var_id.set(product.productID)
            self.var_name.set(product.name)
            self.var_price.set(str(product.basePrice))
            self.var_qty.set(str(product.quantityInStock))

            messagebox.showinfo("Search", f"Found: {product.name}")
            self.status.set(f"findProduct: found {pid}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def sell_product(self):
        try:
            pid = self.var_sell_id.get().strip()
            qty = self.var_sell_qty.get().strip()
            if not pid or not qty:
                raise ValueError("Enter Product ID and Quantity to sell.")

            total = self.inv.sellProduct(pid, qty)
            self.refresh_table()
            messagebox.showinfo("Sell", f"Sale done!\nTotal = {total:.2f}")
            self.status.set(f"sellProduct: sold {qty} of {pid}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stock_value_popup(self):
        value = self.inv.stock_value()
        messagebox.showinfo("Stock Value", f"Total stock value = {value:.2f}")
        self.status.set("stock_value calculated.")

    def low_stock_popup(self):
        low = self.inv.low_stock(10)
        if not low:
            messagebox.showinfo("Low Stock", "No low stock products (qty < 10).")
            self.status.set("low_stock: none.")
            return

        text = ""
        for p in low:
            text += f"{p.productID} - {p.name} (qty: {p.quantityInStock})\n"

        messagebox.showwarning("Low Stock (<10)", text)
        self.status.set("low_stock shown.")

    def revenue_popup(self):
        rev = self.inv.total_revenue()
        messagebox.showinfo("Total Revenue", f"Total revenue = {rev:.2f}")
        self.status.set("total_revenue shown.")


if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()

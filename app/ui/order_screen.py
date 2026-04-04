# ui/order_screen.py
# Create new order: pick customer, add menu items, submit

import customtkinter as ctk
from tkinter import messagebox
from services.menu_service     import get_all_items
from services.customer_service import get_customer, add_customer
from services.billing_service  import create_order, add_item

COLORS = {
    "bg": "#0f1117", "card": "#1a1d2e", "accent": "#4f8ef7",
    "text": "#e2e8f0", "muted": "#64748b", "border": "#2d3148",
    "success": "#22c55e", "danger": "#ef4444",
}


class OrderScreen(ctk.CTkFrame):
    def __init__(self, parent, staff):
        super().__init__(parent, fg_color=COLORS["bg"])
        self.staff   = staff
        self.cart    = {}       # {item_id: {"name":..,"price":..,"qty":..}}
        self.order_id = None
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="🧾  New Order",
                     font=("Segoe UI", 24, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", pady=(0, 16))

        body = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=2)
        body.columnconfigure(1, weight=1)

        # LEFT: Customer + Menu
        left = ctk.CTkFrame(body, fg_color=COLORS["card"], corner_radius=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        # Customer section
        cust_frame = ctk.CTkFrame(left, fg_color="transparent")
        cust_frame.pack(fill="x", padx=20, pady=(18, 8))

        ctk.CTkLabel(cust_frame, text="Customer Details",
                     font=("Segoe UI", 14, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w")

        row1 = ctk.CTkFrame(cust_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(8, 0))
        ctk.CTkLabel(row1, text="Phone:", width=60, font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(side="left")
        self.ent_phone = ctk.CTkEntry(row1, width=160, height=36,
                                      placeholder_text="10-digit mobile",
                                      font=("Segoe UI", 12))
        self.ent_phone.pack(side="left", padx=(4, 8))
        ctk.CTkButton(row1, text="Lookup", width=80, height=36,
                      fg_color=COLORS["accent"], corner_radius=8,
                      command=self._lookup_customer).pack(side="left")

        row2 = ctk.CTkFrame(cust_frame, fg_color="transparent")
        row2.pack(fill="x", pady=6)
        ctk.CTkLabel(row2, text="Name:", width=60, font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(side="left")
        self.ent_name = ctk.CTkEntry(row2, width=220, height=36,
                                     placeholder_text="Customer name",
                                     font=("Segoe UI", 12))
        self.ent_name.pack(side="left", padx=4)

        row3 = ctk.CTkFrame(cust_frame, fg_color="transparent")
        row3.pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(row3, text="Table:", width=60, font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(side="left")
        self.ent_table = ctk.CTkEntry(row3, width=80, height=36,
                                      placeholder_text="No.",
                                      font=("Segoe UI", 12))
        self.ent_table.pack(side="left", padx=4)
        self.lbl_discount = ctk.CTkLabel(row3, text="",
                                          font=("Segoe UI", 12),
                                          text_color=COLORS["success"])
        self.lbl_discount.pack(side="left", padx=12)

        ctk.CTkFrame(left, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=20)

        # Menu items list
        ctk.CTkLabel(left, text="Menu Items",
                     font=("Segoe UI", 14, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=20, pady=(12, 4))

        self.menu_frame = ctk.CTkScrollableFrame(left, fg_color="transparent",
                                                  height=300)
        self.menu_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        self._load_menu()

        # RIGHT: Cart
        right = ctk.CTkFrame(body, fg_color=COLORS["card"], corner_radius=14)
        right.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(right, text="🛒  Cart",
                     font=("Segoe UI", 14, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=20, pady=(18, 8))

        self.cart_frame = ctk.CTkScrollableFrame(right, fg_color="transparent",
                                                  height=300)
        self.cart_frame.pack(fill="both", expand=True, padx=16)

        self.lbl_cart_total = ctk.CTkLabel(right, text="Total: ₹0.00",
                                            font=("Segoe UI", 16, "bold"),
                                            text_color=COLORS["text"])
        self.lbl_cart_total.pack(pady=12)

        ctk.CTkButton(right, text="✅  Place Order", height=48,
                      font=("Segoe UI", 14, "bold"),
                      fg_color=COLORS["success"], hover_color="#16a34a",
                      corner_radius=10,
                      command=self._place_order).pack(padx=20, pady=(0, 16), fill="x")

        ctk.CTkButton(right, text="🔄  Clear Cart", height=36,
                      font=("Segoe UI", 12),
                      fg_color=COLORS["border"], corner_radius=10,
                      command=self._clear_cart).pack(padx=20, pady=(0, 16), fill="x")

    def _load_menu(self):
        for w in self.menu_frame.winfo_children():
            w.destroy()
        try:
            items = get_all_items()
        except Exception as e:
            ctk.CTkLabel(self.menu_frame, text=f"Error: {e}",
                         text_color=COLORS["danger"]).pack()
            return

        current_cat = None
        for item in items:
            if item["category"] != current_cat:
                current_cat = item["category"]
                ctk.CTkLabel(self.menu_frame,
                             text=f"── {current_cat} ──",
                             font=("Segoe UI", 11, "bold"),
                             text_color=COLORS["muted"]).pack(anchor="w", pady=(8, 2))

            row = ctk.CTkFrame(self.menu_frame, fg_color=COLORS["border"],
                               corner_radius=8)
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(row, text=item["name"], width=160, anchor="w",
                         font=("Segoe UI", 12), text_color=COLORS["text"]).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"₹{item['price']:.0f}", width=60,
                         font=("Segoe UI", 12),
                         text_color=COLORS["success"]).pack(side="left")

            qty_var = ctk.IntVar(value=1)
            ctk.CTkLabel(row, text="Qty:", font=("Segoe UI", 11),
                         text_color=COLORS["muted"]).pack(side="left", padx=(8, 2))
            ctk.CTkEntry(row, textvariable=qty_var, width=40, height=28,
                         font=("Segoe UI", 12)).pack(side="left", padx=2)

            ctk.CTkButton(row, text="Add", width=52, height=28,
                          fg_color=COLORS["accent"], corner_radius=6,
                          font=("Segoe UI", 11),
                          command=lambda i=item, q=qty_var: self._add_to_cart(i, q)
                          ).pack(side="right", padx=8)

    def _add_to_cart(self, item, qty_var):
        qty = qty_var.get()
        if qty <= 0:
            messagebox.showerror("Invalid", "Quantity must be ≥ 1")
            return
        iid = item["item_id"]
        if iid in self.cart:
            self.cart[iid]["qty"] += qty
        else:
            self.cart[iid] = {"name": item["name"], "price": float(item["price"]), "qty": qty}
        self._refresh_cart()

    def _refresh_cart(self):
        for w in self.cart_frame.winfo_children():
            w.destroy()
        total = 0
        for iid, info in self.cart.items():
            sub = info["price"] * info["qty"]
            total += sub
            row = ctk.CTkFrame(self.cart_frame, fg_color=COLORS["border"],
                               corner_radius=6)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{info['name']} x{info['qty']}",
                         anchor="w", font=("Segoe UI", 12),
                         text_color=COLORS["text"]).pack(side="left", padx=8)
            ctk.CTkLabel(row, text=f"₹{sub:.0f}",
                         font=("Segoe UI", 12),
                         text_color=COLORS["success"]).pack(side="right", padx=8)
        self.lbl_cart_total.configure(text=f"Total: ₹{total:.2f}")

    def _clear_cart(self):
        self.cart.clear()
        self._refresh_cart()

    def _lookup_customer(self):
        phone = self.ent_phone.get().strip()
        if not phone:
            return
        try:
            rows = get_customer(phone)
            if rows:
                c = rows[0]
                self.ent_name.delete(0, "end")
                self.ent_name.insert(0, c["name"])
                disc = c["visit_count"]
                if disc >= 10:    pct = 15
                elif disc >= 5:   pct = 10
                elif disc >= 3:   pct = 5
                else:             pct = 0
                disc_txt = f"🏆 Visit #{disc} — {pct}% loyalty discount" if pct else f"Visit #{disc}"
                self.lbl_discount.configure(text=disc_txt)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _place_order(self):
        phone = self.ent_phone.get().strip()
        name  = self.ent_name.get().strip()
        table = self.ent_table.get().strip()

        if not phone or not name or not table:
            messagebox.showerror("Missing Info", "Phone, Name, and Table are required.")
            return
        if not self.cart:
            messagebox.showerror("Empty Cart", "Add at least one item.")
            return
        if not table.isdigit():
            messagebox.showerror("Invalid", "Table number must be numeric.")
            return

        try:
            order_id, msg = create_order(phone, name, self.staff["staff_id"], int(table))
            if order_id == -1:
                messagebox.showerror("Failed", msg)
                return

            for iid, info in self.cart.items():
                add_item(order_id, iid, info["qty"])

            messagebox.showinfo("Order Placed ✅",
                                f"Order #{order_id} placed!\nItems added: {len(self.cart)}\n\n"
                                "Go to Billing to generate the bill.")
            self.order_id = order_id
            self._clear_cart()
        except Exception as e:
            messagebox.showerror("Error", str(e))

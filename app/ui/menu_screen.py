# ui/menu_screen.py  — View / Add menu items

import customtkinter as ctk
from tkinter import messagebox
from services.menu_service import get_all_items, add_item, update_price

COLORS = {
    "bg":"#0f1117","card":"#1a1d2e","accent":"#4f8ef7",
    "text":"#e2e8f0","muted":"#64748b","border":"#2d3148",
    "success":"#22c55e","danger":"#ef4444",
}
CATEGORIES = ["Starter", "Main Course", "Dessert", "Beverage", "Snack"]


class MenuScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg"])
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="🍽  Menu Management",
                     font=("Segoe UI", 24, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", pady=(0, 16))

        body = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=2)
        body.columnconfigure(1, weight=1)

        # Menu list
        left = ctk.CTkFrame(body, fg_color=COLORS["card"], corner_radius=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(left, text="Current Menu",
                     font=("Segoe UI", 15, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=20, pady=(18, 8))

        # Headers
        hdr = ctk.CTkFrame(left, fg_color=COLORS["border"], corner_radius=6)
        hdr.pack(fill="x", padx=16, pady=(0, 4))
        for col, w in [("ID", 40), ("Name", 160), ("Category", 110), ("Price", 70), ("Tax %", 55)]:
            ctk.CTkLabel(hdr, text=col, width=w, font=("Segoe UI", 11, "bold"),
                         text_color=COLORS["muted"]).pack(side="left", padx=4, pady=6)

        self.menu_scroll = ctk.CTkScrollableFrame(left, fg_color="transparent")
        self.menu_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 12))
        self._refresh_menu()

        # Add new item form 
        right = ctk.CTkFrame(body, fg_color=COLORS["card"], corner_radius=14)
        right.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(right, text="Add Menu Item",
                     font=("Segoe UI", 15, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=20, pady=(18, 8))

        fields = [("Item Name", "name"), ("Price (₹)", "price"), ("Tax Rate (%)", "tax")]
        self._entries = {}
        for label, key in fields:
            ctk.CTkLabel(right, text=label, font=("Segoe UI", 12),
                         text_color=COLORS["muted"]).pack(anchor="w", padx=20, pady=(8, 0))
            e = ctk.CTkEntry(right, width=240, height=38, font=("Segoe UI", 12))
            e.pack(padx=20, pady=(2, 0))
            self._entries[key] = e

        ctk.CTkLabel(right, text="Category", font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(anchor="w", padx=20, pady=(8, 0))
        self.cat_var = ctk.CTkComboBox(right, values=CATEGORIES, width=240, height=38)
        self.cat_var.set("Main Course")
        self.cat_var.pack(padx=20, pady=(2, 12))

        ctk.CTkButton(right, text="➕  Add Item", height=44,
                      font=("Segoe UI", 13, "bold"),
                      fg_color=COLORS["accent"], corner_radius=10,
                      command=self._add_item).pack(padx=20, pady=8, fill="x")

    def _refresh_menu(self):
        for w in self.menu_scroll.winfo_children():
            w.destroy()
        try:
            items = get_all_items()
        except Exception as e:
            ctk.CTkLabel(self.menu_scroll, text=f"Error: {e}",
                         text_color=COLORS["danger"]).pack()
            return
        for item in items:
            row = ctk.CTkFrame(self.menu_scroll, fg_color=COLORS["border"],
                               corner_radius=6)
            row.pack(fill="x", pady=2)
            for val, w in [
                (str(item["item_id"]), 40),
                (item["name"], 160),
                (item["category"], 110),
                (f"₹{item['price']:.0f}", 70),
                (f"{item['tax_rate']}%", 55),
            ]:
                ctk.CTkLabel(row, text=val, width=w, anchor="w",
                             font=("Segoe UI", 11),
                             text_color=COLORS["text"]).pack(side="left", padx=4, pady=6)

    def _add_item(self):
        name  = self._entries["name"].get().strip()
        price = self._entries["price"].get().strip()
        tax   = self._entries["tax"].get().strip()
        cat   = self.cat_var.get()
        if not name or not price:
            messagebox.showerror("Missing", "Name and Price are required.")
            return
        try:
            add_item(name, cat, float(price), float(tax or 5))
            messagebox.showinfo("Added ✅", f'"{name}" added to menu.')
            for e in self._entries.values():
                e.delete(0, "end")
            self._refresh_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))

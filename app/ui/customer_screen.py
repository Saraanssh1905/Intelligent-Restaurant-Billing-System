# ui/customer_screen.py

import customtkinter as ctk
from tkinter import messagebox
from services.customer_service import get_all_customers, get_customer, add_customer, get_whatsapp_list

COLORS = {
    "bg":"#0f1117","card":"#1a1d2e","accent":"#4f8ef7",
    "text":"#e2e8f0","muted":"#64748b","border":"#2d3148",
    "success":"#22c55e","danger":"#ef4444","warning":"#f59e0b",
}


class CustomerScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg"])
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="👤  Customer Management",
                     font=("Segoe UI", 24, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", pady=(0, 16))

        body = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=2)
        body.columnconfigure(1, weight=1)

        # Customer table 
        left = ctk.CTkFrame(body, fg_color=COLORS["card"], corner_radius=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,10))

        # Search bar
        bar = ctk.CTkFrame(left, fg_color="transparent")
        bar.pack(fill="x", padx=20, pady=(16, 4))
        ctk.CTkLabel(bar, text="Search Phone:", font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(side="left")
        self.ent_search = ctk.CTkEntry(bar, width=160, height=36, font=("Segoe UI", 12))
        self.ent_search.pack(side="left", padx=6)
        ctk.CTkButton(bar, text="Search", width=80, height=36,
                      fg_color=COLORS["accent"], corner_radius=8,
                      command=self._search).pack(side="left")
        ctk.CTkButton(bar, text="All", width=60, height=36,
                      fg_color=COLORS["border"], corner_radius=8,
                      command=self._load_all).pack(side="left", padx=6)

        self.cust_scroll = ctk.CTkScrollableFrame(left, fg_color="transparent")
        self.cust_scroll.pack(fill="both", expand=True, padx=16, pady=(4, 16))
        self._load_all()

        # Add customer + WhatsApp list 
        right = ctk.CTkFrame(body, fg_color=COLORS["card"], corner_radius=14)
        right.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(right, text="Add Customer",
                     font=("Segoe UI", 14, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=20, pady=(18, 8))

        for label, key in [("Phone (10 digits)", "phone"), ("Name", "name")]:
            ctk.CTkLabel(right, text=label, font=("Segoe UI", 12),
                         text_color=COLORS["muted"]).pack(anchor="w", padx=20, pady=(8, 0))
            e = ctk.CTkEntry(right, width=240, height=38, font=("Segoe UI", 12))
            e.pack(padx=20)
            setattr(self, f"ent_{key}", e)

        ctk.CTkButton(right, text="➕  Add Customer", height=44,
                      font=("Segoe UI", 13, "bold"),
                      fg_color=COLORS["accent"], corner_radius=10,
                      command=self._add).pack(padx=20, pady=16, fill="x")

        ctk.CTkFrame(right, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=20)

        ctk.CTkLabel(right, text="📱  WhatsApp List",
                     font=("Segoe UI", 14, "bold"),
                     text_color=COLORS["success"]).pack(anchor="w", padx=20, pady=(14, 6))

        self.wa_frame = ctk.CTkScrollableFrame(right, fg_color="transparent", height=200)
        self.wa_frame.pack(fill="x", padx=16, pady=(0, 12))
        self._load_whatsapp()

    def _load_all(self):
        self._render_customers(get_all_customers())

    def _search(self):
        phone = self.ent_search.get().strip()
        if not phone:
            return
        self._render_customers(get_customer(phone))

    def _render_customers(self, rows):
        for w in self.cust_scroll.winfo_children():
            w.destroy()
        for c in rows:
            visits = c["visit_count"]
            if visits >= 10:  disc = "15% off"
            elif visits >= 5: disc = "10% off"
            elif visits >= 3: disc = "5% off"
            else:             disc = ""

            card = ctk.CTkFrame(self.cust_scroll, fg_color=COLORS["border"],
                                corner_radius=8)
            card.pack(fill="x", pady=3)
            ctk.CTkLabel(card,
                         text=f"{c['name']}  ({c['phone']})",
                         font=("Segoe UI", 13, "bold"),
                         text_color=COLORS["text"]).pack(anchor="w", padx=12, pady=(6,0))
            row2 = ctk.CTkFrame(card, fg_color="transparent")
            row2.pack(anchor="w", padx=12, pady=(2,6))
            ctk.CTkLabel(row2,
                         text=f"Visits: {visits}",
                         font=("Segoe UI", 11),
                         text_color=COLORS["muted"]).pack(side="left", padx=(0, 10))
            if disc:
                ctk.CTkLabel(row2, text=f"🏷 {disc}",
                             font=("Segoe UI", 11),
                             text_color=COLORS["warning"]).pack(side="left", padx=(0, 10))
            if c["on_whatsapp_list"]:
                ctk.CTkLabel(row2, text="📱 WhatsApp",
                             font=("Segoe UI", 11),
                             text_color=COLORS["success"]).pack(side="left")

    def _add(self):
        phone = self.ent_phone.get().strip()
        name  = self.ent_name.get().strip()
        if not phone or not name:
            messagebox.showerror("Missing", "Phone and Name required.")
            return
        try:
            add_customer(phone, name)
            messagebox.showinfo("Added ✅", f"Customer {name} registered.")
            self.ent_phone.delete(0, "end")
            self.ent_name.delete(0, "end")
            self._load_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _load_whatsapp(self):
        for w in self.wa_frame.winfo_children():
            w.destroy()
        try:
            rows = get_whatsapp_list()
            if not rows:
                ctk.CTkLabel(self.wa_frame, text="No customers yet.",
                             text_color=COLORS["muted"],
                             font=("Segoe UI", 11)).pack()
                return
            for c in rows:
                ctk.CTkLabel(self.wa_frame,
                             text=f"📱 {c['name']}  {c['phone']}  ({c['visit_count']} visits)",
                             font=("Segoe UI", 11),
                             text_color=COLORS["success"]).pack(anchor="w", pady=2)
        except Exception as e:
            ctk.CTkLabel(self.wa_frame, text=f"Error: {e}",
                         text_color=COLORS["danger"]).pack()

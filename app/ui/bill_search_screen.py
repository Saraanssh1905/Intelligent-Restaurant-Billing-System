# ui/bill_search_screen.py — Search bills by date / phone / staff

import customtkinter as ctk
from tkinter import messagebox
from services.billing_service import search_bills

COLORS = {
    "bg":"#0f1117","card":"#1a1d2e","accent":"#4f8ef7",
    "text":"#e2e8f0","muted":"#64748b","border":"#2d3148",
    "success":"#22c55e","danger":"#ef4444","warning":"#f59e0b",
}


class BillSearchScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg"])
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="🔍  Bill History Search",
                     font=("Segoe UI", 24, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", pady=(0, 16))

        # Filter bar
        filter_card = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=12)
        filter_card.pack(fill="x", pady=(0, 12))

        row = ctk.CTkFrame(filter_card, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(row, text="Date (YYYY-MM-DD):", font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(side="left")
        self.ent_date = ctk.CTkEntry(row, width=150, height=38,
                                     placeholder_text="leave blank for all",
                                     font=("Segoe UI", 12))
        self.ent_date.pack(side="left", padx=(4, 20))

        ctk.CTkLabel(row, text="Customer Phone:", font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(side="left")
        self.ent_phone = ctk.CTkEntry(row, width=150, height=38,
                                      placeholder_text="optional",
                                      font=("Segoe UI", 12))
        self.ent_phone.pack(side="left", padx=(4, 20))

        ctk.CTkLabel(row, text="Staff ID:", font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(side="left")
        self.ent_staff = ctk.CTkEntry(row, width=80, height=38,
                                      placeholder_text="opt.",
                                      font=("Segoe UI", 12))
        self.ent_staff.pack(side="left", padx=(4, 16))

        ctk.CTkButton(row, text="🔍  Search", width=110, height=38,
                      fg_color=COLORS["accent"], corner_radius=8,
                      font=("Segoe UI", 13, "bold"),
                      command=self._search).pack(side="left", padx=4)

        ctk.CTkButton(row, text="Show All", width=90, height=38,
                      fg_color=COLORS["border"], corner_radius=8,
                      font=("Segoe UI", 12),
                      command=self._show_all).pack(side="left", padx=4)

        self.lbl_count = ctk.CTkLabel(filter_card, text="",
                                       font=("Segoe UI", 12),
                                       text_color=COLORS["muted"])
        self.lbl_count.pack(anchor="w", padx=20, pady=(0, 8))

        # Results
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True)
        self._show_all()

    def _search(self):
        date  = self.ent_date.get().strip()  or None
        phone = self.ent_phone.get().strip() or None
        sid   = self.ent_staff.get().strip()
        staff_id = int(sid) if sid else None
        try:
            rows = search_bills(date=date, phone=phone, staff_id=staff_id)
            self._render_results(rows)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _show_all(self):
        try:
            rows = search_bills()
            self._render_results(rows)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _render_results(self, rows):
        for w in self.results_frame.winfo_children():
            w.destroy()
        self.lbl_count.configure(text=f"{len(rows)} bill(s) found")
        if not rows:
            ctk.CTkLabel(self.results_frame, text="No bills match your search.",
                         font=("Segoe UI", 13),
                         text_color=COLORS["muted"]).pack(pady=30)
            return
        for b in rows:
            status_color = {
                "Paid":     COLORS["success"],
                "Pending":  COLORS["warning"],
                "Refunded": COLORS["danger"],
            }.get(b.get("payment_status"), COLORS["muted"])

            card = ctk.CTkFrame(self.results_frame, fg_color=COLORS["card"],
                                corner_radius=10)
            card.pack(fill="x", pady=5)

            # Header row
            h = ctk.CTkFrame(card, fg_color=COLORS["border"], corner_radius=8)
            h.pack(fill="x", padx=8, pady=(8, 4))
            ctk.CTkLabel(h, text=f"Bill #{b['bill_id']}  |  Order #{b['order_id']}  |  "
                                  f"Table {b.get('table_no','')}  |  {b.get('generated_at','')}",
                         font=("Segoe UI", 12, "bold"),
                         text_color=COLORS["text"]).pack(side="left", padx=10, pady=6)
            ctk.CTkLabel(h, text=b.get("payment_status", ""),
                         font=("Segoe UI", 12, "bold"),
                         text_color=status_color).pack(side="right", padx=10)

            # Detail row
            d = ctk.CTkFrame(card, fg_color="transparent")
            d.pack(fill="x", padx=12, pady=(0, 8))
            details = [
                ("Customer", b.get("customer_name","") + "  " + b.get("customer_phone","")),
                ("Staff",    b.get("staff_name","")),
                ("Total",    f"₹{float(b['total_amount']):,.2f}"),
                ("Tax",      f"₹{float(b['tax_amount']):,.2f}"),
                ("Discount", f"{b.get('discount_applied',0)}%"),
            ]
            for label, val in details:
                ctk.CTkLabel(d, text=f"{label}: {val}",
                             font=("Segoe UI", 11),
                             text_color=COLORS["muted"]).pack(side="left", padx=12)

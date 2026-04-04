# ui/billing_screen.py
# Look up order → show bill → mark as Paid

import customtkinter as ctk
from tkinter import messagebox
from services.billing_service  import generate_bill, update_payment, search_bills, get_bill_detail
from services.report_service   import get_order_items

COLORS = {
    "bg":"#0f1117","card":"#1a1d2e","accent":"#4f8ef7",
    "text":"#e2e8f0","muted":"#64748b","border":"#2d3148",
    "success":"#22c55e","danger":"#ef4444","warning":"#f59e0b",
}


class BillingScreen(ctk.CTkFrame):
    def __init__(self, parent, staff):
        super().__init__(parent, fg_color=COLORS["bg"])
        self.staff   = staff
        self.bill_id = None
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="💳  Billing",
                     font=("Segoe UI", 24, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", pady=(0, 16))

        body = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)

        # LEFT: Generate bill
        left = ctk.CTkFrame(body, fg_color=COLORS["card"], corner_radius=14)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(left, text="Generate Bill",
                     font=("Segoe UI", 15, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=20, pady=(18, 8))

        r = ctk.CTkFrame(left, fg_color="transparent")
        r.pack(fill="x", padx=20, pady=4)
        ctk.CTkLabel(r, text="Order ID:", width=80,
                     font=("Segoe UI", 12), text_color=COLORS["muted"]).pack(side="left")
        self.ent_order = ctk.CTkEntry(r, width=120, height=36,
                                      placeholder_text="e.g. 5",
                                      font=("Segoe UI", 12))
        self.ent_order.pack(side="left", padx=4)
        ctk.CTkButton(r, text="Preview", width=88, height=36,
                      fg_color=COLORS["border"], corner_radius=8,
                      command=self._preview_order).pack(side="left", padx=4)

        self.lbl_preview = ctk.CTkLabel(left, text="",
                                         font=("Segoe UI", 12),
                                         text_color=COLORS["text"],
                                         justify="left")
        self.lbl_preview.pack(anchor="w", padx=20, pady=8)

        ctk.CTkButton(left, text="🧾  Generate Bill", height=46,
                      font=("Segoe UI", 13, "bold"),
                      fg_color=COLORS["accent"], corner_radius=10,
                      command=self._gen_bill).pack(padx=20, pady=8, fill="x")

        ctk.CTkFrame(left, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=20, pady=8)

        # Mark payment
        ctk.CTkLabel(left, text="Mark Payment",
                     font=("Segoe UI", 15, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=20, pady=(4, 8))

        r2 = ctk.CTkFrame(left, fg_color="transparent")
        r2.pack(fill="x", padx=20, pady=4)
        ctk.CTkLabel(r2, text="Bill ID:", width=80,
                     font=("Segoe UI", 12), text_color=COLORS["muted"]).pack(side="left")
        self.ent_bill = ctk.CTkEntry(r2, width=100, height=36,
                                     font=("Segoe UI", 12))
        self.ent_bill.pack(side="left", padx=4)

        self.pay_status = ctk.CTkComboBox(r2, values=["Paid", "Refunded"],
                                           width=110, height=36,
                                           font=("Segoe UI", 12))
        self.pay_status.set("Paid")
        self.pay_status.pack(side="left", padx=4)

        ctk.CTkButton(left, text="✅  Update Payment", height=46,
                      font=("Segoe UI", 13, "bold"),
                      fg_color=COLORS["success"], hover_color="#16a34a",
                      corner_radius=10,
                      command=self._pay).pack(padx=20, pady=8, fill="x")

        self.lbl_pay_msg = ctk.CTkLabel(left, text="",
                                         font=("Segoe UI", 12),
                                         text_color=COLORS["success"])
        self.lbl_pay_msg.pack(padx=20, pady=4)

        # Add rating
        ctk.CTkFrame(left, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=20, pady=8)
        ctk.CTkLabel(left, text="Customer Rating",
                     font=("Segoe UI", 14, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=20, pady=(4, 6))

        r3 = ctk.CTkFrame(left, fg_color="transparent")
        r3.pack(fill="x", padx=20, pady=4)
        ctk.CTkLabel(r3, text="Order ID:", width=80, font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(side="left")
        self.ent_rate_order = ctk.CTkEntry(r3, width=80, height=34, font=("Segoe UI", 12))
        self.ent_rate_order.pack(side="left", padx=4)
        ctk.CTkLabel(r3, text="Staff ID:", width=70, font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(side="left")
        self.ent_rate_staff = ctk.CTkEntry(r3, width=60, height=34, font=("Segoe UI", 12))
        self.ent_rate_staff.pack(side="left", padx=4)
        self.rating_var = ctk.CTkComboBox(r3, values=["5","4","3","2","1"],
                                           width=70, height=34, font=("Segoe UI", 12))
        self.rating_var.set("5")
        self.rating_var.pack(side="left", padx=4)
        ctk.CTkButton(r3, text="Rate", width=68, height=34,
                      fg_color=COLORS["warning"], corner_radius=8,
                      command=self._submit_rating).pack(side="left", padx=4)

        # RIGHT: Recent bills table
        right = ctk.CTkFrame(body, fg_color=COLORS["card"], corner_radius=14)
        right.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(right, text="Recent Bills",
                     font=("Segoe UI", 15, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=20, pady=(18, 8))

        self.bills_frame = ctk.CTkScrollableFrame(right, fg_color="transparent")
        self.bills_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        self._load_recent_bills()

    def _preview_order(self):
        oid = self.ent_order.get().strip()
        if not oid:
            return
        try:
            rows = get_order_items(int(oid))
            if not rows:
                self.lbl_preview.configure(text="No items found for this order.")
                return
            lines = [f"{'Item':<22} {'Qty':>4}  {'Amount':>8}"]
            lines.append("─" * 38)
            total = 0
            for r in rows:
                lines.append(f"{r['name']:<22} {r['quantity']:>4}  ₹{r['subtotal']:>6.2f}")
                total += float(r["subtotal"])
            lines.append("─" * 38)
            lines.append(f"{'Subtotal':>36} ₹{total:.2f}")
            self.lbl_preview.configure(text="\n".join(lines))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _gen_bill(self):
        oid = self.ent_order.get().strip()
        if not oid:
            messagebox.showerror("Missing", "Enter Order ID")
            return
        try:
            bid, msg = generate_bill(int(oid))
            if bid == -1:
                messagebox.showerror("Failed", msg)
            else:
                self.bill_id = bid
                self.ent_bill.delete(0, "end")
                self.ent_bill.insert(0, str(bid))
                messagebox.showinfo("Bill Generated ✅", msg)
                self._load_recent_bills()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _pay(self):
        bid    = self.ent_bill.get().strip()
        status = self.pay_status.get()
        if not bid:
            messagebox.showerror("Missing", "Enter Bill ID")
            return
        try:
            msg = update_payment(int(bid), status)
            color = COLORS["success"] if "updated" in msg.lower() else COLORS["danger"]
            self.lbl_pay_msg.configure(text=msg, text_color=color)
            self._load_recent_bills()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _submit_rating(self):
        oid = self.ent_rate_order.get().strip()
        sid = self.ent_rate_staff.get().strip()
        score = int(self.rating_var.get())
        if not oid or not sid:
            messagebox.showerror("Missing", "Enter Order ID and Staff ID.")
            return
        try:
            from services.staff_service import add_rating
            add_rating(int(sid), int(oid), score)
            messagebox.showinfo("Rating Added ✅", f"Rating {score}⭐ submitted for staff #{sid}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _load_recent_bills(self):
        for w in self.bills_frame.winfo_children():
            w.destroy()
        try:
            bills = search_bills()
            for b in bills[:15]:
                card = ctk.CTkFrame(self.bills_frame, fg_color=COLORS["border"],
                                    corner_radius=8)
                card.pack(fill="x", pady=3)
                status_color = COLORS["success"] if b.get("payment_status") == "Paid" else COLORS["warning"]
                ctk.CTkLabel(card,
                             text=f"Bill #{b['bill_id']}  |  Order #{b['order_id']}  |  {b.get('customer_name','')}",
                             font=("Segoe UI", 12, "bold"),
                             text_color=COLORS["text"]).pack(anchor="w", padx=10, pady=(6, 0))
                ctk.CTkLabel(card,
                             text=f"₹{b['total_amount']:.2f}   Tax: ₹{b['tax_amount']:.2f}   "
                                  f"Discount: {b['discount_applied']}%   [{b.get('payment_status','')}]",
                             font=("Segoe UI", 11),
                             text_color=status_color).pack(anchor="w", padx=10, pady=(0, 6))
        except Exception as e:
            ctk.CTkLabel(self.bills_frame, text=f"Error: {e}",
                         text_color=COLORS["danger"]).pack()

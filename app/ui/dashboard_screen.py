# ui/dashboard_screen.py
# Main navigation hub after login

import customtkinter as ctk
from datetime import datetime

from ui.order_screen     import OrderScreen
from ui.billing_screen   import BillingScreen
from ui.menu_screen      import MenuScreen
from ui.customer_screen  import CustomerScreen
from ui.staff_screen     import StaffScreen
from ui.analytics_screen import AnalyticsScreen
from ui.bill_search_screen import BillSearchScreen

COLORS = {
    "bg":     "#0f1117", "card":   "#1a1d2e",
    "accent": "#4f8ef7", "text":   "#e2e8f0",
    "muted":  "#64748b", "border": "#2d3148",
    "success":"#22c55e", "warning":"#f59e0b",
}

NAV_ITEMS = [
    ("🧾",  "New Order",      "order"),
    ("💳",  "Billing",        "billing"),
    ("🍽",  "Menu",           "menu"),
    ("👤",  "Customers",      "customer"),
    ("👨‍💼", "Staff & Shifts", "staff"),
    ("📊",  "Analytics",      "analytics"),
    ("🔍",  "Bill Search",    "search"),
]


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, staff, on_logout):
        super().__init__(parent, fg_color=COLORS["bg"])
        self.staff     = staff
        self.on_logout = on_logout
        self._build()
        self._show_section("order")

    def _build(self):
        # Sidebar
        sidebar = ctk.CTkFrame(self, fg_color=COLORS["card"], width=220,
                               corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="🍽", font=("Segoe UI", 38)).pack(pady=(28, 0))
        ctk.CTkLabel(sidebar, text="Restaurant", font=("Segoe UI", 14, "bold"),
                     text_color=COLORS["text"]).pack()
        ctk.CTkLabel(sidebar, text="Manager", font=("Segoe UI", 11),
                     text_color=COLORS["muted"]).pack(pady=(0, 20))

        ctk.CTkFrame(sidebar, height=1, fg_color=COLORS["border"]).pack(
            fill="x", padx=16, pady=(0, 12))

        self._nav_btns = {}
        for icon, label, key in NAV_ITEMS:
            btn = ctk.CTkButton(
                sidebar, text=f"  {icon}  {label}",
                anchor="w", width=190, height=44, corner_radius=10,
                font=("Segoe UI", 13), fg_color="transparent",
                hover_color=COLORS["border"], text_color=COLORS["text"],
                command=lambda k=key: self._show_section(k)
            )
            btn.pack(pady=3, padx=16)
            self._nav_btns[key] = btn

        # Staff info + logout at bottom
        ctk.CTkFrame(sidebar, height=1, fg_color=COLORS["border"]).pack(
            fill="x", padx=16, pady=(16, 8), side="bottom")
        ctk.CTkButton(sidebar, text="⎋  Logout", width=190, height=38,
                      corner_radius=10, fg_color=COLORS["border"],
                      hover_color="#3d4160", text_color=COLORS["text"],
                      command=self.on_logout, font=("Segoe UI", 12),
                      ).pack(side="bottom", padx=16, pady=(0, 12))
        ctk.CTkLabel(sidebar,
                     text=f"● {self.staff['name']}\n{self.staff['role']}",
                     font=("Segoe UI", 11), text_color=COLORS["success"],
                     justify="center").pack(side="bottom", pady=(0, 8))

        # Content area 
        self.content = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

    def _show_section(self, key: str):
        # Highlight active nav button
        for k, btn in self._nav_btns.items():
            btn.configure(fg_color=COLORS["accent"] if k == key else "transparent")

        # Clear content
        for w in self.content.winfo_children():
            w.destroy()

        frames = {
            "order":    lambda: OrderScreen(self.content, staff=self.staff),
            "billing":  lambda: BillingScreen(self.content, staff=self.staff),
            "menu":     lambda: MenuScreen(self.content),
            "customer": lambda: CustomerScreen(self.content),
            "staff":    lambda: StaffScreen(self.content),
            "analytics":lambda: AnalyticsScreen(self.content),
            "search":   lambda: BillSearchScreen(self.content),
        }
        widget = frames[key]()
        widget.pack(fill="both", expand=True, padx=20, pady=20)

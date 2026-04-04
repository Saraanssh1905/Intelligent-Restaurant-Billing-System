# main.py  — Application entry point
# Run:  python main.py   (from the app/ directory)

import sys
import os
import customtkinter as ctk

# Allow imports from app/
sys.path.insert(0, os.path.dirname(__file__))

from ui.login_screen    import LoginScreen
from ui.dashboard_screen import DashboardScreen

# ── Appearance ──────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Fonts (Google Fonts via system fallback) ─────────────────
FONT_TITLE  = ("Segoe UI", 28, "bold")
FONT_HEADER = ("Segoe UI", 18, "bold")
FONT_BODY   = ("Segoe UI", 13)
FONT_SMALL  = ("Segoe UI", 11)

COLORS = {
    "bg":       "#0f1117",
    "card":     "#1a1d2e",
    "accent":   "#4f8ef7",
    "success":  "#22c55e",
    "warning":  "#f59e0b",
    "danger":   "#ef4444",
    "text":     "#e2e8f0",
    "muted":    "#64748b",
    "border":   "#2d3148",
}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🍽  Intelligent Restaurant Billing & Management System")
        self.geometry("1280x800")
        self.minsize(1100, 700)
        self.configure(fg_color=COLORS["bg"])

        self.current_staff = None   # set on login
        self._frames = {}
        self._show_login()

    def _show_login(self):
        for w in self.winfo_children():
            w.destroy()
        frame = LoginScreen(self, on_login_success=self._on_login)
        frame.pack(fill="both", expand=True)

    def _on_login(self, staff_record):
        self.current_staff = staff_record
        for w in self.winfo_children():
            w.destroy()
        frame = DashboardScreen(self, staff=staff_record, on_logout=self._show_login)
        frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()

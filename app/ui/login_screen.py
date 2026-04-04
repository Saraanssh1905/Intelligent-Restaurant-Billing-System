# ui/login_screen.py
import customtkinter as ctk
from db_connection import execute_query

COLORS = {
    "bg":     "#0f1117", "card":  "#1a1d2e",
    "accent": "#4f8ef7", "text":  "#e2e8f0",
    "muted":  "#64748b", "danger":"#ef4444",
}


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent, fg_color=COLORS["bg"])
        self.on_login_success = on_login_success
        self._build()

    def _build(self):
        # Centered card
        outer = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        outer.place(relx=0.5, rely=0.5, anchor="center")

        card = ctk.CTkFrame(outer, fg_color=COLORS["card"], corner_radius=20,
                            width=420, height=480)
        card.pack(padx=40, pady=40)
        card.pack_propagate(False)

        # Logo area
        logo = ctk.CTkLabel(card, text="🍽", font=("Segoe UI", 52))
        logo.pack(pady=(40, 4))
        ctk.CTkLabel(card, text="Restaurant Manager",
                     font=("Segoe UI", 22, "bold"),
                     text_color=COLORS["text"]).pack()
        ctk.CTkLabel(card, text="Sign in to continue",
                     font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(pady=(2, 24))

        # Staff ID
        ctk.CTkLabel(card, text="Staff ID", font=("Segoe UI", 12, "bold"),
                     text_color=COLORS["muted"]).pack(anchor="w", padx=40)
        self.entry_id = ctk.CTkEntry(card, placeholder_text="e.g. 1",
                                     width=340, height=44, corner_radius=10,
                                     font=("Segoe UI", 13))
        self.entry_id.pack(padx=40, pady=(4, 16))

        # Password (role check — simplified for demo: password = name)
        ctk.CTkLabel(card, text="Password  (use your name)",
                     font=("Segoe UI", 12, "bold"),
                     text_color=COLORS["muted"]).pack(anchor="w", padx=40)
        self.entry_pw = ctk.CTkEntry(card, placeholder_text="Your name",
                                     width=340, height=44, corner_radius=10,
                                     font=("Segoe UI", 13), show="•")
        self.entry_pw.pack(padx=40, pady=(4, 8))

        self.lbl_error = ctk.CTkLabel(card, text="", text_color=COLORS["danger"],
                                      font=("Segoe UI", 11))
        self.lbl_error.pack()

        ctk.CTkButton(card, text="Sign In", width=340, height=46,
                      corner_radius=10, font=("Segoe UI", 14, "bold"),
                      fg_color=COLORS["accent"],
                      command=self._login).pack(padx=40, pady=(12, 0))

    def _login(self):
        staff_id = self.entry_id.get().strip()
        password = self.entry_pw.get().strip()
        if not staff_id or not password:
            self.lbl_error.configure(text="⚠ Please fill in both fields.")
            return
        try:
            rows = execute_query(
                "SELECT * FROM STAFF WHERE staff_id = %s",
                (staff_id,), fetch=True
            )
            if not rows:
                self.lbl_error.configure(text="❌ Staff ID not found.")
                return
            staff = rows[0]
            # Demo auth: password = first name (case-insensitive)
            if staff["name"].split()[0].lower() != password.lower():
                self.lbl_error.configure(text="❌ Incorrect password.")
                return
            self.on_login_success(staff)
        except Exception as e:
            self.lbl_error.configure(text=f"DB Error: {e}")

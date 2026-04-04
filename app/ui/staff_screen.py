# ui/staff_screen.py — Staff management, shifts, performance

import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from services.staff_service import (get_all_staff, add_staff, add_shift,
                                    get_shifts, get_top_staff, get_staff_performance)

COLORS = {
    "bg":"#0f1117","card":"#1a1d2e","accent":"#4f8ef7",
    "text":"#e2e8f0","muted":"#64748b","border":"#2d3148",
    "success":"#22c55e","danger":"#ef4444","warning":"#f59e0b",
}
ROLES = ["Manager", "Waiter", "Chef", "Cashier", "Host"]
ATT   = ["Present", "Absent", "Late", "Half-Day"]


class StaffScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg"])
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="👨‍💼  Staff & Shift Management",
                     font=("Segoe UI", 24, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", pady=(0, 16))

        tabs = ctk.CTkTabview(self, fg_color=COLORS["card"], corner_radius=14,
                              segmented_button_selected_color=COLORS["accent"])
        tabs.pack(fill="both", expand=True)

        tabs.add("👥 Staff List")
        tabs.add("➕ Add Staff")
        tabs.add("📅 Shifts")
        tabs.add("🏆 Performance")

        self._build_staff_list(tabs.tab("👥 Staff List"))
        self._build_add_staff(tabs.tab("➕ Add Staff"))
        self._build_shifts(tabs.tab("📅 Shifts"))
        self._build_performance(tabs.tab("🏆 Performance"))

    # Tab 1: Staff List
    def _build_staff_list(self, frame):
        self.staff_scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        self.staff_scroll.pack(fill="both", expand=True, padx=16, pady=16)
        self._refresh_staff()

    def _refresh_staff(self):
        for w in self.staff_scroll.winfo_children():
            w.destroy()
        try:
            staff = get_all_staff()
        except Exception as e:
            ctk.CTkLabel(self.staff_scroll, text=f"Error: {e}",
                         text_color=COLORS["danger"]).pack()
            return
        for s in staff:
            row = ctk.CTkFrame(self.staff_scroll, fg_color=COLORS["border"],
                               corner_radius=8)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row,
                         text=f"#{s['staff_id']}  {s['name']}  |  {s['role']}  |  ₹{s['salary']:,.0f}",
                         font=("Segoe UI", 12), text_color=COLORS["text"]
                         ).pack(anchor="w", padx=12, pady=8)

    # Tab 2: Add Staff
    def _build_add_staff(self, frame):
        wrapper = ctk.CTkFrame(frame, fg_color="transparent")
        wrapper.pack(padx=24, pady=24, fill="x")

        fields = [("Full Name", "name"), ("Salary (₹)", "salary")]
        self._sf_entries = {}
        for label, key in fields:
            ctk.CTkLabel(wrapper, text=label, font=("Segoe UI", 12),
                         text_color=COLORS["muted"]).pack(anchor="w", pady=(8, 0))
            e = ctk.CTkEntry(wrapper, width=280, height=40, font=("Segoe UI", 12))
            e.pack(anchor="w", pady=(2, 0))
            self._sf_entries[key] = e

        ctk.CTkLabel(wrapper, text="Role", font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(anchor="w", pady=(8, 0))
        self.sf_role = ctk.CTkComboBox(wrapper, values=ROLES, width=280, height=40)
        self.sf_role.set("Waiter")
        self.sf_role.pack(anchor="w", pady=(2, 14))

        ctk.CTkButton(wrapper, text="➕  Add Staff Member", height=44, width=280,
                      font=("Segoe UI", 13, "bold"),
                      fg_color=COLORS["accent"], corner_radius=10,
                      command=self._add_staff).pack(anchor="w")

    def _add_staff(self):
        name   = self._sf_entries["name"].get().strip()
        salary = self._sf_entries["salary"].get().strip()
        role   = self.sf_role.get()
        if not name or not salary:
            messagebox.showerror("Missing", "Name and Salary required.")
            return
        try:
            add_staff(name, role, float(salary))
            messagebox.showinfo("Added ✅", f"{role} '{name}' added.")
            for e in self._sf_entries.values():
                e.delete(0, "end")
            self._refresh_staff()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Tab 3: Shifts
    def _build_shifts(self, frame):
        col = ctk.CTkFrame(frame, fg_color="transparent")
        col.pack(fill="both", expand=True, padx=16, pady=16)

        top = ctk.CTkFrame(col, fg_color=COLORS["border"], corner_radius=10)
        top.pack(fill="x", pady=(0, 12))
        top.columnconfigure((0,1,2,3,4), weight=1)

        sf = [("Staff ID", "sid", 0), ("Date (YYYY-MM-DD)", "sdate", 1),
              ("Start (HH:MM)", "sstart", 2), ("End (HH:MM)", "send", 3)]
        self._sh_entries = {}
        for label, key, col_i in sf:
            fr = ctk.CTkFrame(top, fg_color="transparent")
            fr.grid(row=0, column=col_i, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(fr, text=label, font=("Segoe UI", 11),
                         text_color=COLORS["muted"]).pack(anchor="w")
            e = ctk.CTkEntry(fr, width=150, height=36, font=("Segoe UI", 12))
            e.pack()
            self._sh_entries[key] = e

        fr5 = ctk.CTkFrame(top, fg_color="transparent")
        fr5.grid(row=0, column=4, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(fr5, text="Attendance", font=("Segoe UI", 11),
                     text_color=COLORS["muted"]).pack(anchor="w")
        self.att_var = ctk.CTkComboBox(fr5, values=ATT, width=120, height=36)
        self.att_var.set("Present")
        self.att_var.pack()

        ctk.CTkButton(col, text="➕  Add Shift", height=40, width=180,
                      fg_color=COLORS["accent"], corner_radius=8,
                      font=("Segoe UI", 12, "bold"),
                      command=self._add_shift).pack(anchor="w", pady=(0, 12))

        self.shift_scroll = ctk.CTkScrollableFrame(col, fg_color="transparent")
        self.shift_scroll.pack(fill="both", expand=True)
        self._refresh_shifts()

    def _add_shift(self):
        sid    = self._sh_entries["sid"].get().strip()
        sdate  = self._sh_entries["sdate"].get().strip() or str(date.today())
        sstart = self._sh_entries["sstart"].get().strip()
        send   = self._sh_entries["send"].get().strip()
        att    = self.att_var.get()
        if not sid or not sstart or not send:
            messagebox.showerror("Missing", "Staff ID, Start, End times required.")
            return
        try:
            add_shift(int(sid), sdate, sstart+":00", send+":00", att)
            messagebox.showinfo("Added ✅", "Shift recorded.")
            self._refresh_shifts()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _refresh_shifts(self):
        for w in self.shift_scroll.winfo_children():
            w.destroy()
        try:
            shifts = get_shifts()
            for s in shifts[:30]:
                att_color = {
                    "Present": COLORS["success"],
                    "Absent":  COLORS["danger"],
                    "Late":    COLORS["warning"],
                    "Half-Day":COLORS["warning"],
                }.get(s["attendance_status"], COLORS["muted"])
                row = ctk.CTkFrame(self.shift_scroll, fg_color=COLORS["border"],
                                   corner_radius=6)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row,
                             text=f"{s['staff_name']}  ({s['role']})  —  {s['shift_date']}  "
                                  f"{s['start_time']} → {s['end_time']}",
                             font=("Segoe UI", 11), text_color=COLORS["text"]
                             ).pack(side="left", padx=10, pady=6)
                ctk.CTkLabel(row, text=s["attendance_status"],
                             font=("Segoe UI", 11, "bold"),
                             text_color=att_color).pack(side="right", padx=10)
        except Exception as e:
            ctk.CTkLabel(self.shift_scroll, text=f"Error: {e}",
                         text_color=COLORS["danger"]).pack()

    # Tab 4: Performance
    def _build_performance(self, frame):
        wrapper = ctk.CTkFrame(frame, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=16, pady=16)

        top = ctk.CTkFrame(wrapper, fg_color="transparent")
        top.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(top, text="Staff ID:", font=("Segoe UI", 12),
                     text_color=COLORS["muted"]).pack(side="left")
        self.ent_perf = ctk.CTkEntry(top, width=80, height=36, font=("Segoe UI", 12))
        self.ent_perf.pack(side="left", padx=6)
        ctk.CTkButton(top, text="Calculate", width=110, height=36,
                      fg_color=COLORS["accent"], corner_radius=8,
                      command=self._load_perf).pack(side="left")

        self.perf_lbl = ctk.CTkLabel(wrapper, text="",
                                      font=("Segoe UI", 13),
                                      text_color=COLORS["text"],
                                      justify="left")
        self.perf_lbl.pack(anchor="w", pady=12)

    def _load_perf(self):
        sid = self.ent_perf.get().strip()
        if not sid:
            return
        try:
            p = get_staff_performance(int(sid))
            if not p:
                self.perf_lbl.configure(text="No data found.")
                return
            text = (
                f"Name:          {p.get('name','—')}\n"
                f"Role:          {p.get('role','—')}\n"
                f"Total Orders:  {p.get('total_orders',0)}\n"
                f"Avg Rating:    {float(p.get('avg_rating',0)):.2f} ⭐\n"
                f"Total Revenue: ₹{float(p.get('total_revenue') or 0):,.2f}\n"
                f"Shifts Worked: {p.get('shifts_worked',0)}\n"
                f"Days Present:  {p.get('days_present',0)}"
            )
            self.perf_lbl.configure(text=text)
        except Exception as e:
            self.perf_lbl.configure(text=f"Error: {e}", text_color=COLORS["danger"])

# ui/analytics_screen.py — Daily/monthly sales + top staff

import customtkinter as ctk
from datetime import datetime
try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

from services.report_service import get_daily_sales, get_monthly_revenue, get_top_staff_view

COLORS = {
    "bg":"#0f1117","card":"#1a1d2e","accent":"#4f8ef7",
    "text":"#e2e8f0","muted":"#64748b","border":"#2d3148",
    "success":"#22c55e","danger":"#ef4444","warning":"#f59e0b",
}


class AnalyticsScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS["bg"])
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="📊  Sales Analytics",
                     font=("Segoe UI", 24, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", pady=(0, 12))

        tabs = ctk.CTkTabview(self, fg_color=COLORS["card"], corner_radius=14,
                              segmented_button_selected_color=COLORS["accent"])
        tabs.pack(fill="both", expand=True)
        tabs.add("📅 Daily Sales")
        tabs.add("📆 Monthly Revenue")
        tabs.add("🏆 Top Staff")

        self._build_daily(tabs.tab("📅 Daily Sales"))
        self._build_monthly(tabs.tab("📆 Monthly Revenue"))
        self._build_top_staff(tabs.tab("🏆 Top Staff"))

    # Daily Sales 
    def _build_daily(self, frame):
        try:
            rows = get_daily_sales()
        except Exception as e:
            ctk.CTkLabel(frame, text=f"Error: {e}",
                         text_color=COLORS["danger"]).pack(padx=20, pady=20)
            return

        if HAS_MPL and rows:
            dates   = [str(r["sale_date"]) for r in rows][::-1]
            revenue = [float(r["total_revenue"]) for r in rows][::-1]

            fig, ax = plt.subplots(figsize=(7, 3.5))
            fig.patch.set_facecolor("#1a1d2e")
            ax.set_facecolor("#1a1d2e")
            ax.bar(dates, revenue, color="#4f8ef7", width=0.5)
            ax.set_xlabel("Date", color="#64748b", fontsize=9)
            ax.set_ylabel("Revenue (₹)", color="#64748b", fontsize=9)
            ax.set_title("Daily Revenue", color="#e2e8f0", fontsize=12)
            ax.tick_params(colors="#64748b", labelrotation=30)
            for spine in ax.spines.values():
                spine.set_edgecolor("#2d3148")
            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="x", padx=16, pady=(12, 0))

        # Table below chart
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent", height=180)
        scroll.pack(fill="both", expand=True, padx=16, pady=8)
        hdr = ctk.CTkFrame(scroll, fg_color=COLORS["border"], corner_radius=6)
        hdr.pack(fill="x", pady=(0, 4))
        for col in ["Date", "Bills", "Revenue (₹)", "Tax (₹)", "Avg Bill"]:
            ctk.CTkLabel(hdr, text=col, width=110, font=("Segoe UI", 11, "bold"),
                         text_color=COLORS["muted"]).pack(side="left", padx=4, pady=6)
        for r in rows:
            row = ctk.CTkFrame(scroll, fg_color=COLORS["border"], corner_radius=6)
            row.pack(fill="x", pady=2)
            for val in [str(r["sale_date"]), str(r["total_bills"]),
                        f"₹{float(r['total_revenue']):,.2f}",
                        f"₹{float(r['total_tax']):,.2f}",
                        f"₹{float(r['avg_bill_value']):,.2f}"]:
                ctk.CTkLabel(row, text=val, width=110, font=("Segoe UI", 11),
                             text_color=COLORS["text"]).pack(side="left", padx=4, pady=6)

    # Monthly Revenue
    def _build_monthly(self, frame):
        try:
            rows = get_monthly_revenue()
        except Exception as e:
            ctk.CTkLabel(frame, text=f"Error: {e}",
                         text_color=COLORS["danger"]).pack(padx=20, pady=20)
            return

        if HAS_MPL and rows:
            labels  = [f"{r['month_name'][:3]} {r['year']}" for r in rows][::-1]
            revenue = [float(r["total_revenue"]) for r in rows][::-1]

            fig, ax = plt.subplots(figsize=(7, 3.5))
            fig.patch.set_facecolor("#1a1d2e")
            ax.set_facecolor("#1a1d2e")
            ax.plot(labels, revenue, color="#22c55e", linewidth=2.5, marker="o", markersize=6)
            ax.fill_between(labels, revenue, alpha=0.15, color="#22c55e")
            ax.set_title("Monthly Revenue Trend", color="#e2e8f0", fontsize=12)
            ax.tick_params(colors="#64748b", labelrotation=20)
            for spine in ax.spines.values():
                spine.set_edgecolor("#2d3148")
            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="x", padx=16, pady=(12, 0))

        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent", height=160)
        scroll.pack(fill="both", expand=True, padx=16, pady=8)
        for r in rows:
            row = ctk.CTkFrame(scroll, fg_color=COLORS["border"], corner_radius=6)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row,
                         text=f"{r['month_name']} {r['year']}  |  "
                              f"Bills: {r['total_bills']}  |  Revenue: ₹{float(r['total_revenue']):,.2f}",
                         font=("Segoe UI", 12), text_color=COLORS["text"]
                         ).pack(anchor="w", padx=12, pady=7)

    # Top Staff
    def _build_top_staff(self, frame):
        try:
            rows = get_top_staff_view()
        except Exception as e:
            ctk.CTkLabel(frame, text=f"Error: {e}",
                         text_color=COLORS["danger"]).pack(padx=20, pady=20)
            return

        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=16)

        hdr = ctk.CTkFrame(scroll, fg_color=COLORS["border"], corner_radius=6)
        hdr.pack(fill="x", pady=(0, 6))
        for col, w in [("Rank", 50), ("Name", 160), ("Role", 100),
                       ("Orders", 70), ("Avg Rating ⭐", 110), ("Revenue", 110)]:
            ctk.CTkLabel(hdr, text=col, width=w, font=("Segoe UI", 11, "bold"),
                         text_color=COLORS["muted"]).pack(side="left", padx=6, pady=6)

        medals = ["🥇", "🥈", "🥉"]
        for i, s in enumerate(rows):
            row = ctk.CTkFrame(scroll, fg_color=COLORS["border"], corner_radius=6)
            row.pack(fill="x", pady=3)
            medal = medals[i] if i < 3 else f"#{i+1}"
            for val, w in [
                (medal, 50),
                (s["staff_name"], 160),
                (s["role"], 100),
                (str(s["orders_served"]), 70),
                (f"{float(s['avg_rating']):.2f}", 110),
                (f"₹{float(s['revenue_generated'] or 0):,.0f}", 110),
            ]:
                color = COLORS["warning"] if i == 0 else COLORS["text"]
                ctk.CTkLabel(row, text=val, width=w, font=("Segoe UI", 12),
                             text_color=color).pack(side="left", padx=6, pady=8)

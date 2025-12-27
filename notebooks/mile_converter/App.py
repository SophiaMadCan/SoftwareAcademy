import tkinter as tk
from tkinter import ttk, messagebox


def miles_to_units(miles: float) -> dict:
    meters = miles * 1609.344
    return {
        "Kilometers (km)": meters / 1000,
        "Meters (m)": meters,
        "Centimeters (cm)": meters * 100,
        "Millimeters (mm)": meters * 1000,
        "Feet (ft)": miles * 5280,
        "Yards (yd)": miles * 1760,
        "Inches (in)": miles * 63360,
        "Nautical miles (nmi)": miles / 1.150779448,
    }


def parse_miles(text: str) -> float:
    # Defensive cleanup for weird whitespace characters (including NBSP)
    cleaned = text.replace("\u00a0", " ").strip().replace(",", "")
    if cleaned == "":
        raise ValueError("Please enter a value in miles.")
    miles = float(cleaned)
    if miles < 0:
        raise ValueError("Miles cannot be negative.")
    return miles


def format_number(value: float) -> str:
    s = f"{value:,.6f}".rstrip("0").rstrip(".")
    return s if s else "0"


class MilesConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Miles Converter")
        self.minsize(560, 420)
        self.configure(padx=16, pady=16)
        self._build_ui()

    def _build_ui(self):
        header = ttk.Label(
            self,
            text="Miles to Multiple Units Converter",
            font=("Segoe UI", 16, "bold"),
        )
        header.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        ttk.Label(self, text="Miles:").grid(row=1, column=0, sticky="w")

        self.miles_entry = ttk.Entry(self, width=24)
        self.miles_entry.grid(row=1, column=1, sticky="w", padx=(8, 8))
        self.miles_entry.focus_set()

        convert_btn = ttk.Button(self, text="Convert", command=self.on_convert)
        convert_btn.grid(row=1, column=2, sticky="w")

        help_text = ttk.Label(
            self,
            text="Tip: Use decimals and commas (e.g., 1,234.5). Press Enter to convert.",
            foreground="#444",
        )
        help_text.grid(row=2, column=0, columnspan=3, sticky="w", pady=(6, 12))

        columns = ("unit", "value")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.heading("unit", text="Unit")
        self.tree.heading("value", text="Value")
        self.tree.column("unit", width=240, anchor="w")
        self.tree.column("value", width=260, anchor="e")
        self.tree.grid(row=3, column=0, columnspan=3, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=3, sticky="ns", padx=(8, 0))

        self.status_var = tk.StringVar(self, value="Enter miles and click Convert.")
        status = ttk.Label(self, textvariable=self.status_var)
        status.grid(row=4, column=0, columnspan=3, sticky="w", pady=(12, 0))

        clear_btn = ttk.Button(self, text="Clear", command=self.on_clear)
        clear_btn.grid(row=4, column=2, sticky="e", pady=(12, 0))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Bind Enter ONLY when the miles entry has focus
        self.miles_entry.bind("<Return>", lambda _: self.on_convert())
        self.bind("<Escape>", lambda _: self.on_clear())

    def on_convert(self):
        # Read directly from the Entry widget (most reliable)
        raw_text = self.miles_entry.get()

        try:
            miles = parse_miles(raw_text)
            conversions = miles_to_units(miles)
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            self.status_var.set("Please enter a valid, non-negative number.")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for unit, value in conversions.items():
            self.tree.insert("", "end", values=(unit, format_number(value)))

        self.status_var.set(
            f"Converted {format_number(miles)} miles into {len(conversions)} units."
        )

    def on_clear(self):
        self.miles_entry.delete(0, tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.status_var.set("Enter miles and click Convert.")
        self.miles_entry.focus_set()


if __name__ == "__main__":
    app = MilesConverterApp()
    app.mainloop()

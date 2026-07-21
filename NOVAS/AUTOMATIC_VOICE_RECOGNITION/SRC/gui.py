"""
@Module Name : gui.py

@Description : Professional static GUI for NOVA Voice Assistant.

@Author : Bhoomi Sapke
"""

import tkinter as tk
from config import ASSISTANT_NAME


class NovaGUI:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(ASSISTANT_NAME)
        self.root.geometry("580x380")
        self.root.resizable(False, False)
        self.root.configure(bg="#EAF0F6")

        # ---------------- Header ----------------

        header = tk.Frame(
            self.root,
            bg="#355C7D",
            height=65
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="NOVA Voice Assistant",
            font=("Segoe UI", 22, "bold"),
            bg="#355C7D",
            fg="white"
        ).pack(pady=15)

        # ---------------- Main Card ----------------

        card = tk.Frame(
            self.root,
            bg="white",
            relief="ridge",
            bd=1
        )

        card.pack(
            padx=25,
            pady=20,
            fill="both",
            expand=True
        )

        tk.Label(
            card,
            text="Assistant Status",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#2F3542"
        ).pack(pady=(20, 8))

        tk.Label(
            card,
            text="● Running",
            font=("Segoe UI", 18, "bold"),
            fg="#2E8B57",
            bg="white"
        ).pack()

        tk.Label(
            card,
            text="Wake Word",
            font=("Segoe UI", 11),
            fg="#6C757D",
            bg="white"
        ).pack(pady=(20, 3))

        tk.Label(
            card,
            text='"Hello Nova"',
            font=("Segoe UI", 15, "bold"),
            fg="#355C7D",
            bg="white"
        ).pack()

        tk.Label(
            card,
            text="Ready to receive your voice command.",
            font=("Segoe UI", 11),
            fg="#6C757D",
            bg="white"
        ).pack(pady=(20, 20))

        # ---------------- Footer ----------------

        tk.Label(
            card,
            text="Industrial Training Project • NOVA Assistant",
            font=("Segoe UI", 9),
            bg="white",
            fg="#6C757D"
        ).pack(side="bottom", pady=12)

    def run(self):
        self.root.mainloop()
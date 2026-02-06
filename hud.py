from __future__ import annotations

import threading
import tkinter as tk

from .system_monitor import SystemMonitor


class HudWindow:
    """Minimal futuristic HUD window using Tkinter."""

    def __init__(self, monitor: SystemMonitor):
        self.monitor = monitor

    def open_async(self) -> None:
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self) -> None:
        root = tk.Tk()
        root.title("JARVIS HUD")
        root.geometry("700x120")
        root.configure(bg="#040b14")

        label = tk.Label(
            root,
            text="",
            fg="#3ef8ff",
            bg="#040b14",
            font=("Consolas", 13, "bold"),
        )
        label.pack(padx=10, pady=25)

        def refresh() -> None:
            snap = self.monitor.snapshot()
            label.config(text=self.monitor.format_snapshot(snap))
            root.after(1400, refresh)

        refresh()
        root.mainloop()

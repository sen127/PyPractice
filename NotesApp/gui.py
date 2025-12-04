"""Tkinter front end for the CLI note manager.

This keeps the original CLI script intact while providing a lightweight
GUI with a dropdown to choose the desired action.
"""

from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import Notes as notes_cli


class NoteManagerUI(tk.Tk):
    """Simple Tkinter UI that reuses the CLI helper utilities."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Note Manager")
        self.geometry("640x520")

        self.action_labels = {
            "list": "List notes",
            "read": "Read a note",
            "create": "Create / overwrite a note",
            "append": "Append to a note",
        }
        self.current_files = []

        self.action_var = tk.StringVar(value=self.action_labels["read"])
        self.note_name_var = tk.StringVar()

        self._build_widgets()
        self.refresh_notes()
        self.update_fields()

    def _build_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        for row in range(1, 4):
            self.rowconfigure(row, weight=1)

        action_frame = ttk.Frame(self, padding=12)
        action_frame.grid(row=0, column=0, sticky="ew")
        action_frame.columnconfigure(1, weight=1)

        ttk.Label(action_frame, text="Choose an action:").grid(
            row=0, column=0, sticky="w"
        )
        combo = ttk.Combobox(
            action_frame,
            textvariable=self.action_var,
            state="readonly",
            values=list(self.action_labels.values()),
        )
        combo.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        combo.bind("<<ComboboxSelected>>", self.update_fields)

        self.note_frame = ttk.LabelFrame(self, text="Existing notes", padding=12)
        self.note_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 8))
        self.note_frame.columnconfigure(0, weight=1)
        self.note_frame.rowconfigure(0, weight=1)

        self.note_list = tk.Listbox(self.note_frame, height=6, exportselection=False)
        self.note_list.grid(row=0, column=0, sticky="nsew")
        self.note_list.bind("<<ListboxSelect>>", lambda *_: None)

        note_scroll = ttk.Scrollbar(
            self.note_frame, orient="vertical", command=self.note_list.yview
        )
        note_scroll.grid(row=0, column=1, sticky="ns")
        self.note_list.configure(yscrollcommand=note_scroll.set)

        refresh_btn = ttk.Button(
            self.note_frame, text="Refresh list", command=self.refresh_notes
        )
        refresh_btn.grid(row=1, column=0, columnspan=2, pady=(8, 0), sticky="ew")

        self.name_frame = ttk.Frame(self, padding=(12, 0))
        self.name_frame.grid(row=2, column=0, sticky="ew")
        self.name_frame.columnconfigure(1, weight=1)

        ttk.Label(self.name_frame, text="New note name:").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        ttk.Entry(self.name_frame, textvariable=self.note_name_var).grid(
            row=0, column=1, sticky="ew"
        )

        text_frame = ttk.LabelFrame(self, text="Note content", padding=12)
        text_frame.grid(row=3, column=0, sticky="nsew", padx=12, pady=8)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.text = tk.Text(text_frame, wrap="word")
        self.text.grid(row=0, column=0, sticky="nsew")
        text_scroll = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.text.yview
        )
        text_scroll.grid(row=0, column=1, sticky="ns")
        self.text.configure(yscrollcommand=text_scroll.set)

        button_frame = ttk.Frame(self, padding=12)
        button_frame.grid(row=4, column=0, sticky="ew")
        ttk.Button(
            button_frame, text="Run action", command=self.execute_action
        ).grid(row=0, column=0, sticky="w")

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(self, textvariable=self.status_var, padding=(12, 0, 12, 12)).grid(
            row=5, column=0, sticky="ew"
        )

    def current_action(self) -> str:
        label = self.action_var.get()
        for key, value in self.action_labels.items():
            if value == label:
                return key
        return "read"

    def update_fields(self, *_: object) -> None:
        action = self.current_action()

        if action in {"create", "append"}:
            self.text.config(state="normal")
            if action == "create":
                self.text.delete("1.0", tk.END)
        else:
            self.text.config(state="disabled")

        if action in {"list", "read", "append"}:
            self.note_frame.grid()
        else:
            self.note_frame.grid_remove()

        if action == "create":
            self.name_frame.grid()
        else:
            self.name_frame.grid_remove()

        msg = {
            "list": "Refresh to see all files, then run the action.",
            "read": "Select a note and run the action to view it.",
            "create": "Enter a name plus body text, then run the action.",
            "append": "Select a note, enter extra text, then run the action.",
        }[action]
        self.set_status(msg)

    def refresh_notes(self, select: str | None = None) -> None:
        try:
            self.current_files = notes_cli.get_note_files()
        except Exception as exc:  # pragma: no cover - Tk UI helper
            messagebox.showerror("Error", f"Could not list notes: {exc}")
            return

        self.note_list.delete(0, tk.END)
        for file in self.current_files:
            self.note_list.insert(tk.END, file.name)

        if not self.current_files:
            self.note_list.configure(state="disabled")
        else:
            self.note_list.configure(state="normal")

        if select:
            for idx, file in enumerate(self.current_files):
                if file.name == select:
                    self.note_list.selection_clear(0, tk.END)
                    self.note_list.selection_set(idx)
                    self.note_list.see(idx)
                    break
        elif self.current_files and not self.note_list.curselection():
            self.note_list.selection_set(0)

    def selected_note(self) -> Path | None:
        if not self.current_files:
            return None
        selection = self.note_list.curselection()
        if not selection:
            return None
        return self.current_files[selection[0]]

    def execute_action(self) -> None:
        action = self.current_action()
        if action == "list":
            self.handle_list()
        elif action == "read":
            self.handle_read()
        elif action == "create":
            self.handle_create()
        elif action == "append":
            self.handle_append()

    def handle_list(self) -> None:
        self.refresh_notes()
        lines = [
            f"{idx + 1}. {path.name} ({path.stat().st_size} bytes)"
            for idx, path in enumerate(self.current_files)
        ]
        text = "\n".join(lines) if lines else "No notes found."
        self._write_text(text, editable=False)
        self.set_status("Listed available notes.")

    def handle_read(self) -> None:
        note = self.selected_note()
        if not note:
            messagebox.showinfo("Select a note", "Please choose a note first.")
            return
        content = (
            note.read_text(encoding="utf-8") if note.stat().st_size else "(empty)"
        )
        self._write_text(content, editable=False)
        self.set_status(f"Showing {note.name}.")

    def handle_create(self) -> None:
        name = self.note_name_var.get().strip()
        if not name:
            messagebox.showinfo("Missing name", "Enter a note name.")
            return
        text = self.text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Missing text", "Enter some text for the note.")
            return

        note_path = notes_cli.NOTES_DIR / notes_cli.ensure_suffix(name)
        note_path.write_text(text + "\n", encoding="utf-8")
        self.set_status(f"Saved {note_path.name}.")
        self.refresh_notes(select=note_path.name)

    def handle_append(self) -> None:
        note = self.selected_note()
        if not note:
            messagebox.showinfo("Select a note", "Choose a note to append to.")
            return
        text = self.text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Missing text", "Enter text to append.")
            return

        with note.open("a", encoding="utf-8") as fh:
            fh.write("\n" + text + "\n")
        self.text.delete("1.0", tk.END)
        self.set_status(f"Appended to {note.name}.")

    def _write_text(self, content: str, *, editable: bool) -> None:
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, content)
        self.text.config(state="normal" if editable else "disabled")

    def set_status(self, message: str) -> None:
        self.status_var.set(message)


def main() -> None:
    app = NoteManagerUI()
    app.mainloop()


if __name__ == "__main__":
    main()

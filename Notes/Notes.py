#TODO write a program using which I can write notes in files and read from them, so it basically creates a file or access the same and edit, read etc.."""Simple CLI utility for creating, reading, and updating text notes.
"""Notes are stored next to this script (in the Notes directory). The tool
supports listing available notes, reading an existing note, creating a
new one, and appending additional text to an existing note.
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import List, Optional
NOTES_DIR = Path(__file__).resolve().parent
DEFAULT_SUFFIX = ".txt"
def get_note_files() -> List[Path]:
    """Return all note files (text-like, skip .py) sorted by name."""
    files = [
        path
        for path in NOTES_DIR.iterdir()
        if path.is_file() and path.suffix != ".py"
    ]
    return sorted(files, key=lambda p: p.name.lower())
def ensure_suffix(name: str) -> str:
    """Ensure filenames have a suffix; default to .txt."""
    path = Path(name.strip())
    if not path.suffix:
        path = path.with_suffix(DEFAULT_SUFFIX)
    return path.name
def prompt_for_text(action: str) -> str:
    """Capture multi-line text input that ends on an empty line."""
    print(f"\n{action}")
    print("Enter text. Submit an empty line to finish.\n")
    lines: List[str] = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if not line:
            break
        lines.append(line)
    return "\n".join(lines).strip()
def prompt_for_note_name(
    prompt: str, *, must_exist: bool, allow_overwrite: bool = False
) -> Optional[Path]:
    """Ask the user for a note name and validate existence rules."""
    while True:
        raw = input(f"{prompt} ").strip()
        if not raw:
            print("Cancelled.\n")
            return None
        if any(sep in raw for sep in ("/", "\\")):
            print("Please enter only a file name, not a path.")
            continue
        candidate = NOTES_DIR / ensure_suffix(raw)
        exists = candidate.exists()
        if must_exist and not exists:
            print("That note does not exist. Try again.")
            continue
        if not must_exist and exists and not allow_overwrite:
            choice = input("Note exists. Overwrite? [y/N]: ").strip().lower()
            if choice != "y":
                print("Pick a different name.\n")
                continue
        return candidate
def list_notes() -> None:
    files = get_note_files()
    if not files:
        print("\nNo notes found. Create one from the menu!\n")
        return
    print("\nAvailable notes:")
    for idx, file in enumerate(files, start=1):
        size = file.stat().st_size
        print(f" {idx:>2}. {file.name} ({size} bytes)")
    print()
def select_note() -> Optional[Path]:
    files = get_note_files()
    if not files:
        print("\nNo notes to select. Create one first.\n")
        return None
    list_notes()
    choice = input("Select a note by number or name: ").strip()
    if not choice:
        print("Cancelled.\n")
        return None
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(files):
            return files[idx - 1]
        print("Invalid selection.\n")
        return None
    candidate = NOTES_DIR / ensure_suffix(choice)
    if candidate.exists():
        return candidate
    print("Note not found.\n")
    return None
def read_note() -> None:
    note = select_note()
    if not note:
        return
    print(f"\n--- {note.name} ---")
    content = note.read_text(encoding="utf-8") if note.stat().st_size else ""
    print(content if content else "(empty)")
    print("-" * (len(note.name) + 8) + "\n")
def create_note() -> None:
    note_path = prompt_for_note_name(
        "Enter a name for the new note:", must_exist=False
    )
    if not note_path:
        return
    text = prompt_for_text("Add the body of your note:")
    if not text:
        print("No text entered; note not saved.\n")
        return
    note_path.write_text(text + "\n", encoding="utf-8")
    print(f"Saved {note_path.name}.\n")
def append_to_note() -> None:
    note = select_note()
    if not note:
        return
    text = prompt_for_text(f"Append text to {note.name}:")
    if not text:
        print("No text entered; nothing changed.\n")
        return
    with note.open("a", encoding="utf-8") as fh:
        fh.write("\n" + text + "\n")
    print(f"Updated {note.name}.\n")
def main() -> None:
    actions = {
        "1": ("List notes", list_notes),
        "2": ("Read a note", read_note),
        "3": ("Create / overwrite a note", create_note),
        "4": ("Append to a note", append_to_note),
        "0": ("Exit", None),
    }
    while True:
        print("Note Manager")
        for key, (label, _) in actions.items():
            print(f" {key}. {label}")
        choice = input("Choose an option: ").strip()
        action = actions.get(choice)
        if not action:
            print("Invalid option. Try again.\n")
            continue
        if choice == "0":
            print("Goodbye!")
            return
        _, handler = action
        handler()
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
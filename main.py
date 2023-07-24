import os
import json
import time
import keyboard
import tkinter as tk
from tkinter import messagebox


class PhrasesManager:
    def __init__(self):
        self.file_path = './texts.json'
        self.frases = {}
        self.hotkey = tk.StringVar()
        self.text = tk.StringVar()
        self.hook_ids = {}
        self.load_phrases()
        self.bind_keys()

    def load_phrases(self):
        try:
            with open(self.file_path, 'r', encoding="utf-8") as file:
                self.frases = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.frases = {}

    def show_phrases(self):
        phrases_window = tk.Toplevel()
        phrases_window.configure(bg="#282c44")
        phrases_window.title("Registered Phrases")
        phrases_window.geometry("160x220")
        phrases_listbox = tk.Listbox(
            phrases_window, selectmode=tk.SINGLE, background="#282c34", foreground="white")
        phrases_listbox.pack()

        for key, phrase in self.frases.items():
            phrases_listbox.insert(tk.END, f"Key {key}: {phrase}")

        delete_button = tk.Button(
            phrases_window, text="Delete", command=lambda: self.delete_phrase(phrases_listbox), background="#282c34", foreground="white")
        delete_button.pack()

    def delete_phrase(self, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            selected_key = listbox.get(selected_index[0]).split()[
                1].replace(':', '')
            del self.frases[selected_key]
            with open(self.file_path, 'w', encoding="utf-8") as file:
                json.dump(self.frases, file)
            listbox.delete(selected_index)
        else:
            messagebox.showinfo("Warning", "Please select a phrase to delete.")

    def create_phrase(self):
        self.unbind_keys()
        create_phrase_window = tk.Toplevel()
        create_phrase_window.configure(bg="#282c34")
        create_phrase_window.title("Create New Message")
        create_phrase_window.geometry("200x120")

        label = tk.Label(create_phrase_window, text="Hotkey:",
                         background="#282c34", foreground="white")
        label.pack()

        hotkey_entry = tk.Entry(
            create_phrase_window, textvariable=self.hotkey, state='readonly', width=5)
        hotkey_entry.bind("<KeyPress>", self.get_hotkey)
        hotkey_entry.pack()

        label = tk.Label(create_phrase_window, text="Message:",
                         width=150, background="#282c34", foreground="white")
        label.pack()

        text_entry = tk.Entry(create_phrase_window,
                              textvariable=self.text, state='normal', background="#282c34", foreground="white")
        text_entry.pack()

        save_button = tk.Button(
            create_phrase_window, text="Save", command=self.save_message(create_phrase_window))
        save_button.pack()

    def unbind_keys(self):
        for _, hook_id in self.hook_ids.items():
            keyboard.unhook(hook_id)

    def get_hotkey(self, event=None):
        key = event.keysym
        self.hotkey.set(key)

    def save_message(self, window):
        def save_and_close():
            hotkey = self.hotkey.get()
            text = self.text.get()
            self.frases[hotkey] = text
            with open(self.file_path, 'w', encoding="utf-8") as file:
                json.dump(self.frases, file)
            window.destroy()
            self.bind_keys()

        return save_and_close

    def write_phrase(self, key):
        if key not in self.frases:
            return

        phrase = self.frases[key]

        time.sleep(0.01)
        keyboard.press_and_release("shift+enter")
        time.sleep(0.01)
        keyboard.write(phrase)
        keyboard.press_and_release('enter')

    def bind_keys(self):
        for key, _ in self.frases.items():
            self.callback(key)

    def callback(self, key):
        hook_id = keyboard.on_press_key(key, lambda _: self.write_phrase(key))
        self.hook_ids[key] = hook_id


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PQZIN-MACRO")
        self.configure(bg='#282c34')
        self.phrases_manager = PhrasesManager()
        self.create_widgets()

    def create_widgets(self):

        title = """====================================
PQZIN-MACRO TO LEAGUE OF LEGENDS
==================================================="""
        help_label = tk.Label(self, text=title,
                              background="#282c34", foreground="white")
        help_label.pack()

        phrases_button = tk.Button(
            self, text="Show Registered Phrases", command=self.phrases_manager.show_phrases, background="#282c34", foreground="white")
        phrases_button.pack()

        create_phrase_button = tk.Button(
            self, text="Create New Phrase", command=self.phrases_manager.create_phrase, background="#282c34", foreground="white")
        create_phrase_button.pack()

    def on_exit(self):
        if messagebox.askyesno("Exit", "Do you want to exit the program?"):
            self.destroy()


def main():
    app = Application()
    app.resizable(False, False)
    app.protocol("WM_DELETE_WINDOW", app.on_exit)
    app.mainloop()


if __name__ == "__main__":
    main()

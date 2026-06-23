from tkinter import *
from tkinter import filedialog, messagebox
from Encryption import encrypt_file, decrypt_file
from Database import log_action, view_logs
import os

FONT = ("Consolas", 12)
TITLE_FONT = ("Consolas", 16, "bold")
BG_COLOR = "#95B8DE"
GOLD = "#024310"
DARK_GOLD = "#024310"
TEXT_COLOR = "#2B2B2B"
ENTRY_BG = "#ADACE8"


def browse_file():
    path = filedialog.askopenfilename()
    if path:
        file_entry.delete(0, END)
        file_entry.insert(0, path)


def encrypt_action():
    filepath = file_entry.get().strip()
    password = password_entry.get()

    if not os.path.exists(filepath):
        messagebox.showerror("Error", "File not found!")
        log_action(filepath, "ENCRYPT", "FAILED - File not found")
        return

    result = encrypt_file(filepath, password)
    if result:
        log_action(os.path.basename(filepath), "ENCRYPT", "SUCCESS")
        messagebox.showinfo("Success", f"File encrypted:\n{result}")


def decrypt_action():
    filepath = file_entry.get().strip()
    password = password_entry.get()

    if not os.path.exists(filepath):
        messagebox.showerror("Error", "File not found!")
        log_action(filepath, "DECRYPT", "FAILED - File not found")
        return

    result = decrypt_file(filepath, password)
    if result:
        log_action(os.path.basename(filepath), "DECRYPT", "SUCCESS")
        messagebox.showinfo("Success", f"File decrypted:\n{result}")
    else:
        log_action(os.path.basename(filepath), "DECRYPT", "FAILED - Wrong password")
        messagebox.showerror("Error", "Wrong password or corrupted file!")


def logs_action():
    view_logs()
    messagebox.showinfo("Logs", "Logs printed in the terminal.")


root = Tk()
root.title("File Encryption System")
root.geometry("450x340")
root.configure(bg=BG_COLOR)

Label(root, text="File Encryption System", font=TITLE_FONT, bg=BG_COLOR, fg=DARK_GOLD).pack(pady=15)

Label(root, text="File path:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack()
file_frame = Frame(root, bg=BG_COLOR)
file_frame.pack(pady=5)
file_entry = Entry(file_frame, width=32, font=FONT, bg=ENTRY_BG, fg=TEXT_COLOR)
file_entry.pack(side=LEFT, padx=5)
Button(file_frame, text="Browse", font=FONT, command=browse_file, bg=GOLD, fg=TEXT_COLOR).pack(side=LEFT)

Label(root, text="Password:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(10, 0))
password_entry = Entry(root, show="*", font=FONT, width=25, bg=ENTRY_BG, fg=TEXT_COLOR)
password_entry.pack(pady=5)

btn_frame = Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=20)
Button(btn_frame, text="Encrypt", font=FONT, width=10, command=encrypt_action, bg=GOLD, fg=TEXT_COLOR).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Decrypt", font=FONT, width=10, command=decrypt_action, bg=GOLD, fg=TEXT_COLOR).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Logs", font=FONT, width=10, command=logs_action, bg=GOLD, fg=TEXT_COLOR).grid(row=0, column=2, padx=5)
Button(btn_frame, text="Exit", font=FONT, width=32, command=root.destroy, bg=DARK_GOLD, fg=BG_COLOR).grid(row=1, column=0, columnspan=3, pady=10)

root.mainloop()
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from Encryption import encrypt_file, decrypt_file
from Database import log_action, view_logs


# ─── Colour palette ──────────────────────────────────────────────────────────
BG       = "#1e2330"
PANEL    = "#252b3b"
ACCENT   = "#4f8ef7"
SUCCESS  = "#3ddc97"
DANGER   = "#ff6b6b"
FG       = "#e0e6f0"
FG_DIM   = "#8892a4"
ENTRY_BG = "#2e3650"
BTN_FG   = "#ffffff"


# ─── Helper widgets ──────────────────────────────────────────────────────────
def styled_button(parent, text, command, color=ACCENT, width=22):
    return tk.Button(
        parent, text=text, command=command,
        bg=color, fg=BTN_FG, activebackground=color,
        font=("Segoe UI", 10, "bold"), relief="flat",
        cursor="hand2", width=width, pady=6
    )


def labeled_entry(parent, label_text, show=""):
    tk.Label(parent, text=label_text, bg=PANEL, fg=FG_DIM,
             font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 2))
    var = tk.StringVar()
    entry = tk.Entry(parent, textvariable=var, bg=ENTRY_BG, fg=FG,
                     insertbackground=FG, relief="flat", font=("Segoe UI", 10),
                     show=show)
    entry.pack(fill="x", ipady=6, padx=2)
    return var


# ─── Main application ────────────────────────────────────────────────────────
class FileEncryptionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Encryption System  🔐")
        self.geometry("660x540")
        self.resizable(False, False)
        self.configure(bg=BG)

        self._build_header()
        self._build_notebook()
        self._build_status_bar()

    # ── Header ───────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=ACCENT, height=54)
        hdr.pack(fill="x")
        tk.Label(hdr, text="  🔐  FILE ENCRYPTION SYSTEM",
                 bg=ACCENT, fg=BTN_FG,
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=12, pady=10)
        tk.Label(hdr, text="Ethical Hacking – Semester 1",
                 bg=ACCENT, fg="#d0e4ff",
                 font=("Segoe UI", 9)).pack(side="right", padx=14)

    # ── Notebook tabs ─────────────────────────────────────────────────────────
    def _build_notebook(self):
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TNotebook",       background=BG,    borderwidth=0)
        style.configure("TNotebook.Tab",   background=PANEL, foreground=FG_DIM,
                        padding=[18, 8],   font=("Segoe UI", 10))
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", BTN_FG)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=14, pady=12)

        self._build_encrypt_tab(nb)
        self._build_decrypt_tab(nb)
        self._build_logs_tab(nb)

    # ── Encrypt tab ───────────────────────────────────────────────────────────
    def _build_encrypt_tab(self, nb):
        frame = tk.Frame(nb, bg=PANEL)
        nb.add(frame, text="  Encrypt  ")

        inner = tk.Frame(frame, bg=PANEL, padx=28, pady=18)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text="Select a file to encrypt",
                 bg=PANEL, fg=FG, font=("Segoe UI", 11, "bold")).pack(anchor="w")

        # File path row
        self.enc_path = tk.StringVar()
        row = tk.Frame(inner, bg=PANEL)
        row.pack(fill="x", pady=(10, 0))
        tk.Entry(row, textvariable=self.enc_path, bg=ENTRY_BG, fg=FG,
                 insertbackground=FG, relief="flat",
                 font=("Segoe UI", 10)).pack(side="left", fill="x",
                                             expand=True, ipady=6)
        tk.Button(row, text=" Browse ", command=self._browse_encrypt,
                  bg="#3a4460", fg=FG, relief="flat",
                  font=("Segoe UI", 9), cursor="hand2").pack(side="left", padx=(6, 0), ipady=6)

        self.enc_pass = labeled_entry(inner, "Password", show="•")

        tk.Frame(inner, bg=PANEL, height=14).pack()
        styled_button(inner, "🔒  Encrypt File", self._do_encrypt, color=ACCENT).pack()

    # ── Decrypt tab ───────────────────────────────────────────────────────────
    def _build_decrypt_tab(self, nb):
        frame = tk.Frame(nb, bg=PANEL)
        nb.add(frame, text="  Decrypt  ")

        inner = tk.Frame(frame, bg=PANEL, padx=28, pady=18)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text="Select an encrypted (.enc) file to decrypt",
                 bg=PANEL, fg=FG, font=("Segoe UI", 11, "bold")).pack(anchor="w")

        self.dec_path = tk.StringVar()
        row = tk.Frame(inner, bg=PANEL)
        row.pack(fill="x", pady=(10, 0))
        tk.Entry(row, textvariable=self.dec_path, bg=ENTRY_BG, fg=FG,
                 insertbackground=FG, relief="flat",
                 font=("Segoe UI", 10)).pack(side="left", fill="x",
                                             expand=True, ipady=6)
        tk.Button(row, text=" Browse ", command=self._browse_decrypt,
                  bg="#3a4460", fg=FG, relief="flat",
                  font=("Segoe UI", 9), cursor="hand2").pack(side="left", padx=(6, 0), ipady=6)

        self.dec_pass = labeled_entry(inner, "Password", show="•")

        tk.Frame(inner, bg=PANEL, height=14).pack()
        styled_button(inner, "🔓  Decrypt File", self._do_decrypt, color="#7c5cbf").pack()

    # ── Logs tab ──────────────────────────────────────────────────────────────
    def _build_logs_tab(self, nb):
        frame = tk.Frame(nb, bg=PANEL)
        nb.add(frame, text="  Logs  ")

        inner = tk.Frame(frame, bg=PANEL, padx=14, pady=14)
        inner.pack(fill="both", expand=True)

        btn_row = tk.Frame(inner, bg=PANEL)
        btn_row.pack(fill="x", pady=(0, 10))
        styled_button(btn_row, "🔄  Refresh Logs", self._load_logs, width=18).pack(side="left")

        # Treeview
        cols = ("ID", "Filename", "Action", "Status", "Date")
        style = ttk.Style()
        style.configure("Treeview",
                        background=ENTRY_BG, fieldbackground=ENTRY_BG,
                        foreground=FG, rowheight=24,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        background=ACCENT, foreground=BTN_FG,
                        font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", ACCENT)])

        self.tree = ttk.Treeview(inner, columns=cols, show="headings", height=12)
        widths = (40, 200, 90, 120, 150)
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        scroll = ttk.Scrollbar(inner, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="left", fill="y")

        self._load_logs()

    # ── Status bar ────────────────────────────────────────────────────────────
    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="Ready")
        bar = tk.Label(self, textvariable=self.status_var,
                       bg="#161b27", fg=FG_DIM,
                       font=("Segoe UI", 9), anchor="w", padx=10)
        bar.pack(fill="x", side="bottom", ipady=4)

    def _set_status(self, msg, color=FG_DIM):
        self.status_var.set(msg)

    # ── Actions ───────────────────────────────────────────────────────────────
    def _browse_encrypt(self):
        path = filedialog.askopenfilename(title="Select file to encrypt")
        if path:
            self.enc_path.set(path)

    def _browse_decrypt(self):
        path = filedialog.askopenfilename(title="Select .enc file",
                                          filetypes=[("Encrypted files", "*.enc"),
                                                     ("All files", "*.*")])
        if path:
            self.dec_path.set(path)

    def _do_encrypt(self):
        filepath = self.enc_path.get().strip()
        password = self.enc_pass.get()

        if not filepath:
            messagebox.showwarning("Missing File", "Please select a file to encrypt.")
            return
        if not os.path.exists(filepath):
            messagebox.showerror("File Not Found", f"Cannot find:\n{filepath}")
            log_action(filepath, "ENCRYPT", "FAILED - File not found")
            return
        if not password:
            messagebox.showwarning("Missing Password", "Please enter a password.")
            return

        result = encrypt_file(filepath, password)
        if result:
            log_action(os.path.basename(filepath), "ENCRYPT", "SUCCESS")
            messagebox.showinfo("Success 🔒", f"File encrypted successfully!\n\nSaved as:\n{result}")
            self._set_status(f"Encrypted: {os.path.basename(result)}")
            self.enc_path.set("")
            self.enc_pass.set("")
        else:
            log_action(os.path.basename(filepath), "ENCRYPT", "FAILED")
            messagebox.showerror("Error", "Encryption failed. Check the console for details.")

    def _do_decrypt(self):
        filepath = self.dec_path.get().strip()
        password = self.dec_pass.get()

        if not filepath:
            messagebox.showwarning("Missing File", "Please select a .enc file to decrypt.")
            return
        if not os.path.exists(filepath):
            messagebox.showerror("File Not Found", f"Cannot find:\n{filepath}")
            log_action(filepath, "DECRYPT", "FAILED - File not found")
            return
        if not password:
            messagebox.showwarning("Missing Password", "Please enter a password.")
            return

        result = decrypt_file(filepath, password)
        if result:
            log_action(os.path.basename(filepath), "DECRYPT", "SUCCESS")
            messagebox.showinfo("Success 🔓", f"File decrypted successfully!\n\nSaved as:\n{result}")
            self._set_status(f"Decrypted: {os.path.basename(result)}")
            self.dec_path.set("")
            self.dec_pass.set("")
        else:
            log_action(os.path.basename(filepath), "DECRYPT", "FAILED - Wrong password")
            messagebox.showerror("Wrong Password", "Decryption failed.\nThe password may be incorrect or the file is corrupted.")

    def _load_logs(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            import mysql.connector
            from Database import connect_db
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM encryption_logs ORDER BY id DESC")
            for i, row in enumerate(cursor.fetchall()):
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=row, tags=(tag,))
            self.tree.tag_configure("even", background=ENTRY_BG)
            self.tree.tag_configure("odd",  background="#262d42")
            conn.close()
            self._set_status("Logs refreshed.")
        except Exception as e:
            messagebox.showerror("Database Error",
                                 f"Could not load logs:\n{e}\n\n"
                                 "Make sure MySQL is running and Database.py credentials are correct.")


# ─── Entry point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = FileEncryptionApp()
    app.mainloop()
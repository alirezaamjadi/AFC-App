import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
from datetime import datetime
import webbrowser

class FolderCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Folder Creator Alireza")
        self.geometry("700x850")
        self.resizable(False, False)

        style = ttk.Style(self)
        self.configure(bg="#1e1e2f")

        style.theme_use('clam')

        style.configure('TButton', font=('Arial', 12), padding=10, background="#2e86de", foreground="#f9ca24")
        style.configure('TLabel', font=('Arial', 12), background="#1e1e2f", foreground="#f5f6fa")
        style.configure('Header.TLabel', font=('Arial', 18, 'bold'), foreground="#f9ca24", background="#1e1e2f")
        style.configure('TEntry', padding=5, fieldbackground="#353b48", foreground="#ffffff")

        self.folder_entries = []
        self.folder_path = ''

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Folder Creator Alireza", style='Header.TLabel').pack(pady=25)

        path_frame = ttk.Frame(self)
        path_frame.pack(pady=15)

        self.path_label = ttk.Label(path_frame, text="مسیر انتخاب نشده")
        self.path_label.pack(side=tk.LEFT, padx=10)

        ttk.Button(path_frame, text="📂 انتخاب مسیر", command=self.select_path).pack(side=tk.RIGHT)

        count_frame = ttk.Frame(self)
        count_frame.pack(pady=20)

        ttk.Label(count_frame, text="تعداد پوشه‌ها (حداکثر 10):").pack(side=tk.LEFT, padx=10)
        self.count_entry = ttk.Entry(count_frame, width=5)
        self.count_entry.pack(side=tk.LEFT)

        ttk.Button(count_frame, text="تایید", command=self.generate_folder_inputs).pack(side=tk.LEFT, padx=10)

        self.folders_frame = ttk.Frame(self)
        self.folders_frame.pack(pady=15, fill=tk.X, padx=20)

        self.create_button = ttk.Button(self, text="🚀 ساخت پوشه‌ها", command=self.create_folders, state=tk.DISABLED)
        self.create_button.pack(pady=20)

        self.open_button = ttk.Button(self, text="📁 باز کردن محل پوشه‌ها", command=self.open_folder, state=tk.DISABLED)
        self.open_button.pack(pady=15)

        github_btn = ttk.Button(self, text="💻 GitHub: alirezaamjadi", command=self.open_github)
        github_btn.pack(pady=15)

        fullscreen_btn = ttk.Button(self, text="🖥️ حالت تمام صفحه", command=self.toggle_fullscreen)
        fullscreen_btn.pack(pady=15)

    def toggle_fullscreen(self):
        is_fullscreen = self.attributes('-fullscreen')
        self.attributes('-fullscreen', not is_fullscreen)

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path = path
            self.path_label.config(text=path)

    def generate_folder_inputs(self):
        for widget in self.folders_frame.winfo_children():
            widget.destroy()

        try:
            count = int(self.count_entry.get())
            if count <= 0 or count > 10:
                raise ValueError
        except:
            messagebox.showerror("❗ خطا", "لطفا عددی معتبر بین 1 تا 10 وارد کنید")
            return

        self.folder_entries = []

        for i in range(count):
            entry_frame = ttk.Frame(self.folders_frame)
            entry_frame.pack(pady=5, fill=tk.X)

            label = ttk.Label(entry_frame, text=f"نام پوشه {i+1}:")
            label.pack(side=tk.LEFT, padx=5)

            entry = ttk.Entry(entry_frame, width=50)
            entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            self.folder_entries.append(entry)

        self.create_button.config(state=tk.NORMAL)

    def create_folders(self):
        if not self.folder_path:
            messagebox.showerror("❗ خطا", "لطفا مسیر پوشه را انتخاب کنید.")
            return

        for idx, entry in enumerate(self.folder_entries, start=1):
            name = entry.get().strip()
            if not name:
                messagebox.showerror("❗ خطا", f"نام پوشه {idx} خالی است. لطفا تکمیل کنید.")
                return

        for name in [e.get().strip() for e in self.folder_entries]:
            folder_dir = os.path.join(self.folder_path, name)
            os.makedirs(folder_dir, exist_ok=True)

            info_path = os.path.join(folder_dir, "info.txt")
            now = datetime.now()
            with open(info_path, 'w', encoding='utf-8') as f:
                f.write(f"Folder Created\n")
                f.write(f"ساعت : {now.strftime('%H:%M:%S')}\n")
                f.write(f"تاریخ : {now.strftime('%Y-%m-%d')}\n")
                f.write(f"نام پوشه : {name}\n")

        messagebox.showinfo("🎉 موفقیت", f"{len(self.folder_entries)} پوشه با موفقیت ساخته شد!")
        self.open_button.config(state=tk.NORMAL)

    def open_folder(self):
        if self.folder_path:
            if os.name == 'nt':
                subprocess.run(['explorer', self.folder_path])
            elif os.name == 'posix':
                subprocess.run(['xdg-open', self.folder_path])
            else:
                messagebox.showwarning("خطا", "باز کردن مسیر در این سیستم‌عامل پشتیبانی نمی‌شود.")

    def open_github(self):
        webbrowser.open_new_tab("https://github.com/alirezaamjadi")

if __name__ == '__main__':
    app = FolderCreatorApp()
    app.mainloop()

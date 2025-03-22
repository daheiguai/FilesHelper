import tkinter as tk
from tkinter import ttk
from tkinters.extenders.BatchDeleteTab import BatchDeleteTab
from tkinters.extenders.BatchMoveTab import BatchMoveTab
from tkinters.extenders.RecursiveMoveTab import RecursiveMoveTab

class FileHelper(tk.Tk):
    """主应用程序"""

    def __init__(self):
        super().__init__()
        self.title("FileHelper 文件管理助手")
        self.geometry("800x600")
        self._init_ui()

    def _init_ui(self):
        notebook = ttk.Notebook(self)

        tabs = [
            RecursiveMoveTab(notebook),
            BatchMoveTab(notebook),
            BatchDeleteTab(notebook)
        ]

        for tab in tabs:
            notebook.add(tab, text=tab.tab_name)

        notebook.pack(expand=True, fill=tk.BOTH)

if __name__ == "__main__":
    app = FileHelper()
    app.mainloop()

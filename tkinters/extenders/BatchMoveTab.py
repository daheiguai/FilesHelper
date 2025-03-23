from pathlib import Path
from tkinter import ttk, filedialog
import tkinter as tk
from excuters.extenders.BatchMover import BatchMover
from tkinters.OperationTab import OperationTab


class BatchMoveTab(OperationTab):
    """批量移动标签页"""

    def __init__(self, master):
        super().__init__(master, "文件批量移动")
        self.strategy = BatchMover(log_callback=self._log_handler)
        self._add_target_dir()
        ttk.Button(self, text="开始移动", command=self.start_operation).pack(pady=10)

    def _add_target_dir(self):
        target_frame = ttk.Frame(self)
        ttk.Label(target_frame, text="目标目录:").pack(side=tk.LEFT)
        self.target_entry = ttk.Entry(target_frame, width=40)
        self.target_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(target_frame, text="浏览...", command=self._browse_target).pack(side=tk.LEFT)
        target_frame.pack(pady=5)
        self.target_dir = None

    def _browse_target(self):  # 删除错误的tk参数
        path = filedialog.askdirectory()
        if path:
            self.target_entry.delete(0, tk.END)  # 使用正确的tk引用
            self.target_entry.insert(0, path)
            self.target_dir = Path(path)
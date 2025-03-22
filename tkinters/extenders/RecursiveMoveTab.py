from tkinter import ttk

from excuters.extenders.RecursiveMover import RecursiveMover
from tkinters.OperationTab import OperationTab


class RecursiveMoveTab(OperationTab):
    """递归移出标签页"""

    def __init__(self, master):
        super().__init__(master, "文件递归移出")
        self.strategy = RecursiveMover(log_callback=self._log_handler)
        ttk.Button(self, text="开始移出", command=self.start_operation).pack(pady=10)
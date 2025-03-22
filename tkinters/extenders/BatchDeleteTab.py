from tkinter import ttk

from excuters.extenders.BatchDeleter import BatchDeleter
from tkinters.OperationTab import OperationTab


class BatchDeleteTab(OperationTab):
    """批量删除标签页"""

    def __init__(self, master):
        super().__init__(master, "文件批量删除")
        self.strategy = BatchDeleter(log_callback=self._log_handler)
        ttk.Button(self, text="开始删除", command=self.start_operation).pack(pady=10)
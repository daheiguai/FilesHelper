from tkinter import ttk
from excuters.extenders.CopyDirStructureStrategy import CopyDirStructureStrategy
from tkinters.OperationTab import OperationTab

class CopyDirStructureTab(OperationTab):
    """目录结构拷贝标签页"""

    def __init__(self, master):
        super().__init__(master, "拷贝目录结构")
        self.strategy = CopyDirStructureStrategy(log_callback=self._log_handler)
        ttk.Button(self, text="开始拷贝", command=self.start_operation).pack(pady=10)


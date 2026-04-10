from pathlib import Path
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from excuters.extenders.FolderSplitter import FolderSplitter
from tkinters.OperationTab import OperationTab


class FolderSplitTab(OperationTab):
    """大文件夹切割标签页"""

    def __init__(self, master):
        super().__init__(master, "大文件夹切割")
        self.strategy = FolderSplitter(log_callback=self._log_handler)
        self._init_split_ui()
        ttk.Button(self, text="开始切割", command=self.start_operation).pack(pady=10)

    def _init_split_ui(self):
        """初始化切割功能的UI组件"""
        # 文件夹数量输入
        num_frame = ttk.Frame(self)
        ttk.Label(num_frame, text="切割数量:").pack(side=tk.LEFT)
        self.num_entry = ttk.Entry(num_frame, width=10)
        self.num_entry.insert(0, "5")  # 默认值为5
        self.num_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(num_frame, text="(将文件分配到几个文件夹)").pack(side=tk.LEFT)
        num_frame.pack(pady=5)

        # 文件夹名前缀输入
        prefix_frame = ttk.Frame(self)
        ttk.Label(prefix_frame, text="文件夹前缀:").pack(side=tk.LEFT)
        self.prefix_entry = ttk.Entry(prefix_frame, width=20)
        self.prefix_entry.insert(0, "folder")  # 默认前缀
        self.prefix_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(prefix_frame, text="(完整名称: 前缀-序号)").pack(side=tk.LEFT)
        prefix_frame.pack(pady=5)

    def _validate_inputs(self) -> bool:
        """验证输入参数"""
        # 检查根目录
        if not self.dir_entry.get():
            messagebox.showerror("错误", "必须选择根目录")
            return False

        # 检查切割数量
        try:
            num_folders = int(self.num_entry.get())
            if num_folders < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "切割数量必须是正整数")
            return False

        # 检查文件夹前缀
        prefix = self.prefix_entry.get().strip()
        if not prefix:
            messagebox.showerror("错误", "文件夹前缀不能为空")
            return False

        # 检查前缀是否包含非法字符
        if any(c in prefix for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']):
            messagebox.showerror("错误", "文件夹前缀包含非法字符: / \\ : * ? \" < > |")
            return False

        return True

    def _execute_operation(self):
        """执行切割操作"""
        try:
            root_dir = Path(self.dir_entry.get())
            num_folders = int(self.num_entry.get())
            prefix = self.prefix_entry.get().strip()

            # 确认操作 - 先检查目录是否存在
            if not root_dir.exists():
                messagebox.showerror("错误", "目标目录不存在")
                return

            if not root_dir.is_dir():
                messagebox.showerror("错误", "选择的路径不是目录")
                return

            confirm_msg = (
                f"即将把文件分配到 {num_folders} 个文件夹中\n"
                f"文件夹命名: {prefix}-1, {prefix}-2, ..., {prefix}-{num_folders}\n"
                f"确定要继续吗？"
            )

            if not messagebox.askyesno("确认", confirm_msg):
                return

            processed_files = self.strategy.execute(
                root_dir=root_dir,
                num_folders=num_folders,
                prefix=prefix
            )

            messagebox.showinfo("完成", f"成功将 {len(processed_files)} 个文件分配到 {num_folders} 个文件夹中")

        except Exception as e:
            messagebox.showerror("错误", str(e))

from pathlib import Path
from queue import Queue, Empty
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinter as tk
import threading

from util.constant import DEFAULT_ROOT_DIR, PATTERN_OPTIONS, LOG_COLORS


class OperationTab(ttk.Frame):
    """操作标签页基类"""

    def __init__(self, master, tab_name):
        super().__init__(master)
        self.tab_name = tab_name
        self.strategy = None
        self.log_queue = Queue()
        self._init_ui()
        self._start_log_poller()

    def _init_ui(self):
        # 目录选择
        dir_frame = ttk.Frame(self)
        ttk.Label(dir_frame, text="根目录:").pack(side=tk.LEFT)
        self.dir_entry = ttk.Entry(dir_frame, width=40)
        self.dir_entry.insert(0, str(DEFAULT_ROOT_DIR))
        self.dir_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(dir_frame, text="浏览...", command=self._browse_dir).pack(side=tk.LEFT)
        dir_frame.pack(pady=5)

        # 添加递归复选框
        recursive_frame = ttk.Frame(self)
        self.recursive_var = tk.BooleanVar(value=True)  # 默认勾选
        ttk.Checkbutton(
            recursive_frame,
            text="递归搜索子目录",
            variable=self.recursive_var
        ).pack(side=tk.LEFT)
        recursive_frame.pack(pady=5)

        # 匹配模式设置
        mode_frame = ttk.Frame(self)

        # 以关键字开头
        start_frame = ttk.Frame(mode_frame)
        self.start_var = tk.BooleanVar()
        self.start_check = ttk.Checkbutton(start_frame, variable=self.start_var)
        self.start_entry = ttk.Entry(start_frame, width=15, state=tk.DISABLED)
        self.start_check.pack(side=tk.LEFT)
        self.start_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(start_frame, text="以关键字开头").pack(side=tk.LEFT)
        start_frame.pack(anchor=tk.W)

        # 以关键字结尾
        end_frame = ttk.Frame(mode_frame)
        self.end_var = tk.BooleanVar()
        self.end_check = ttk.Checkbutton(end_frame, variable=self.end_var)
        self.end_entry = ttk.Entry(end_frame, width=15, state=tk.DISABLED)
        self.end_check.pack(side=tk.LEFT)
        self.end_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(end_frame, text="以关键字结尾").pack(side=tk.LEFT)
        end_frame.pack(anchor=tk.W)

        # 包含关键字
        include_frame = ttk.Frame(mode_frame)
        self.include_var = tk.BooleanVar()
        self.include_check = ttk.Checkbutton(include_frame, variable=self.include_var)
        self.include_entry = ttk.Entry(include_frame, width=30, state=tk.DISABLED)
        self.include_check.pack(side=tk.LEFT)
        self.include_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(include_frame, text="包含关键字（用;分隔）").pack(side=tk.LEFT)
        include_frame.pack(anchor=tk.W)

        # 提示标签
        self.tooltip = ttk.Label(mode_frame, foreground="gray")
        self.tooltip.pack(side=tk.TOP, fill=tk.X)
        self.include_entry.bind("<Enter>",
                                lambda e: self.tooltip.config(text="多个关键字用英文分号分隔，文件需要包含所有指定关键字"))
        self.include_entry.bind("<Leave>", lambda e: self.tooltip.config(text=""))

        # 动态启用输入框
        self.start_var.trace_add("write", self._toggle_entry_state)
        self.end_var.trace_add("write", self._toggle_entry_state)
        self.include_var.trace_add("write", self._toggle_entry_state)

        mode_frame.pack(pady=5)

        # 日志区域
        self.log_area = scrolledtext.ScrolledText(self, height=10)
        self.log_area.pack(fill=tk.BOTH, expand=True)

        # 初始化日志样式
        for level, color in LOG_COLORS.items():
            self.log_area.tag_config(f"log_{level}", foreground=color)

    def _toggle_entry_state(self, *args):
        """根据复选框状态切换输入框可用性"""
        self.start_entry.config(state=tk.NORMAL if self.start_var.get() else tk.DISABLED)
        self.end_entry.config(state=tk.NORMAL if self.end_var.get() else tk.DISABLED)
        self.include_entry.config(state=tk.NORMAL if self.include_var.get() else tk.DISABLED)

    def _start_log_poller(self):
        """启动日志队列轮询"""

        def check_queue():
            try:
                while True:
                    msg, level = self.log_queue.get_nowait()
                    self._append_log(msg, level)
            except Empty:
                pass
            self.after(100, check_queue)

        self.after(100, check_queue)

    def _append_log(self, message: str, level: str):
        """实际追加日志到文本框"""
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, message + "\n", f"log_{level}")
        self.log_area.configure(state="disabled")
        self.log_area.see(tk.END)

    def _log_handler(self, message: str, level: str):
        """线程安全的日志入队"""
        self.log_queue.put((message, level))

    def _browse_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, path)

    def _validate_inputs(self) -> bool:
        # 检查基础输入
        if not self.dir_entry.get():
            messagebox.showerror("错误", "必须选择根目录")
            return False

        # 检查至少启用一个模式
        enabled_modes = [
            self.start_var.get() and self.start_entry.get().strip(),
            self.end_var.get() and self.end_entry.get().strip(),
            self.include_var.get() and self.include_entry.get().strip()
        ]
        if not any(enabled_modes):
            messagebox.showerror("错误", "至少需要启用并填写一个匹配模式")
            return False

        # 检查已启用模式的输入有效性
        if self.start_var.get() and not self.start_entry.get().strip():
            messagebox.showerror("错误", "启用'以关键字开头'必须填写关键字")
            return False

        if self.end_var.get() and not self.end_entry.get().strip():
            messagebox.showerror("错误", "启用'以关键字结尾'必须填写关键字")
            return False

        if self.include_var.get() and not self.include_entry.get().strip():
            messagebox.showerror("错误", "启用'包含关键字'必须填写关键字")
            return False

        return True

    def _execute_operation(self):
        try:
            root_dir = Path(self.dir_entry.get())
            recursive = self.recursive_var.get()

            # 获取输入参数
            start_kw = self.start_entry.get().strip() if self.start_var.get() else None
            end_kw = self.end_entry.get().strip() if self.end_var.get() else None
            include_kws = [kw.strip() for kw in self.include_entry.get().split(';')
                           if self.include_var.get() and kw.strip()]

            # 验证至少选择一种模式
            if not any([self.start_var.get(), self.end_var.get(), self.include_var.get()]):
                messagebox.showerror("错误", "至少需要选择一种匹配模式")
                return

            processed_files = self.strategy.execute(
                root_dir=root_dir,
                start_keyword=start_kw,
                end_keyword=end_kw,
                include_keywords=include_kws,
                recursive=recursive,
                target_dir=getattr(self, "target_dir", None)
            )

            messagebox.showinfo("完成", f"成功处理 {len(processed_files)} 个文件")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def start_operation(self):
        if not self._validate_inputs():
            return

        if messagebox.askyesno("确认", "确定要执行此操作吗？"):
            threading.Thread(
                target=self._execute_operation,
                daemon=True
            ).start()
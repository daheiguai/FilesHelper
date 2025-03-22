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

        # 关键词输入
        key_frame = ttk.Frame(self)
        ttk.Label(key_frame, text="关键信息:").pack(side=tk.LEFT)
        self.key_entry = ttk.Entry(key_frame, width=30)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        key_frame.pack(pady=5)

        # 模式选择
        mode_frame = ttk.Frame(self)
        ttk.Label(mode_frame, text="匹配模式:").pack(side=tk.LEFT)
        self.mode_combo = ttk.Combobox(mode_frame, values=PATTERN_OPTIONS, state="readonly")
        self.mode_combo.current(0)
        self.mode_combo.pack(side=tk.LEFT, padx=5)
        mode_frame.pack(pady=5)

        # 日志区域
        self.log_area = scrolledtext.ScrolledText(self, height=10)
        self.log_area.pack(fill=tk.BOTH, expand=True)

        # 初始化日志样式
        for level, color in LOG_COLORS.items():
            self.log_area.tag_config(f"log_{level}", foreground=color)

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
        if not self.dir_entry.get():
            messagebox.showerror("错误", "必须选择根目录")
            return False
        if not self.key_entry.get().strip():
            messagebox.showerror("错误", "必须输入关键信息")
            return False
        return True

    def _execute_operation(self):
        try:
            root_dir = Path(self.dir_entry.get())
            keyword = self.key_entry.get().strip()
            pattern = self.mode_combo.get()

            processed_files = self.strategy.execute(
                root_dir=root_dir,
                keyword=keyword,
                pattern=pattern,
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
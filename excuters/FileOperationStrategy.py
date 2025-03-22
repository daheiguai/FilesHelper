from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Callable

class FileOperationStrategy(ABC):
    """文件操作策略抽象基类"""

    def __init__(self, log_callback: Callable[[str, str], None] = None):
        self.log_callback = log_callback

    def log(self, message: str, level: str = "info"):
        """统一日志记录方法"""
        if self.log_callback:
            self.log_callback(f"[{level.upper()}] {message}", level)

    @staticmethod
    def find_files(root_dir: Path, keyword: str, pattern: str) -> List[Path]:
        """通用文件查找方法（大小写不敏感）"""
        files = []
        keyword_lower = keyword.lower()

        for path in root_dir.rglob('*'):
            if path.is_file():
                # 修改为使用完整文件名（含扩展名）
                filename = path.name.lower()

                match_pattern = (
                        (pattern == "以关键信息开头" and filename.startswith(keyword_lower)) or
                        (pattern == "以关键信息结尾" and filename.endswith(keyword_lower)) or
                        (pattern == "包含关键信息" and keyword_lower in filename)
                )

                if match_pattern:
                    files.append(path)
        return files

    @abstractmethod
    def execute(self,
                root_dir: Path,
                keyword: str,
                pattern: str,
                target_dir: Optional[Path] = None) -> List[Path]:
        pass
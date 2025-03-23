# FileOperationStrategy.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Callable


class FileOperationStrategy(ABC):
    """文件操作策略抽象基类"""

    def __init__(self, log_callback: Callable[[str, str], None] = None):
        self.log_callback = log_callback

    def log(self, message: str, level: str = "info"):
        if self.log_callback:
            self.log_callback(f"[{level.upper()}] {message}", level)

    @staticmethod
    def find_files(
            root_dir: Path,
            start_keyword: Optional[str],
            end_keyword: Optional[str],
            include_keywords: List[str],
            recursive: bool
    ) -> List[Path]:
        files = []
        iterator = root_dir.rglob('*') if recursive else root_dir.glob('*')

        for path in iterator:
            if not path.is_file():
                continue

            filename = path.name.lower()
            match_flag = True

            # 检查以关键字开头（如果启用）
            if start_keyword:
                start_lower = start_keyword.strip().lower()
                if not filename.startswith(start_lower):
                    match_flag = False

            # 检查以关键字结尾（如果启用且当前仍匹配）
            if match_flag and end_keyword:
                end_lower = end_keyword.strip().lower()
                if not filename.endswith(end_lower):
                    match_flag = False

            # 检查包含所有关键字（如果启用且当前仍匹配）
            if match_flag and include_keywords:
                include_lower = [kw.strip().lower() for kw in include_keywords]
                for kw in include_lower:
                    if kw not in filename:
                        match_flag = False
                        break

            if match_flag:
                files.append(path)

        return files

    @abstractmethod
    def execute(
            self,
            root_dir: Path,
            start_keyword: Optional[str],
            end_keyword: Optional[str],
            include_keywords: List[str],
            recursive: bool,
            target_dir: Optional[Path] = None
    ) -> List[Path]:
        pass

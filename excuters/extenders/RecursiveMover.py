import shutil
from pathlib import Path
from typing import List

from excuters.FileOperationStrategy import FileOperationStrategy


class RecursiveMover(FileOperationStrategy):
    """递归移出策略"""

    def execute(self, root_dir, keyword, pattern, target_dir=None) -> List[Path]:
        try:
            self.log("开始递归移动操作...")
            matched_files = self.find_files(root_dir, keyword, pattern)

            if not matched_files:
                self.log("未找到匹配文件", "warning")
                return []

            self.log(f"找到 {len(matched_files)} 个匹配文件")

            for idx, file in enumerate(matched_files, 1):
                dest = root_dir / file.name
                if dest.exists():
                    self.log(f"文件已存在，跳过: {dest.name}", "warning")
                    continue

                shutil.move(str(file), str(dest))
                self.log(f"移动文件 ({idx}/{len(matched_files)}): {file.name}")

            self.log("操作成功完成")
            return matched_files

        except Exception as e:
            self.log(f"操作失败: {str(e)}", "error")
            raise
import shutil
from pathlib import Path
from typing import List

from excuters.FileOperationStrategy import FileOperationStrategy


class BatchMover(FileOperationStrategy):
    """批量移动策略"""

    def execute(self, root_dir, keyword, pattern, target_dir) -> List[Path]:
        try:
            self.log("开始批量移动操作...")
            if not target_dir.exists():
                target_dir.mkdir(parents=True)

            matched_files = self.find_files(root_dir, keyword, pattern)

            for idx, file in enumerate(matched_files, 1):
                dest = target_dir / file.name
                shutil.move(str(file), str(dest))
                self.log(f"移动文件 ({idx}/{len(matched_files)}): {file.name}")

            self.log("操作成功完成")
            return matched_files

        except Exception as e:
            self.log(f"操作失败: {str(e)}", "error")
            raise
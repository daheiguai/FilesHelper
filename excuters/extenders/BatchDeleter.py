from pathlib import Path
from typing import List

from excuters.FileOperationStrategy import FileOperationStrategy


class BatchDeleter(FileOperationStrategy):
    """批量删除策略"""

    def execute(self, root_dir, start_keyword, end_keyword, include_keywords, recursive, target_dir=None) -> List[Path]:
        try:
            self.log("开始批量删除操作...")
            matched_files = FileOperationStrategy.find_files(
                root_dir, start_keyword, end_keyword, include_keywords, recursive
            )

            for idx, file in enumerate(matched_files, 1):
                file.unlink()
                self.log(f"删除文件 ({idx}/{len(matched_files)}): {file.name}")

            self.log("操作成功完成")
            return matched_files

        except Exception as e:
            self.log(f"操作失败: {str(e)}", "error")
            raise
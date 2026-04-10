from pathlib import Path
import shutil
import os
from excuters.FileOperationStrategy import FileOperationStrategy


class FolderSplitter(FileOperationStrategy):
    """文件夹分割策略 - 将文件夹中的文件平均分配到n个子文件夹中"""

    def execute(
            self,
            root_dir: Path,
            num_folders: int,
            prefix: str = "folder",
            start_keyword=None,
            end_keyword=None,
            include_keywords=None,
            recursive=False,
            target_dir=None
    ) -> list:
        """
        执行文件夹分割操作

        Args:
            root_dir: 目标根目录
            num_folders: 要创建的子文件夹数量
            prefix: 文件夹名前缀
            start_keyword: 未使用（保留接口兼容性）
            end_keyword: 未使用（保留接口兼容性）
            include_keywords: 未使用（保留接口兼容性）
            recursive: 未使用（保留接口兼容性）
            target_dir: 未使用（保留接口兼容性）

        Returns:
            成功移动的文件列表
        """
        if not root_dir.exists():
            raise FileNotFoundError(f"目录不存在: {root_dir}")

        if not root_dir.is_dir():
            raise NotADirectoryError(f"路径不是目录: {root_dir}")

        if num_folders < 1:
            raise ValueError("文件夹数量必须大于0")

        # 使用 os.scandir() 优化文件扫描性能
        all_files = []
        try:
            with os.scandir(root_dir) as entries:
                for entry in entries:
                    if entry.is_file(follow_symlinks=False):
                        all_files.append(Path(entry.path))
        except PermissionError as e:
            raise PermissionError(f"没有权限访问目录: {root_dir}") from e

        if not all_files:
            self.log("目标目录中没有文件", "warning")
            return []

        total_files = len(all_files)
        self.log(f"找到 {total_files} 个文件，将分配到 {num_folders} 个文件夹中")

        # 计算每个文件夹应该有多少文件
        files_per_folder = total_files // num_folders
        remainder = total_files % num_folders

        # 创建子文件夹
        created_folders = []
        for i in range(1, num_folders + 1):
            folder_name = f"{prefix}-{i}"
            folder_path = root_dir / folder_name

            # 如果文件夹已存在，跳过或报错
            if folder_path.exists():
                self.log(f"文件夹已存在，将使用现有文件夹: {folder_name}", "warning")
            else:
                folder_path.mkdir(parents=True, exist_ok=True)
                self.log(f"创建文件夹: {folder_name}")

            created_folders.append(folder_path)

        # 分配文件到各个文件夹
        moved_files = []
        file_index = 0

        for folder_idx, folder_path in enumerate(created_folders):
            # 计算当前文件夹的文件数量（前remainder个文件夹多一个文件）
            current_folder_size = files_per_folder + (1 if folder_idx < remainder else 0)

            for _ in range(current_folder_size):
                if file_index >= total_files:
                    break

                source_file = all_files[file_index]
                dest_file = folder_path / source_file.name

                try:
                    # 处理文件名冲突
                    if dest_file.exists():
                        counter = 1
                        stem = source_file.stem
                        suffix = source_file.suffix
                        while dest_file.exists():
                            dest_file = folder_path / f"{stem}_{counter}{suffix}"
                            counter += 1

                    # 移动文件
                    shutil.move(str(source_file), str(dest_file))
                    moved_files.append(dest_file)
                    self.log(f"移动: {source_file.name} -> {folder_path.name}/{dest_file.name}")
                    file_index += 1

                except Exception as e:
                    self.log(f"移动文件失败 {source_file.name}: {str(e)}", "error")

        self.log(f"完成！共移动 {len(moved_files)} 个文件到 {num_folders} 个文件夹中")
        return moved_files

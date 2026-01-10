from pathlib import Path
from excuters.FileOperationStrategy import FileOperationStrategy

class CopyDirStructureStrategy(FileOperationStrategy):
    def execute(self, root_dir: Path, **kwargs):
        parent_dir = root_dir.parent
        base_name = root_dir.name
        new_dir = parent_dir / f"{base_name}-1"
        if new_dir.exists():
            self.log("目标目录已存在", "error")
            return []

        new_dir.mkdir()
        for path in root_dir.rglob("*"):
            if path.is_dir():
                rel_path = path.relative_to(root_dir)
                target_path = new_dir / rel_path
                target_path.mkdir(exist_ok=True)
        self.log(f"目录结构已拷贝到: {new_dir}", "info")
        return [new_dir]

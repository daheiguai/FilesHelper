from pathlib import Path

DEFAULT_ROOT_DIR = Path.cwd()
PATTERN_OPTIONS = ["以关键信息开头", "以关键信息结尾", "包含关键信息"]
LOG_COLORS = {
    "info": "blue",
    "warning": "orange",
    "error": "red"
}
#需要走模式的页面，包括页面检查，递归选择等
PATTERN_TABLE_TYPE = [
    "文件批量删除",
    "文件批量移动",
    "文件递归移出"
]


def valid_or_none(obj):
    """
    判断对象是否为空或为 None，如果是则返回 None，否则返回对象本身
    """
    if is_empty(obj):
        return None
    return obj

def is_empty(obj):
    """
    判断对象是否为 None、空字符串、空列表、空元组、空字典等
    """
    if obj is None:
        return True
    if isinstance(obj, (str, list, tuple, dict, set)) and len(obj) == 0:
        return True
    return False
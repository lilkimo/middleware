from typing import Any, Callable
from datetime import datetime, timedelta

def _compareAny(a: Any, b: Any) -> bool:
    return a == b

def _compareDict(a: dict, b: dict) -> bool:
    if a.keys() != b.keys():
        return False
    for key in a.keys():
        if not compare(a[key], b[key]):
            return False
    return True

def _compareList(a: list, b: list) -> bool:
    if len(a) != len(b):
        return False
    for key in range(len(a)):
        if not compare(a[key], b[key]):
            return False
    return True

def _compareStr(a: str, b: str) -> bool:
    try:
        dta = datetime.fromisoformat(a)
    except ValueError:
        dta = None
    try:
        dtb = datetime.fromisoformat(b)
    except ValueError:
        dtb = None

    if bool(dta)^bool(dtb):
        return False
    if (dta is not None) and (dtb is not None):
        if abs(dta - dtb) > timedelta(seconds=10):
            return False
        return True
    return _compareAny(a, b)

_compare: dict[type, Callable[[Any, Any], bool]] = {
    dict: _compareDict,
    list: _compareList,
    str: _compareStr,
}

def compare(a: Any, b: Any):
    print(a)
    print(b)
    t = type(a)
    if t != type(b):
        return False
    return _compare.get(t, _compareAny)(a, b)

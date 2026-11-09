"""实例发现与连接管理。"""

from .autocad_adapter import AutoCADAdapter
from .base import CADAdapter
from .tarch_adapter import TArchAdapter

ADAPTERS = {
    "autocad": AutoCADAdapter,
    "tarch": TArchAdapter,
}


def list_apps() -> dict:
    """探测本机可连接的 CAD 实例，返回 {平台名: 是否在线}。"""
    status = {}
    for name, cls in ADAPTERS.items():
        try:
            adapter = cls.attach_or_launch()
            status[name] = adapter.is_alive()
        except Exception:
            status[name] = False
    return status


def connect(platform: str = "auto", exe_path: str | None = None) -> CADAdapter:
    """连接 CAD 实例。

    platform: "auto"（先 AutoCAD 后天正）、"autocad" 或 "tarch"
    exe_path: 实例未运行时用于启动的可执行文件路径（可选）
    """
    if platform == "auto":
        order = ["autocad", "tarch"]
    else:
        order = [platform]

    for name in order:
        cls = ADAPTERS.get(name)
        if cls is None:
            raise ValueError(f"未知平台：{name}，可选 {list(ADAPTERS)}")
        try:
            return cls.attach_or_launch(exe_path)
        except ConnectionError:
            continue
    raise ConnectionError("AutoCAD 2020 与天正 V7.0 实例均未找到。")

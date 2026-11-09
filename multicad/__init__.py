"""multiCAD：统一控制 AutoCAD 2020 与天正（TArch/T20）V7.0。"""

from .app import connect, list_apps

__all__ = ["connect", "list_apps"]
__version__ = "0.1.0"

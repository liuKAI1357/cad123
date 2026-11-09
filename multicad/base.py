"""CAD 适配器抽象接口：所有平台（AutoCAD / 天正）均实现此协议。"""

from abc import ABC, abstractmethod
from typing import Sequence, Tuple

Point = Tuple[float, float, float]


class CADAdapter(ABC):
    """统一的 CAD 自动化接口。"""

    name: str = "base"

    @abstractmethod
    def is_alive(self) -> bool:
        """当前 CAD 实例是否仍可通信。"""

    @abstractmethod
    def send_command(self, command: str) -> None:
        """向活动文档发送命令行命令（以换行结尾视为回车）。"""

    @abstractmethod
    def draw_line(self, start: Sequence[float], end: Sequence[float]) -> object:
        """绘制直线，返回图元对象。"""

    @abstractmethod
    def draw_circle(self, center: Sequence[float], radius: float) -> object:
        """绘制圆。"""

    @abstractmethod
    def draw_text(self, insert: Sequence[float], text: str, height: float = 3.5) -> object:
        """绘制单行文字。"""

    @abstractmethod
    def draw_polyline(self, points: Sequence[Sequence[float]], closed: bool = False) -> object:
        """绘制多段线。"""

    def close(self) -> None:
        """释放资源（默认无操作）。"""

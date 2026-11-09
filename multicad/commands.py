"""常用绘图组合命令封装（可选的高级封装层）。"""

from typing import Sequence

from .base import CADAdapter


def draw_rectangle(cad: CADAdapter, corner1: Sequence[float], corner2: Sequence[float]):
    """按对角两点绘制矩形（四段多段线）。"""
    x1, y1 = corner1[0], corner1[1]
    x2, y2 = corner2[0], corner2[1]
    pts = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    return cad.draw_polyline(pts, closed=True)


def draw_axis_text(cad: CADAdapter, label: str, insert: Sequence[float]):
    """绘制轴号文字（直径 800mm 圆内标注，简化版）。"""
    circle = cad.draw_circle(insert, 400)
    text = cad.draw_text(insert, label, height=350)
    return circle, text

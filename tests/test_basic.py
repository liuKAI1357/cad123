"""基础自测：不依赖真实 CAD 进程。"""

from multicad.base import CADAdapter
from multicad.commands import draw_rectangle


class DummyAdapter(CADAdapter):
    name = "dummy"

    def __init__(self):
        self.calls = []

    def is_alive(self):
        return True

    def send_command(self, command):
        self.calls.append(("cmd", command))

    def draw_line(self, start, end):
        self.calls.append(("line", start, end))
        return None

    def draw_circle(self, center, radius):
        self.calls.append(("circle", center, radius))
        return None

    def draw_text(self, insert, text, height=3.5):
        self.calls.append(("text", insert, text))
        return None

    def draw_polyline(self, points, closed=False):
        self.calls.append(("polyline", list(points), closed))
        return None


def test_draw_rectangle():
    cad = DummyAdapter()
    draw_rectangle(cad, (0, 0), (100, 50))
    kind, pts, closed = cad.calls[0]
    assert kind == "polyline"
    assert closed is True
    assert len(pts) == 4


if __name__ == "__main__":
    test_draw_rectangle()
    print("测试通过")

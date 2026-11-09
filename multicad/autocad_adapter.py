"""AutoCAD 2020 COM 适配器（ActiveX Automation）。"""

from typing import Sequence

from .base import CADAdapter

PROG_IDS = ("AutoCAD.Application.23", "AutoCAD.Application")  # 23 = 2020


class AutoCADAdapter(CADAdapter):
    name = "autocad"

    def __init__(self, app):
        # app: win32com COM 对象（AutoCAD.Application）
        self._app = app

    # -- 生命周期 ---------------------------------------------------------
    @classmethod
    def attach_or_launch(cls, exe_path: str | None = None) -> "AutoCADAdapter":
        import pythoncom
        import win32com.client

        pythoncom.CoInitialize()
        for prog_id in PROG_IDS:
            try:
                app = win32com.client.GetActiveObject(prog_id)
                return cls(app)
            except Exception:
                continue
        if exe_path:
            app = win32com.client.Dispatch("AutoCAD.Application")
            app.Visible = True
            app.Documents.Add()
            return cls(app)
        raise ConnectionError("未找到运行中的 AutoCAD 2020 实例，且未提供可执行文件路径。")

    def is_alive(self) -> bool:
        try:
            _ = self._app.ActiveDocument.Name
            return True
        except Exception:
            return False

    def close(self) -> None:
        self._app = None

    # -- 绘图 -------------------------------------------------------------
    def _model_space(self):
        return self._app.ActiveDocument.ModelSpace

    def _p3(self, pt: Sequence[float]):
        pt = list(pt) + [0.0] * (3 - len(pt))
        # win32com 需要显式的 VARIANT 数组
        import pythoncom
        import win32com.client

        arr = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, pt)
        return arr

    def send_command(self, command: str) -> None:
        if not command.endswith("\n"):
            command += "\n"
        self._app.ActiveDocument.SendCommand(command)

    def draw_line(self, start: Sequence[float], end: Sequence[float]):
        return self._model_space().AddLine(self._p3(start), self._p3(end))

    def draw_circle(self, center: Sequence[float], radius: float):
        return self._model_space().AddCircle(self._p3(center), radius)

    def draw_text(self, insert: Sequence[float], text: str, height: float = 3.5):
        return self._model_space().AddText(text, self._p3(insert), height)

    def draw_polyline(self, points: Sequence[Sequence[float]], closed: bool = False):
        import pythoncom
        import win32com.client

        flat = []
        for p in points:
            p = list(p) + [0.0] * (3 - len(p))
            flat.extend(p[:3])
        arr = win32com.client.VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_R8, flat
        )
        pl = self._model_space().AddPolyline(arr)
        if closed:
            pl.Closed = True
        return pl

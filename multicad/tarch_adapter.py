"""天正（TArch / T20）V7.0 适配器。

天正 T20 V7.0 的 CAD 内核基于 AutoCAD 2020（OEM），其 COM 自动化
入口的 ProgID 与 AutoCAD 不同（常见为 T20V7.Application）。
"""

from typing import Sequence

from .autocad_adapter import AutoCADAdapter

PROG_IDS = (
    "T20V7.Application",       # 天正 T20 V7.0
    "TArch.Application",
    "Tangent.Application",
)


class TArchAdapter(AutoCADAdapter):
    """天正 V7.0 与 AutoCAD 共用 ActiveX 接口，仅需替换 ProgID 发现逻辑。"""

    name = "tarch"

    @classmethod
    def attach_or_launch(cls, exe_path: str | None = None) -> "TArchAdapter":
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
            app = win32com.client.Dispatch(PROG_IDS[0])
            app.Visible = True
            return cls(app)
        raise ConnectionError(
            "未找到运行中的天正 V7.0 实例。"
            "若 ProgID 不同，请在 tarch_adapter.PROG_IDS 中补充。"
        )

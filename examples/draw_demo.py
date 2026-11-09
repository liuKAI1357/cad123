"""示例：连接 CAD 并绘制简单图形（需在本机运行 AutoCAD 2020 或天正 V7.0）。"""

from multicad import connect
from multicad.commands import draw_rectangle

cad = connect()  # 自动发现：先 AutoCAD 2020，后天正 V7.0
print(f"已连接：{cad.name}")

draw_rectangle(cad, (0, 0), (200, 100))
cad.draw_circle((100, 50), 30)
cad.draw_text((70, 110), "multiCAD 示例")
cad.send_command("ZOOM E")

print("绘图完成。")

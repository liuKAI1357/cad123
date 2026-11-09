# multiCAD

一套用于统一控制 **AutoCAD 2020** 与 **天正（TArch/T20）V7.0** 的 Python 工具。
通过 COM 自动化接口（pywin32）连接 CAD 进程，对两种平台提供一致的绘图与查询 API。

## 特性

- 自动发现并连接正在运行的 AutoCAD 2020 / 天正 V7.0 实例
- 未运行时可自动启动指定可执行文件
- 统一适配层：绘制直线、圆、多段线、文字，发送命令行命令
- 支持 ActiveX `SendCommand` 与命令别名，兼容天正 T20 内核

## 环境要求

- Windows + 已安装 AutoCAD 2020 或 天正 T20 V7.0
- Python 3.9+
- `pip install -r requirements.txt`

## 快速开始

```python
from multicad import connect

# 自动连接（优先 AutoCAD，其次天正）
cad = connect()

# 或显式指定平台
cad = connect("tarch")      # 天正 V7.0
cad = connect("autocad")    # AutoCAD 2020

cad.draw_line((0, 0), (100, 0))
cad.draw_circle((50, 50), 20)
cad.draw_text((0, 10), "你好，multiCAD")
cad.send_command("ZOOM\nE\n")
```

命令行：

```bash
python -m multicad.cli status          # 查看当前连接状态
python -m multicad.cli run "ZOOM E"    # 向活动文档发送命令
```

## 项目结构

```
multicad/
├── base.py               # CADAdapter 抽象接口
├── app.py                # 实例发现 / 连接管理
├── autocad_adapter.py    # AutoCAD 2020 COM 适配器
├── tarch_adapter.py      # 天正 T20 V7.0 适配器
├── commands.py           # 通用绘图命令封装
└── cli.py                # 命令行入口
```

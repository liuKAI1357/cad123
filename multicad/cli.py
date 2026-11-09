"""命令行入口：python -m multicad.cli"""

import argparse
import sys

from .app import connect, list_apps


def main(argv=None):
    parser = argparse.ArgumentParser(prog="multicad", description="控制 AutoCAD 2020 / 天正 V7.0")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="查看各平台连接状态")

    p_run = sub.add_parser("run", help="向活动文档发送命令")
    p_run.add_argument("command", help="要发送的命令，如 \"ZOOM E\"")
    p_run.add_argument("-p", "--platform", default="auto", choices=["auto", "autocad", "tarch"])

    args = parser.parse_args(argv)

    if args.cmd == "status":
        for name, online in list_apps().items():
            print(f"{name}: {'在线' if online else '未找到'}")
        return 0

    if args.cmd == "run":
        cad = connect(args.platform)
        cad.send_command(args.command)
        print(f"已发送命令：{args.command!r} -> {cad.name}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

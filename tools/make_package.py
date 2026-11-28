#!/usr/bin/env python3
"""
打包“发给别人”的商品管理工具压缩包。

包含：
- 泡泡哥商品管理工具.exe（免 Python）
- 使用手册.md
- 使用说明.txt
- src/data（商品与分类 JSON）
- public/images/products（商品图片）
- public/images/details（详情图片）
- public/videos/products（详情视频）
- public/images 下的客服头像、微信二维码、收款二维码

用法：
    python tools/make_package.py
    python tools/make_package.py --output D:\\paopao-tool.zip

生成前请先确认 exe 已打包：
    tools\\build_exe.bat
"""

from __future__ import annotations

import argparse
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "tools" / "dist" / "泡泡哥商品管理工具.exe"
DATA_DIR = ROOT / "src" / "data"
IMAGES_DIR = ROOT / "public" / "images" / "products"
DETAIL_IMAGES_DIR = ROOT / "public" / "images" / "details"
VIDEOS_DIR = ROOT / "public" / "videos" / "products"
SITE_IMAGES = (
    ROOT / "public" / "images" / "paopao-qr.png",
    ROOT / "public" / "images" / "paopao-face.jpg",
    ROOT / "public" / "images" / "paopao-avatar-600.jpg",
    ROOT / "public" / "images" / "payment-qr.webp",
    ROOT / "public" / "images" / "wechat-qr.webp",
    ROOT / "public" / "images" / "wechat-avatar.webp",
)
MANUAL = ROOT / "tools" / "使用手册.md"

QUICK_START = """泡泡哥商品管理工具 · 快速上手
================================

1. 解压后双击“泡泡哥商品管理工具.exe”。
   不需要安装 Python、Node.js 或 Git。

2. 商品管理：
   左侧选商品，右侧改名称、价格、一级/二级分类、描述。
   “选择图片”可以从任意文件夹选图，保存时自动压缩。
   改完点“保存商品”。

3. 分类 / 导航：
   一级分类 = 顶部菜单，二级分类 = 下拉项。
   改完点“保存分类”。

4. 保存不会自动上线：
   这台电脑没有 Git 时，点右上角“导出数据包”，
   把生成的 zip 发给管理员发布上线。

5. 注意：
   - 不要把 exe 单独移出文件夹，否则会提示“找不到项目数据”。
   - Windows 提示“未知发布者”时，点“更多信息 → 仍要运行”。
   - 不要删除 src 和 public 文件夹。

完整说明见同目录的“使用手册.md”。
"""


def add_folder(archive: zipfile.ZipFile, folder: Path, prefix: str) -> int:
    if not folder.exists():
        return 0
    count = 0
    for path in folder.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".tmp":
            continue
        archive.write(path, f"{prefix}/{path.relative_to(ROOT).as_posix()}")
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="打包商品管理工具分发包")
    parser.add_argument("--output", help="输出 zip 路径，默认放到桌面")
    args = parser.parse_args()

    if not EXE.exists():
        print("没有找到 exe：", EXE)
        print("请先运行 tools\\build_exe.bat 打包 exe，再执行本脚本。")
        return 1

    if args.output:
        target = Path(args.output).expanduser().resolve()
    else:
        desktop = Path.home() / "Desktop"
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        target = (desktop if desktop.exists() else ROOT) / (
            f"泡泡哥商品管理工具-发给别人-{stamp}.zip"
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    prefix = "泡泡哥商品管理工具"

    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(f"{prefix}/使用说明.txt", QUICK_START)
        archive.write(EXE, f"{prefix}/{EXE.name}")
        if MANUAL.exists():
            archive.write(MANUAL, f"{prefix}/{MANUAL.name}")
        json_count = add_folder(archive, DATA_DIR, prefix)
        image_count = add_folder(archive, IMAGES_DIR, prefix)
        detail_count = add_folder(archive, DETAIL_IMAGES_DIR, prefix)
        video_count = add_folder(archive, VIDEOS_DIR, prefix)
        site_image_count = 0
        for path in SITE_IMAGES:
            if not path.exists():
                continue
            archive.write(path, f"{prefix}/{path.relative_to(ROOT).as_posix()}")
            site_image_count += 1

    size_mb = round(target.stat().st_size / 1024 / 1024, 2)
    print("已生成：", target)
    print("大小：", size_mb, "MB")
    print("数据文件：", json_count)
    print("商品图片：", image_count)
    print("详情图片：", detail_count)
    print("详情视频：", video_count)
    print("客服图片：", site_image_count)
    if image_count == 0:
        print("提示：当前没有商品图片，压缩包里只有数据。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

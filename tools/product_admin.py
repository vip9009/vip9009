#!/usr/bin/env python3
"""
泡泡哥雾化 · 本地商品管理工具

不依赖线上后台，直接编辑项目里的 JSON 和图片：
- 商品新增 / 修改 / 删除 / 排序
- 一级分类、二级分类新增 / 修改 / 删除
- 商品可指定到具体二级分类（末级分类）
- 图片自动压缩成 800px WebP
- 一键保存，一键 git commit + push，GitHub Actions 自动部署

运行：
    python tools/product_admin.py

检查数据：
    python tools/product_admin.py --check
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from PIL import Image, ImageOps, ImageTk
except ImportError:  # 允许 --check 在没有 Pillow 的环境下运行
    Image = None
    ImageOps = None
    ImageTk = None


def resolve_root() -> Path:
    """Find the project folder both when running as .py and as a frozen .exe."""
    starts = []
    if getattr(sys, "frozen", False):
        starts.append(Path(sys.executable).resolve().parent)
        starts.append(Path.cwd())
    else:
        starts.append(Path(__file__).resolve().parent)
    for start in starts:
        for candidate in [start, *start.parents]:
            if (candidate / "src" / "data" / "site" / "categories.json").exists():
                return candidate
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


ROOT = resolve_root()
DATA_DIR = ROOT / "src" / "data"
SECTIONS_DIR = DATA_DIR / "sections"
CATEGORIES_FILE = DATA_DIR / "site" / "categories.json"
GENERAL_FILE = DATA_DIR / "site" / "general.json"
CONTACTS_FILE = DATA_DIR / "site" / "contacts.json"
IMAGES_DIR = ROOT / "public" / "images" / "products"
PAYMENT_IMAGE = ROOT / "public" / "images" / "payment-qr.webp"
BACKUP_DIR = ROOT / "tools" / ".backups"
CATEGORY_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

TOP_LEVEL = "（一级分类）"
NO_SUB = "（不指定）"
IMAGE_HINT = "未选择图片\n任意文件夹的图片都可以\n保存时自动转成 800px WebP"


# ---------------------------------------------------------------------------
# JSON / 数据层
# ---------------------------------------------------------------------------

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handler:
        return json.load(handler)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        shutil.copy2(path, BACKUP_DIR / f"{path.stem}-{stamp}{path.suffix}")
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)


def load_sections() -> dict:
    sections = {}
    for path in sorted(SECTIONS_DIR.glob("*.json")):
        data = load_json(path)
        if not isinstance(data, dict):
            continue
        data.setdefault("id", path.stem)
        data.setdefault("title", path.stem)
        data.setdefault("sort", 999)
        data.setdefault("products", [])
        sections[path.stem] = data
    return sections


def sorted_sections(sections: dict):
    return sorted(
        sections.values(),
        key=lambda item: (item.get("sort", 999), item.get("id", "")),
    )


def category_tops(categories: dict):
    return sorted(
        [(cid, cat) for cid, cat in categories.items() if not cat.get("parent")],
        key=lambda item: (item[1].get("sort", 999), item[0]),
    )


def children_of(categories: dict, category_id: str):
    category = categories.get(category_id) or {}
    children = []
    for child_id in category.get("children", []):
        child = categories.get(child_id)
        if child:
            children.append((child_id, child))
    return sorted(children, key=lambda item: (item[1].get("sort", 999), item[0]))


def category_full_title(categories: dict, category_id: str) -> str:
    category = categories.get(category_id)
    if not category:
        return ""
    parent_id = category.get("parent")
    if parent_id and parent_id in categories:
        return f"{categories[parent_id].get('title', parent_id)} / {category.get('title', category_id)}"
    return category.get("title", category_id)


def section_for_category(categories: dict, category_id: str):
    category = categories.get(category_id) or {}
    if category.get("parent"):
        parent = categories.get(category["parent"]) or {}
        return parent.get("section")
    return category.get("section")


def compact_price(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    return int(number) if number.is_integer() else round(number, 2)


def image_path(local_image: str) -> Path | None:
    if not local_image:
        return None
    return ROOT / "public" / local_image.lstrip("/")


def process_image(source: str, section_id: str) -> str:
    if Image is None:
        raise RuntimeError("缺少 Pillow，请先执行：pip install -r tools/requirements.txt")
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    safe_section = re.sub(r"[^a-zA-Z0-9_-]+", "-", section_id).strip("-") or "product"
    filename = f"{safe_section}-{stamp}.webp"
    destination = IMAGES_DIR / filename

    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened) if ImageOps else opened
        if image.mode in ("RGBA", "LA"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        else:
            image = image.convert("RGB")
        resampling = getattr(Image, "Resampling", Image)
        image.thumbnail((800, 800), resampling.LANCZOS)
        image.save(destination, "WEBP", quality=85, method=6)

    return f"/images/products/{filename}"


def check_data() -> int:
    errors = []
    sections = load_sections()
    categories = load_json(CATEGORIES_FILE)
    product_count = 0

    for category_id, category in categories.items():
        if not category.get("title"):
            errors.append(f"分类 {category_id}: 缺少名称")
        parent_id = category.get("parent")
        if parent_id:
            parent = categories.get(parent_id)
            if not parent:
                errors.append(f"分类 {category_id}: 上级分类 {parent_id} 不存在")
            elif category_id not in parent.get("children", []):
                errors.append(f"分类 {category_id}: 没有挂到上级 {parent_id} 的下拉列表中")
        elif not category.get("to"):
            section_id = category.get("section")
            if section_id and section_id not in sections:
                errors.append(f"分类 {category_id}: 关联分区 {section_id} 不存在")

    for section_id, section in sections.items():
        if not section.get("title"):
            errors.append(f"{section_id}: 缺少分区标题")
        seen_titles = set()
        for index, product in enumerate(section.get("products", [])):
            product_count += 1
            title = str(product.get("title", "")).strip()
            if not title:
                errors.append(f"{section_id}[{index}]: 缺少商品名称")
            elif title in seen_titles:
                errors.append(f"{section_id}[{index}]: 商品名称重复：{title}")
            seen_titles.add(title)
            if product.get("price") in (None, ""):
                errors.append(f"{section_id}[{index}]: 缺少价格")
            price_max = product.get("priceMax")
            if price_max not in (None, ""):
                try:
                    if float(price_max) < float(product.get("price")):
                        errors.append(f"{section_id}[{index}]: 价格上限小于基础价格")
                except (TypeError, ValueError):
                    errors.append(f"{section_id}[{index}]: 价格上限不是数字：{price_max}")
            options = product.get("options")
            if options is not None:
                if not isinstance(options, list):
                    errors.append(f"{section_id}[{index}]: options 应该是数组")
                else:
                    for option in options:
                        if isinstance(option, dict):
                            if not option.get("label"):
                                errors.append(f"{section_id}[{index}]: 口味缺少名称")
                            if option.get("price") not in (None, ""):
                                try:
                                    if float(option.get("price")) <= 0:
                                        raise ValueError
                                except (TypeError, ValueError):
                                    errors.append(
                                        f"{section_id}[{index}]: 口味价格不正确：{option.get('label')}"
                                    )
                            if "stock" in option and not isinstance(option.get("stock"), bool):
                                errors.append(
                                    f"{section_id}[{index}]: 口味库存标记应为 true/false：{option.get('label')}"
                                )
                        elif not isinstance(option, str):
                            errors.append(f"{section_id}[{index}]: 口味格式不正确")
            local_image = product.get("localImage", "")
            path = image_path(local_image)
            if not path or not path.exists():
                errors.append(f"{section_id}[{index}]: 图片不存在：{local_image}")
            subcategory = product.get("subcategory")
            if subcategory:
                child = categories.get(subcategory)
                if not child:
                    errors.append(f"{section_id}[{index}]: 二级分类 {subcategory} 不存在")
                elif child.get("parent") != section_id:
                    errors.append(
                        f"{section_id}[{index}]: 二级分类 {subcategory} 不属于该一级分类"
                    )

    print(f"分区：{len(sections)}")
    print(f"商品：{product_count}")
    print(f"分类：{len(categories)}")

    try:
        general = load_json(GENERAL_FILE)
        contacts = load_json(CONTACTS_FILE)
        qr = (general.get("payment") or {}).get("qr")
        if qr:
            qr_path = ROOT / "public" / str(qr).lstrip("/")
            if not qr_path.exists():
                errors.append(f"收款二维码不存在：{qr}")
        if not (contacts.get("qq") or {}).get("number"):
            errors.append("contacts.json 缺少 QQ 号")
    except Exception as error:
        errors.append(f"站点配置读取失败：{error}")
    if errors:
        print("\n发现以下问题：")
        for error in errors:
            print(" -", error)
        return 1
    print("\n数据检查通过。")
    return 0


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class ProductAdmin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("泡泡哥雾化 · 商品管理工具")
        self.geometry("1260x860")
        self.minsize(1080, 740)

        self.sections = load_sections()
        self.categories = load_json(CATEGORIES_FILE)
        self.general = load_json(GENERAL_FILE)
        self.contacts = load_json(CONTACTS_FILE)

        self.row_map = {}
        self.product_top_labels = {}
        self.product_sub_labels = {}
        self.filter_map = {}
        self.category_parent_labels = {}

        self.current_section = None
        self.current_index = None
        self.pending_image = None
        self._preview_photo = None
        self._last_image_dir = None
        self.extra = self._empty_extra()
        self._pay_photo = None
        self.pending_payment_image = None

        self.category_mode = "edit"
        self.editing_category = None

        self._build_style()
        self._build_header()
        self._build_tabs()
        self._build_status()
        self._refresh_all()

    # -- 基础样式 ---------------------------------------------------------

    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(".", font=("Microsoft YaHei UI", 10))
        style.configure("Treeview", rowheight=30, font=("Microsoft YaHei UI", 10))
        style.configure("Treeview.Heading", font=("Microsoft YaHei UI", 10, "bold"))
        style.configure("Accent.TButton", background="#EA580C", foreground="#000000", padding=(12, 6))
        style.map("Accent.TButton", background=[("active", "#F97316")])
        style.configure("Danger.TButton", background="#B91C1C", foreground="#FFFFFF", padding=(12, 6))
        style.map("Danger.TButton", background=[("active", "#DC2626")])
        style.configure("Secondary.TButton", padding=(10, 5))

    def _build_header(self):
        header = tk.Frame(self, bg="#064E3B", height=66)
        header.pack(fill="x")
        tk.Label(
            header,
            text="泡泡哥雾化 · 商品管理",
            bg="#064E3B",
            fg="#FFFFFF",
            font=("Microsoft YaHei UI", 18, "bold"),
        ).pack(side="left", padx=22, pady=16)
        tk.Label(
            header,
            text="本地工具 · 直接修改 JSON · 不依赖线上后台",
            bg="#064E3B",
            fg="#A7F3D0",
            font=("Microsoft YaHei UI", 9),
        ).pack(side="left", pady=20)

        tk.Button(
            header,
            text="发布到 GitHub",
            command=self.publish,
            bg="#EA580C",
            fg="#000000",
            activebackground="#F97316",
            relief="flat",
            font=("Microsoft YaHei UI", 10, "bold"),
            padx=16,
            pady=7,
            cursor="hand2",
        ).pack(side="right", padx=20)
        tk.Button(
            header,
            text="打开数据目录",
            command=self.open_data_dir,
            bg="#0B7A5F",
            fg="#FFFFFF",
            activebackground="#059669",
            relief="flat",
            font=("Microsoft YaHei UI", 9),
            padx=12,
            pady=7,
            cursor="hand2",
        ).pack(side="right", padx=6)
        tk.Button(
            header,
            text="导出数据包",
            command=self.export_package,
            bg="#0B7A5F",
            fg="#FFFFFF",
            activebackground="#059669",
            relief="flat",
            font=("Microsoft YaHei UI", 9),
            padx=12,
            pady=7,
            cursor="hand2",
        ).pack(side="right", padx=6)
        tk.Button(
            header,
            text="使用说明",
            command=self.open_manual,
            bg="#0B7A5F",
            fg="#FFFFFF",
            activebackground="#059669",
            relief="flat",
            font=("Microsoft YaHei UI", 9),
            padx=12,
            pady=7,
            cursor="hand2",
        ).pack(side="right", padx=6)

    def _build_status(self):
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", padding=(10, 5)).pack(fill="x")

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(10, 0))
        self._build_products_tab()
        self._build_categories_tab()
        self._build_settings_tab()

    # -- 商品页 -----------------------------------------------------------

    def _build_products_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="商品管理")

        toolbar = ttk.Frame(tab)
        toolbar.pack(fill="x", pady=(0, 10))
        ttk.Label(toolbar, text="分类筛选").pack(side="left")
        self.filter_var = tk.StringVar(value="全部分类")
        self.filter_combo = ttk.Combobox(toolbar, textvariable=self.filter_var, state="readonly", width=30)
        self.filter_combo.pack(side="left", padx=(6, 18))
        self.filter_combo.bind("<<ComboboxSelected>>", lambda _event: self._refresh_product_tree())

        ttk.Label(toolbar, text="搜索").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_args: self._refresh_product_tree())
        ttk.Entry(toolbar, textvariable=self.search_var, width=26).pack(side="left", padx=6)

        ttk.Button(toolbar, text="初始化数据", style="Danger.TButton", command=self.reset_data).pack(
            side="right", padx=(18, 0)
        )
        ttk.Button(toolbar, text="新增商品", style="Accent.TButton", command=self.new_product).pack(side="right")

        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        left = ttk.Frame(paned)
        right = ttk.LabelFrame(paned, text="商品信息", padding=12)
        paned.add(left, weight=3)
        paned.add(right, weight=2)

        tree_frame = ttk.Frame(left)
        tree_frame.pack(fill="both", expand=True)
        self.product_tree = ttk.Treeview(
            tree_frame,
            columns=("title", "price", "category"),
            show="headings",
            selectmode="browse",
        )
        self.product_tree.heading("title", text="商品名称")
        self.product_tree.heading("price", text="价格")
        self.product_tree.heading("category", text="一级 / 二级分类")
        self.product_tree.column("title", width=320, anchor="w")
        self.product_tree.column("price", width=80, anchor="center")
        self.product_tree.column("category", width=230, anchor="w")
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scroll.set)
        self.product_tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        self.product_tree.bind("<<TreeviewSelect>>", self.load_product)

        actions = ttk.Frame(left)
        actions.pack(fill="x", pady=(10, 0))
        ttk.Button(actions, text="删除商品", command=self.delete_product).pack(side="left")
        ttk.Button(actions, text="上移", command=lambda: self.move_product(-1)).pack(side="left", padx=6)
        ttk.Button(actions, text="下移", command=lambda: self.move_product(1)).pack(side="left")

        right.columnconfigure(1, weight=1)

        ttk.Label(right, text="商品名称").grid(row=0, column=0, sticky="w", pady=4)
        self.title_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.title_var).grid(row=0, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(right, text="一级分类").grid(row=1, column=0, sticky="w", pady=4)
        self.product_top_var = tk.StringVar()
        self.top_combo = ttk.Combobox(right, textvariable=self.product_top_var, state="readonly")
        self.top_combo.grid(row=1, column=1, columnspan=2, sticky="ew", pady=4)
        self.top_combo.bind("<<ComboboxSelected>>", lambda _event: self._refresh_sub_options(preferred=NO_SUB))

        ttk.Label(right, text="二级分类").grid(row=2, column=0, sticky="w", pady=4)
        self.product_sub_var = tk.StringVar()
        self.sub_combo = ttk.Combobox(right, textvariable=self.product_sub_var, state="readonly")
        self.sub_combo.grid(row=2, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(right, text="价格").grid(row=3, column=0, sticky="w", pady=4)
        self.price_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.price_var, width=18).grid(row=3, column=1, sticky="w", pady=4)
        ttk.Label(right, text="元").grid(row=3, column=2, sticky="w")

        ttk.Label(right, text="图片").grid(row=4, column=0, sticky="w", pady=4)
        self.image_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.image_var, state="readonly").grid(
            row=4, column=1, sticky="ew", pady=4
        )
        ttk.Button(right, text="选择图片", command=self.choose_image).grid(
            row=4, column=2, sticky="w", padx=(6, 0)
        )

        preview_box = tk.Frame(right, height=210, bg="#F7FFFB", relief="solid", borderwidth=1)
        preview_box.grid(row=5, column=0, columnspan=3, pady=(6, 10), sticky="ew")
        preview_box.grid_propagate(False)
        self.preview_label = tk.Label(
            preview_box,
            text=IMAGE_HINT,
            bg="#F7FFFB",
            fg="#9AA0A6",
            justify="center",
        )
        self.preview_label.pack(fill="both", expand=True)

        ttk.Label(right, text="商品描述\n（显示在详情页）", justify="left").grid(
            row=6, column=0, sticky="nw", pady=4
        )
        self.description_text = tk.Text(
            right,
            height=7,
            wrap="word",
            relief="solid",
            borderwidth=1,
            font=("Microsoft YaHei UI", 10),
        )
        self.description_text.grid(row=6, column=1, columnspan=2, sticky="nsew", pady=4)
        right.rowconfigure(6, weight=1)

        buttons = ttk.Frame(right)
        buttons.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(12, 0))
        ttk.Button(buttons, text="保存商品", style="Accent.TButton", command=self.save_product).pack(
            side="left"
        )
        ttk.Button(buttons, text="更多信息", command=self.edit_extra).pack(side="left", padx=8)
        ttk.Button(buttons, text="清空表单", command=self.new_product).pack(side="left", padx=8)

    # -- 分类页 -----------------------------------------------------------

    def _build_categories_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="分类 / 导航")

        ttk.Label(
            tab,
            text="一级分类 = 顶部导航菜单；二级分类 = 下拉菜单项。导航按“排序”自动生成，不用手改代码。",
            foreground="#475569",
        ).pack(anchor="w", pady=(0, 8))

        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)

        left = ttk.Frame(paned)
        right = ttk.LabelFrame(paned, text="分类信息", padding=12)
        paned.add(left, weight=3)
        paned.add(right, weight=2)

        tree_frame = ttk.Frame(left)
        tree_frame.pack(fill="both", expand=True)
        self.category_tree = ttk.Treeview(
            tree_frame,
            columns=("id", "count", "nav", "level"),
            show="tree headings",
            selectmode="browse",
        )
        self.category_tree.heading("#0", text="分类名称")
        self.category_tree.heading("id", text="分类 ID")
        self.category_tree.heading("count", text="商品数")
        self.category_tree.heading("nav", text="导航")
        self.category_tree.heading("level", text="层级")
        self.category_tree.column("#0", width=220, anchor="w")
        self.category_tree.column("id", width=130, anchor="w")
        self.category_tree.column("count", width=70, anchor="center")
        self.category_tree.column("nav", width=60, anchor="center")
        self.category_tree.column("level", width=60, anchor="center")
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=scroll.set)
        self.category_tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        self.category_tree.bind("<<TreeviewSelect>>", self.load_category)

        actions = ttk.Frame(left)
        actions.pack(fill="x", pady=(10, 0))
        ttk.Button(actions, text="新增一级分类", style="Accent.TButton", command=self.new_top_category).pack(
            side="left"
        )
        ttk.Button(actions, text="新增二级分类", command=self.new_child_category).pack(side="left", padx=8)
        ttk.Button(actions, text="删除分类", command=self.delete_category).pack(side="left")

        right.columnconfigure(1, weight=1)

        ttk.Label(right, text="分类 ID").grid(row=0, column=0, sticky="w", pady=4)
        self.category_id_var = tk.StringVar()
        self.category_id_entry = ttk.Entry(right, textvariable=self.category_id_var)
        self.category_id_entry.grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Label(right, text="英文小写，例如 relx-disposable", foreground="#777").grid(
            row=1, column=1, sticky="w"
        )

        ttk.Label(right, text="分类名称").grid(row=2, column=0, sticky="w", pady=4)
        self.category_name_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.category_name_var).grid(
            row=2, column=1, sticky="ew", pady=4
        )

        ttk.Label(right, text="分类描述").grid(row=3, column=0, sticky="nw", pady=4)
        self.category_desc_text = tk.Text(
            right,
            height=5,
            wrap="word",
            relief="solid",
            borderwidth=1,
            font=("Microsoft YaHei UI", 10),
        )
        self.category_desc_text.grid(row=3, column=1, sticky="nsew", pady=4)
        right.rowconfigure(3, weight=1)

        ttk.Label(right, text="上级分类").grid(row=4, column=0, sticky="w", pady=4)
        self.category_parent_var = tk.StringVar()
        self.category_parent_combo = ttk.Combobox(
            right, textvariable=self.category_parent_var, state="readonly"
        )
        self.category_parent_combo.grid(row=4, column=1, sticky="ew", pady=4)

        ttk.Label(right, text="排序").grid(row=5, column=0, sticky="w", pady=4)
        self.category_sort_var = tk.StringVar(value="10")
        ttk.Spinbox(right, from_=1, to=999, textvariable=self.category_sort_var, width=8).grid(
            row=5, column=1, sticky="w", pady=4
        )

        self.category_nav_var = tk.BooleanVar(value=True)
        self.category_nav_check = ttk.Checkbutton(
            right, text="显示在顶部导航", variable=self.category_nav_var
        )
        self.category_nav_check.grid(row=6, column=1, sticky="w", pady=4)

        ttk.Label(right, text="自定义链接").grid(row=7, column=0, sticky="w", pady=4)
        self.category_link_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.category_link_var).grid(
            row=7, column=1, sticky="ew", pady=4
        )
        ttk.Label(
            right,
            text="一般留空。联系客服这类非商品菜单可填 /contact。",
            foreground="#777",
        ).grid(row=8, column=1, sticky="w")

        ttk.Label(
            right,
            text="二级分类的商品放在上级分类里；保存商品时选择一级 + 二级即可。",
            foreground="#475569",
            wraplength=320,
            justify="left",
        ).grid(row=9, column=0, columnspan=2, sticky="w", pady=(8, 0))

        buttons = ttk.Frame(right)
        buttons.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        ttk.Button(buttons, text="保存分类", style="Accent.TButton", command=self.save_category).pack(
            side="left"
        )
        ttk.Button(buttons, text="新增一级", command=self.new_top_category).pack(side="left", padx=8)

    # -- 站点设置 ---------------------------------------------------------

    def _build_settings_tab(self):
        tab = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(tab, text="站点设置")
        tab.columnconfigure(1, weight=1)

        general = self.general
        hero = general.get("hero", {})
        shipping = general.get("shipping", {})
        payment = general.get("payment", {})

        ttk.Label(tab, text="公告文字").grid(row=0, column=0, sticky="w", pady=5)
        self.announce_var = tk.StringVar(value=general.get("announcement", ""))
        ttk.Entry(tab, textvariable=self.announce_var).grid(row=0, column=1, columnspan=2, sticky="ew", pady=5)

        ttk.Label(tab, text="公告右侧").grid(row=1, column=0, sticky="w", pady=5)
        self.announce_right_var = tk.StringVar(value=general.get("announcementRight", ""))
        ttk.Entry(tab, textvariable=self.announce_right_var).grid(row=1, column=1, columnspan=2, sticky="ew", pady=5)

        ttk.Label(tab, text="首页 Banner 链接").grid(row=5, column=0, sticky="w", pady=5)
        self.hero_link_var = tk.StringVar(value=hero.get("link", ""))
        ttk.Entry(tab, textvariable=self.hero_link_var).grid(row=5, column=1, columnspan=2, sticky="ew", pady=5)

        ttk.Label(tab, text="包邮门槛 / 运费").grid(row=6, column=0, sticky="w", pady=5)
        ship_frame = ttk.Frame(tab)
        ship_frame.grid(row=6, column=1, columnspan=2, sticky="w", pady=5)
        self.free_over_var = tk.StringVar(value=str(shipping.get("freeOver", 138)))
        self.ship_fee_var = tk.StringVar(value=str(shipping.get("fee", 8)))
        ttk.Entry(ship_frame, textvariable=self.free_over_var, width=10).pack(side="left")
        ttk.Label(ship_frame, text="元包邮，运费").pack(side="left", padx=6)
        ttk.Entry(ship_frame, textvariable=self.ship_fee_var, width=8).pack(side="left")
        ttk.Label(ship_frame, text="元").pack(side="left", padx=4)

        ttk.Label(tab, text="客服 QQ").grid(row=7, column=0, sticky="w", pady=5)
        self.qq_var = tk.StringVar(value=str((self.contacts.get("qq") or {}).get("number", "")))
        ttk.Entry(tab, textvariable=self.qq_var).grid(row=7, column=1, columnspan=2, sticky="ew", pady=5)

        ttk.Label(tab, text="收款二维码").grid(row=8, column=0, sticky="w", pady=5)
        self.payment_path_var = tk.StringVar(value=payment.get("qr", ""))
        pay_row = ttk.Frame(tab)
        pay_row.grid(row=8, column=1, columnspan=2, sticky="ew", pady=5)
        ttk.Entry(pay_row, textvariable=self.payment_path_var, state="readonly").pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(pay_row, text="选择图片", command=self.choose_payment_image).pack(side="left", padx=(6, 0))

        self.payment_preview = tk.Label(
            tab,
            text="未选择收款码\n建议使用企业微信收款码",
            bg="#F7FFFB",
            fg="#9AA0A6",
            width=22,
            height=8,
            relief="solid",
            borderwidth=1,
            justify="center",
        )
        self.payment_preview.grid(row=9, column=0, columnspan=3, pady=10)
        self._show_payment_preview(payment.get("qr", ""))

        ttk.Label(
            tab,
            text="保存后会写入 src/data/site/general.json 和 contacts.json；发布时会一并提交收款码图片。",
            foreground="#777",
        ).grid(row=10, column=0, columnspan=3, sticky="w")

        ttk.Button(tab, text="保存站点设置", style="Accent.TButton", command=self.save_settings).grid(
            row=11, column=0, columnspan=3, sticky="w", pady=(14, 0)
        )

    def choose_payment_image(self):
        initial = self._last_image_dir
        if not initial:
            pictures = Path.home() / "Pictures"
            initial = str(pictures if pictures.exists() else ROOT)
        path = filedialog.askopenfilename(
            title="选择收款二维码图片",
            initialdir=initial,
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.webp *.bmp"),
                ("所有文件", "*.*"),
            ],
        )
        if not path:
            return
        self._last_image_dir = str(Path(path).parent)
        self.pending_payment_image = path
        self.payment_path_var.set(path)
        self._show_payment_preview(path)
        self.status_var.set("已选择收款码，点“保存站点设置”后生效")

    def _show_payment_preview(self, path_value):
        self._pay_photo = None
        if not path_value:
            self.payment_preview.configure(image="", text="未选择收款码\n建议使用企业微信收款码")
            return
        path = Path(path_value)
        if not path.is_absolute():
            path = ROOT / "public" / str(path_value).lstrip("/")
        if not path.exists():
            self.payment_preview.configure(image="", text="图片不存在")
            return
        try:
            with Image.open(path) as opened:
                image = opened.convert("RGB")
                resampling = getattr(Image, "Resampling", Image)
                image.thumbnail((180, 180), resampling.LANCZOS)
                self._pay_photo = ImageTk.PhotoImage(image)
            self.payment_preview.configure(image=self._pay_photo, text="")
        except Exception as error:
            self.payment_preview.configure(image="", text=f"预览失败：{error}")

    def _process_payment_image(self, source):
        if Image is None:
            raise RuntimeError("缺少 Pillow")
        PAYMENT_IMAGE.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as opened:
            image = ImageOps.exif_transpose(opened) if ImageOps else opened
            if image.mode in ("RGBA", "LA"):
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            else:
                image = image.convert("RGB")
            resampling = getattr(Image, "Resampling", Image)
            image.thumbnail((700, 700), resampling.LANCZOS)
            image.save(PAYMENT_IMAGE, "WEBP", quality=90, method=6)
        return "/images/payment-qr.webp"

    def save_settings(self):
        try:
            free_over = compact_price(self.free_over_var.get().strip())
            ship_fee = compact_price(self.ship_fee_var.get().strip())
            if float(free_over) < 0 or float(ship_fee) < 0:
                raise ValueError
        except (TypeError, ValueError):
            messagebox.showwarning("金额不正确", "包邮门槛和运费需要填写大于等于 0 的数字。")
            return

        if self.pending_payment_image:
            try:
                qr_path = self._process_payment_image(self.pending_payment_image)
            except Exception as error:
                messagebox.showerror("收款码处理失败", str(error))
                return
            self.payment_path_var.set(qr_path)
            self.pending_payment_image = None

        self.general["announcement"] = self.announce_var.get().strip()
        self.general["announcementRight"] = self.announce_right_var.get().strip()
        hero = self.general.setdefault("hero", {})
        hero["link"] = self.hero_link_var.get().strip()
        self.general.setdefault("shipping", {})["freeOver"] = free_over
        self.general["shipping"]["fee"] = ship_fee
        self.general.setdefault("payment", {})["qr"] = self.payment_path_var.get().strip()
        self.contacts.setdefault("qq", {})["number"] = self.qq_var.get().strip()

        write_json(GENERAL_FILE, self.general)
        write_json(CONTACTS_FILE, self.contacts)
        self._show_payment_preview(self.payment_path_var.get().strip())
        self.status_var.set("站点设置已保存")
        messagebox.showinfo("保存成功", "站点设置已保存。发布到 GitHub 后前台生效。")

    # -- 分类辅助 ---------------------------------------------------------

    def _top_choices(self, with_section_only=True):
        choices = []
        used_labels = set()
        for category_id, category in category_tops(self.categories):
            if with_section_only and not category.get("section"):
                continue
            label = category.get("title") or category_id
            if label in used_labels:
                label = f"{label}（{category_id}）"
            used_labels.add(label)
            choices.append((label, category_id))
        return choices

    def _top_label_for(self, category_id):
        for label, cid in self._top_choices(with_section_only=False):
            if cid == category_id:
                return label
        return ""

    def _top_for_section(self, section_id):
        candidates = [
            (cid, category)
            for cid, category in category_tops(self.categories)
            if category.get("section") == section_id
        ]
        if not candidates:
            return None, None
        for cid, category in candidates:
            if cid == section_id:
                return cid, category
        return candidates[0]

    def _product_category_text(self, section_id, product):
        top_id, top = self._top_for_section(section_id)
        title = top.get("title", section_id) if top else section_id
        subcategory = self.categories.get(product.get("subcategory") or "")
        if subcategory:
            return f"{title} / {subcategory.get('title', '')}"
        return title

    def _assignments_for_child(self, child_id):
        child = self.categories.get(child_id) or {}
        parent_id = child.get("parent")
        parent = self.categories.get(parent_id) or {}
        section_id = parent.get("section")
        section = self.sections.get(section_id) or {}
        return [
            item
            for item in section.get("products", [])
            if item.get("subcategory") == child_id
        ]

    # -- 数据刷新 ---------------------------------------------------------

    def _refresh_all(self):
        self._refresh_filter_options()
        self._refresh_product_top_options()
        self._refresh_product_tree()
        self._refresh_category_tree()

    def _refresh_filter_options(self):
        options = ["全部分类"]
        mapping = {"全部分类": (None, None)}
        for label, top_id in self._top_choices():
            section_id = self.categories.get(top_id, {}).get("section")
            options.append(label)
            mapping[label] = (section_id, None)
            for child_id, child in children_of(self.categories, top_id):
                child_label = f"{label} / {child.get('title', child_id)}"
                options.append(child_label)
                mapping[child_label] = (section_id, child_id)
        self.filter_map = mapping
        current = self.filter_var.get()
        self.filter_combo["values"] = options
        if current not in mapping:
            self.filter_var.set("全部分类")

    def _refresh_product_top_options(self):
        choices = self._top_choices()
        labels = [label for label, _cid in choices]
        self.product_top_labels = {label: cid for label, cid in choices}
        current = self.product_top_var.get()
        self.top_combo["values"] = labels
        if current not in labels:
            self.product_top_var.set(labels[0] if labels else "")
        self._refresh_sub_options()

    def _refresh_sub_options(self, preferred=None):
        top_id = self.product_top_labels.get(self.product_top_var.get())
        values = [NO_SUB]
        mapping = {NO_SUB: None}
        for child_id, child in children_of(self.categories, top_id) if top_id else []:
            label = child.get("title", child_id)
            if label in mapping:
                label = f"{label}（{child_id}）"
            values.append(label)
            mapping[label] = child_id

        self.product_sub_labels = mapping
        self.sub_combo["values"] = values
        self.sub_combo.configure(state="readonly" if len(values) > 1 else "disabled")
        current = preferred if preferred is not None else self.product_sub_var.get()
        if current not in mapping:
            current = NO_SUB
        self.product_sub_var.set(current)

    def _refresh_product_tree(self):
        selected = self.product_tree.selection()
        selected_id = selected[0] if selected else None
        self.product_tree.delete(*self.product_tree.get_children())
        self.row_map = {}
        filter_section, filter_sub = self.filter_map.get(self.filter_var.get(), (None, None))
        search = self.search_var.get().strip().lower()

        for section in sorted_sections(self.sections):
            section_id = section.get("id")
            if filter_section and section_id != filter_section:
                continue
            for index, product in enumerate(section.get("products", [])):
                if filter_sub and product.get("subcategory") != filter_sub:
                    continue
                title = str(product.get("title", ""))
                if search and search not in title.lower():
                    continue
                iid = f"{section_id}:{index}"
                self.product_tree.insert(
                    "",
                    "end",
                    iid=iid,
                    values=(
                        title,
                        f"￥{product.get('price', '')}",
                        self._product_category_text(section_id, product),
                    ),
                )
                self.row_map[iid] = (section_id, index)

        if selected_id and selected_id in self.row_map:
            self.product_tree.selection_set(selected_id)
            self.product_tree.see(selected_id)

    def _refresh_category_tree(self):
        selected = self.category_tree.selection()
        selected_id = selected[0] if selected else None
        self.category_tree.delete(*self.category_tree.get_children())

        for category_id, category in category_tops(self.categories):
            section_id = category.get("section")
            count = len(self.sections.get(section_id, {}).get("products", [])) if section_id else 0
            nav_text = "显示" if category.get("nav", True) else "隐藏"
            self.category_tree.insert(
                "",
                "end",
                iid=category_id,
                text=category.get("title", category_id),
                values=(category_id, count, nav_text, "一级"),
                open=True,
            )
            for child_id, child in children_of(self.categories, category_id):
                child_count = len(self._assignments_for_child(child_id))
                self.category_tree.insert(
                    category_id,
                    "end",
                    iid=child_id,
                    text=child.get("title", child_id),
                    values=(child_id, child_count, "-", "二级"),
                )

        if selected_id and self.category_tree.exists(selected_id):
            self.category_tree.selection_set(selected_id)
            self.category_tree.see(selected_id)

    # -- 商品操作 ---------------------------------------------------------

    def _clear_preview(self):
        self._preview_photo = None
        self.preview_label.configure(image="", text=IMAGE_HINT)

    def _show_preview(self, path_value):
        self._preview_photo = None
        if not path_value:
            self._clear_preview()
            return
        path = Path(path_value)
        if not path.is_absolute():
            path = image_path(str(path_value)) or path
        if not path.exists():
            self.preview_label.configure(image="", text="图片不存在")
            return
        try:
            with Image.open(path) as opened:
                image = opened.convert("RGB")
                resampling = getattr(Image, "Resampling", Image)
                image.thumbnail((320, 200), resampling.LANCZOS)
                self._preview_photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=self._preview_photo, text="")
        except Exception as error:
            self.preview_label.configure(image="", text=f"预览失败：{error}")

    @staticmethod
    def _empty_extra():
        return {
            "brand": "",
            "badges": [],
            "priceMax": None,
            "stock": True,
            "hot": False,
            "options": [],
            "specs": {},
        }

    def _extra_has_data(self):
        extra = self.extra
        return bool(
            extra.get("brand")
            or extra.get("badges")
            or extra.get("priceMax")
            or extra.get("hot")
            or extra.get("options")
            or extra.get("specs")
            or extra.get("stock", True) is False
        )

    @staticmethod
    def _options_text(options):
        lines = []
        for item in options or []:
            if isinstance(item, dict):
                line = f"{item.get('label', '')}|{item.get('price', '')}"
                if item.get("stock") is False:
                    line += "|无货"
                lines.append(line)
            else:
                lines.append(str(item))
        return "\n".join(lines)

    @staticmethod
    def _specs_text(specs):
        if not isinstance(specs, dict):
            return ""
        return "\n".join(f"{key}|{value}" for key, value in specs.items())

    def _extra_from_product(self, product):
        extra = self._empty_extra()
        if not product:
            return extra
        extra["brand"] = str(product.get("brand", ""))
        extra["badges"] = list(product.get("badges") or [])
        extra["priceMax"] = product.get("priceMax")
        extra["stock"] = product.get("stock", True) is not False
        extra["hot"] = product.get("hot") is True
        extra["options"] = list(product.get("options") or [])
        extra["specs"] = dict(product.get("specs") or {})
        return extra

    def _extra_to_product(self, product):
        extra = self.extra
        product["brand"] = str(extra.get("brand", "")).strip()
        if not product["brand"]:
            product.pop("brand", None)

        badges = [str(item).strip() for item in extra.get("badges") or [] if str(item).strip()]
        if badges:
            product["badges"] = badges
        else:
            product.pop("badges", None)

        price_max = extra.get("priceMax")
        if price_max not in (None, ""):
            product["priceMax"] = compact_price(price_max)
        else:
            product.pop("priceMax", None)

        if extra.get("stock", True) is False:
            product["stock"] = False
        else:
            product.pop("stock", None)

        if extra.get("hot"):
            product["hot"] = True
        else:
            product.pop("hot", None)

        if extra.get("options"):
            product["options"] = extra["options"]
        else:
            product.pop("options", None)

        if extra.get("specs"):
            product["specs"] = extra["specs"]
        else:
            product.pop("specs", None)

    def edit_extra(self):
        dialog = tk.Toplevel(self)
        dialog.title("更多商品信息")
        dialog.geometry("640x700")
        dialog.transient(self)
        dialog.grab_set()
        dialog.columnconfigure(1, weight=1)

        brand_var = tk.StringVar(value=self.extra.get("brand", ""))
        badges_var = tk.StringVar(value="，".join(self.extra.get("badges") or []))
        price_max_var = tk.StringVar(value=str(self.extra.get("priceMax") or ""))
        stock_var = tk.BooleanVar(value=self.extra.get("stock", True))
        hot_var = tk.BooleanVar(value=self.extra.get("hot", False))

        ttk.Label(dialog, text="品牌").grid(row=0, column=0, sticky="w", padx=12, pady=6)
        ttk.Entry(dialog, textvariable=brand_var).grid(row=0, column=1, columnspan=2, sticky="ew", padx=(0, 12), pady=6)

        ttk.Label(dialog, text="角标 / 标签").grid(row=1, column=0, sticky="w", padx=12, pady=6)
        ttk.Entry(dialog, textvariable=badges_var).grid(row=1, column=1, columnspan=2, sticky="ew", padx=(0, 12), pady=6)
        ttk.Label(dialog, text="活动角标显示右上；自定义/呼吸灯/凉度调节等功能标签显示图片左下", foreground="#777").grid(
            row=2, column=1, columnspan=2, sticky="w", padx=(0, 12)
        )

        ttk.Label(dialog, text="价格上限").grid(row=3, column=0, sticky="w", padx=12, pady=6)
        ttk.Entry(dialog, textvariable=price_max_var, width=16).grid(row=3, column=1, sticky="w", padx=(0, 12), pady=6)
        ttk.Label(dialog, text="留空表示单一价格；填写后前台显示价格区间", foreground="#777").grid(
            row=4, column=1, columnspan=2, sticky="w", padx=(0, 12)
        )

        ttk.Checkbutton(dialog, text="现货（取消勾选显示“无货”）", variable=stock_var).grid(
            row=5, column=1, sticky="w", padx=(0, 12), pady=6
        )
        ttk.Checkbutton(dialog, text="在卡片显示 HOT 角标", variable=hot_var).grid(
            row=6, column=1, sticky="w", padx=(0, 12), pady=6
        )

        ttk.Label(dialog, text="口味 / 规格").grid(row=7, column=0, sticky="nw", padx=12, pady=6)
        options_text = tk.Text(dialog, height=7, wrap="word", relief="solid", borderwidth=1)
        options_text.grid(row=7, column=1, columnspan=2, sticky="nsew", padx=(0, 12), pady=6)
        options_text.insert("1.0", self._options_text(self.extra.get("options")))
        ttk.Label(dialog, text="每行一个口味；单独价格写：名称|价格；该口味无货写：名称|价格|无货", foreground="#777").grid(
            row=8, column=1, columnspan=2, sticky="w", padx=(0, 12)
        )

        ttk.Label(dialog, text="参数").grid(row=9, column=0, sticky="nw", padx=12, pady=6)
        specs_text = tk.Text(dialog, height=6, wrap="word", relief="solid", borderwidth=1)
        specs_text.grid(row=9, column=1, columnspan=2, sticky="nsew", padx=(0, 12), pady=6)
        specs_text.insert("1.0", self._specs_text(self.extra.get("specs")))
        ttk.Label(dialog, text="每行一个参数，格式：键|值，例如 口数|18000", foreground="#777").grid(
            row=10, column=1, columnspan=2, sticky="w", padx=(0, 12)
        )

        dialog.rowconfigure(9, weight=1)

        def save_extra():
            brand = brand_var.get().strip()
            badges = [
                item.strip()
                for item in re.split(r"[,，]", badges_var.get())
                if item.strip()
            ]
            price_max_raw = price_max_var.get().strip()
            try:
                price_max = compact_price(price_max_raw) if price_max_raw else None
                if price_max is not None and float(price_max) <= 0:
                    raise ValueError
            except (TypeError, ValueError):
                messagebox.showwarning("价格上限不正确", "价格上限需要留空或填写大于 0 的数字。", parent=dialog)
                return

            options = []
            for line in options_text.get("1.0", "end").splitlines():
                line = line.strip()
                if not line:
                    continue
                if "|" in line:
                    parts = line.split("|")
                    label = parts[0].strip()
                    price_raw = parts[1].strip() if len(parts) > 1 else ""
                    flag = "|".join(parts[2:]).strip()
                    out_of_stock = any(word in flag for word in ("无货", "缺货", "售罄"))
                    if not label:
                        messagebox.showwarning("口味名称缺失", f"这一行缺少名称：{line}", parent=dialog)
                        return
                    option = {"label": label}
                    if price_raw:
                        try:
                            price_value = compact_price(price_raw)
                            if float(price_value) <= 0:
                                raise ValueError
                        except (TypeError, ValueError):
                            messagebox.showwarning("口味价格不正确", f"这一行价格不正确：{line}", parent=dialog)
                            return
                        option["price"] = price_value
                    if out_of_stock:
                        option["stock"] = False
                    if len(option) == 1:
                        options.append(label)
                    else:
                        options.append(option)
                else:
                    options.append(line)

            specs = {}
            for line in specs_text.get("1.0", "end").splitlines():
                line = line.strip()
                if not line:
                    continue
                if "|" not in line:
                    messagebox.showwarning("参数格式不正确", f"请使用 键|值 格式：{line}", parent=dialog)
                    return
                key, value = line.split("|", 1)
                key = key.strip()
                if not key:
                    messagebox.showwarning("参数名称缺失", f"这一行缺少名称：{line}", parent=dialog)
                    return
                specs[key] = value.strip()

            self.extra = {
                "brand": brand,
                "badges": badges,
                "priceMax": price_max,
                "stock": bool(stock_var.get()),
                "hot": bool(hot_var.get()),
                "options": options,
                "specs": specs,
            }
            dialog.destroy()
            self.status_var.set("更多信息已更新，记得点“保存商品”")

        buttons = ttk.Frame(dialog)
        buttons.grid(row=11, column=0, columnspan=3, sticky="e", padx=12, pady=12)
        ttk.Button(buttons, text="保存", style="Accent.TButton", command=save_extra).pack(side="left")
        ttk.Button(buttons, text="取消", command=dialog.destroy).pack(side="left", padx=8)

    def new_product(self):
        self.current_section = None
        self.current_index = None
        self.pending_image = None
        self.extra = self._empty_extra()
        self.title_var.set("")
        self.price_var.set("")
        self.image_var.set("")
        self.description_text.delete("1.0", "end")

        filter_section, filter_sub = self.filter_map.get(self.filter_var.get(), (None, None))
        top_id, _top = self._top_for_section(filter_section) if filter_section else (None, None)
        if top_id:
            self.product_top_var.set(self._top_label_for(top_id))
            self._refresh_sub_options(preferred=NO_SUB)
            if filter_sub:
                for label, cid in self.product_sub_labels.items():
                    if cid == filter_sub:
                        self.product_sub_var.set(label)
                        break
        else:
            self.product_top_var.set("")
            self._refresh_sub_options(preferred=NO_SUB)

        self._clear_preview()
        self.status_var.set("新建商品：填写信息后点击“保存商品”")

    def load_product(self, _event=None):
        selection = self.product_tree.selection()
        if not selection:
            return
        iid = selection[0]
        key = self.row_map.get(iid)
        if not key:
            return
        section_id, index = key
        section = self.sections.get(section_id)
        if not section or index >= len(section.get("products", [])):
            return
        product = section["products"][index]
        self.current_section = section_id
        self.current_index = index
        self.pending_image = None
        self.extra = self._extra_from_product(product)

        self.title_var.set(product.get("title", ""))
        self.price_var.set(str(product.get("price", "")))
        self.image_var.set(product.get("localImage", ""))
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", product.get("description", ""))

        top_id, _top = self._top_for_section(section_id)
        if top_id:
            self.product_top_var.set(self._top_label_for(top_id))
            self._refresh_sub_options(preferred=NO_SUB)
            subcategory = product.get("subcategory")
            for label, cid in self.product_sub_labels.items():
                if cid == subcategory:
                    self.product_sub_var.set(label)
                    break
        else:
            self.product_top_var.set("")
            self._refresh_sub_options(preferred=NO_SUB)

        self._show_preview(product.get("localImage", ""))
        self.status_var.set(f"正在编辑：{product.get('title', '')}")

    def choose_image(self):
        initial = self._last_image_dir
        if not initial:
            pictures = Path.home() / "Pictures"
            initial = str(pictures if pictures.exists() else ROOT)
        path = filedialog.askopenfilename(
            title="选择商品图片（保存时自动压缩到 public/images/products）",
            initialdir=initial,
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.webp *.bmp"),
                ("所有文件", "*.*"),
            ],
        )
        if not path:
            return
        self._last_image_dir = str(Path(path).parent)
        self.pending_image = path
        self.image_var.set(path)
        self._show_preview(path)
        self.status_var.set("已选择新图片，保存时会自动压缩并复制到 public/images/products")

    def save_product(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("缺少名称", "请填写商品名称。")
            return False
        try:
            price = compact_price(self.price_var.get().strip())
            if float(price) <= 0:
                raise ValueError
        except (TypeError, ValueError):
            messagebox.showwarning("价格不正确", "请填写大于 0 的商品价格。")
            return False

        top_id = self.product_top_labels.get(self.product_top_var.get())
        if not top_id:
            messagebox.showwarning("缺少分类", "请选择一级分类。")
            return False
        section_id = self.categories.get(top_id, {}).get("section")
        if not section_id or section_id not in self.sections:
            messagebox.showwarning("分类未关联分区", "该一级分类没有可用商品分区，请先在分类管理中处理。")
            return False
        sub_id = self.product_sub_labels.get(self.product_sub_var.get())

        existing = None
        if self.current_section and self.current_index is not None:
            products = self.sections.get(self.current_section, {}).get("products", [])
            if self.current_index < len(products):
                existing = products[self.current_index]

        local_image = existing.get("localImage", "") if existing else ""
        if self.pending_image:
            try:
                local_image = process_image(self.pending_image, section_id)
            except Exception as error:
                messagebox.showerror("图片处理失败", str(error))
                return False
        if not local_image:
            messagebox.showwarning("缺少图片", "请选择一张商品图片。")
            return False

        product = dict(existing) if existing else {}
        product.update(
            {
                "title": title,
                "price": price,
                "imageAlt": title,
                "localImage": local_image,
            }
        )
        self._extra_to_product(product)
        if sub_id:
            product["subcategory"] = sub_id
        else:
            product.pop("subcategory", None)

        description = self.description_text.get("1.0", "end").strip()
        if description:
            product["description"] = description
        else:
            product.pop("description", None)

        if existing:
            if self.current_section == section_id:
                self.sections[section_id]["products"][self.current_index] = product
                target_index = self.current_index
            else:
                self.sections[self.current_section]["products"].pop(self.current_index)
                self.sections[section_id]["products"].append(product)
                target_index = len(self.sections[section_id]["products"]) - 1
        else:
            self.sections[section_id]["products"].append(product)
            target_index = len(self.sections[section_id]["products"]) - 1

        self.save_all()
        self._refresh_all()
        iid = f"{section_id}:{target_index}"
        if iid in self.row_map:
            self.product_tree.selection_set(iid)
            self.product_tree.see(iid)
        self.current_section = section_id
        self.current_index = target_index
        self.pending_image = None
        self.status_var.set(f"已保存商品：{title}")
        return True

    def delete_product(self):
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showinfo("未选择商品", "请先在列表中选择一个商品。")
            return
        section_id, index = self.row_map[selection[0]]
        product = self.sections[section_id]["products"][index]
        if not messagebox.askyesno("删除商品", f"确定删除“{product.get('title', '')}”吗？"):
            return
        self.sections[section_id]["products"].pop(index)
        self.save_all()
        self.new_product()
        self._refresh_all()
        self.status_var.set("商品已删除")

    def move_product(self, direction):
        selection = self.product_tree.selection()
        if not selection:
            return
        section_id, index = self.row_map[selection[0]]
        products = self.sections[section_id]["products"]
        target = index + direction
        if target < 0 or target >= len(products):
            return
        products[index], products[target] = products[target], products[index]
        self.save_all()
        self._refresh_all()
        iid = f"{section_id}:{target}"
        if iid in self.row_map:
            self.product_tree.selection_set(iid)
            self.product_tree.see(iid)
        self.status_var.set("商品排序已更新")

    # -- 分类操作 ---------------------------------------------------------

    def _refresh_parent_options(self, exclude=None):
        values = [TOP_LEVEL]
        mapping = {TOP_LEVEL: None}
        used = set()
        for label, category_id in self._top_choices(with_section_only=True):
            if category_id == exclude:
                continue
            if label in used:
                label = f"{label}（{category_id}）"
            used.add(label)
            values.append(label)
            mapping[label] = category_id
        self.category_parent_labels = mapping
        self.category_parent_combo["values"] = values

    def new_top_category(self):
        self.category_mode = "new-top"
        self.editing_category = None
        self.category_tree.selection_remove(self.category_tree.selection())
        self.category_id_var.set("")
        self.category_name_var.set("")
        self.category_desc_text.delete("1.0", "end")
        self.category_link_var.set("")
        self.category_id_entry.configure(state="normal")
        self._refresh_parent_options()
        self.category_parent_combo.configure(state="readonly")
        self.category_parent_var.set(TOP_LEVEL)
        max_sort = max((cat.get("sort", 0) for cat in self.categories.values()), default=0)
        self.category_sort_var.set(str(max_sort + 1))
        self.category_nav_var.set(True)
        self.category_nav_check.configure(state="normal")
        self.status_var.set("新增一级分类：保存后会自动出现在顶部导航")

    def new_child_category(self):
        selection = self.category_tree.selection()
        parent_id = None
        if selection:
            selected_id = selection[0]
            selected = self.categories.get(selected_id) or {}
            parent_id = selected.get("parent") or selected_id
        if not parent_id:
            parent_id = next(
                (cid for cid, cat in category_tops(self.categories) if cat.get("section")),
                None,
            )
        if not parent_id:
            messagebox.showwarning("没有一级分类", "请先创建一级分类。")
            return

        self.category_mode = "new-child"
        self.editing_category = None
        self.category_tree.selection_remove(self.category_tree.selection())
        self.category_id_var.set("")
        self.category_name_var.set("")
        self.category_desc_text.delete("1.0", "end")
        self.category_link_var.set("")
        self.category_id_entry.configure(state="normal")
        self._refresh_parent_options(exclude=None)
        self.category_parent_combo.configure(state="readonly")
        self.category_parent_var.set(self._top_label_for(parent_id))
        self.category_sort_var.set(str(len(children_of(self.categories, parent_id)) + 1))
        self.category_nav_var.set(True)
        self.category_nav_check.configure(state="disabled")
        self.status_var.set("新增二级分类：商品可归到这个末级分类")

    def load_category(self, _event=None):
        selection = self.category_tree.selection()
        if not selection:
            return
        category_id = selection[0]
        category = self.categories.get(category_id)
        if not category:
            return

        self.category_mode = "edit"
        self.editing_category = category_id
        self.category_id_var.set(category_id)
        self.category_id_entry.configure(state="disabled")
        self.category_name_var.set(category.get("title", ""))
        self.category_desc_text.delete("1.0", "end")
        self.category_desc_text.insert("1.0", category.get("desc", ""))
        self.category_link_var.set(category.get("to", ""))
        self.category_sort_var.set(str(category.get("sort", 10)))
        self.category_nav_var.set(bool(category.get("nav", True)))
        self.category_nav_check.configure(state="normal" if not category.get("parent") else "disabled")

        parent_id = category.get("parent")
        self._refresh_parent_options(exclude=None)
        self.category_parent_combo.configure(state="readonly")
        self.category_parent_var.set(self._top_label_for(parent_id) if parent_id else TOP_LEVEL)
        self.status_var.set(f"正在编辑分类：{category.get('title', '')}")

    def _sort_children(self):
        for category_id, category in self.categories.items():
            if category.get("parent"):
                continue
            children = [cid for cid in category.get("children", []) if cid in self.categories]
            children.sort(key=lambda cid: (self.categories[cid].get("sort", 999), cid))
            if children:
                category["children"] = children
            else:
                category.pop("children", None)

    def save_category(self):
        name = self.category_name_var.get().strip()
        if not name:
            messagebox.showwarning("缺少名称", "请填写分类名称。")
            return
        desc = self.category_desc_text.get("1.0", "end").strip()
        try:
            sort = int(self.category_sort_var.get().strip())
        except (TypeError, ValueError):
            sort = 999
        link = self.category_link_var.get().strip()
        parent_id = self.category_parent_labels.get(self.category_parent_var.get())

        if self.category_mode in ("new-top", "new-child"):
            category_id = self.category_id_var.get().strip()
            if not CATEGORY_ID_RE.match(category_id):
                messagebox.showwarning("ID 不正确", "分类 ID 只能使用小写字母、数字和短横线，例如 new-pods。")
                return
            if category_id in self.categories:
                messagebox.showwarning("ID 重复", "该分类 ID 已存在。")
                return
            if self.category_mode == "new-top" and category_id in self.sections:
                messagebox.showwarning("分区重复", "该商品分区已存在，请换一个 ID。")
                return

            if self.category_mode == "new-child":
                if not parent_id:
                    messagebox.showwarning("缺少上级", "请选择上级一级分类。")
                    return
                if not (self.categories.get(parent_id) or {}).get("section"):
                    messagebox.showwarning("上级没有分区", "该一级分类没有商品分区，不能添加二级分类。")
                    return
                self.categories[category_id] = {
                    "title": name,
                    "desc": desc,
                    "parent": parent_id,
                    "sort": sort,
                }
                self.categories[parent_id].setdefault("children", []).append(category_id)
            else:
                section = category_id
                if section not in self.sections:
                    self.sections[section] = {
                        "id": section,
                        "title": name,
                        "sort": sort,
                        "products": [],
                    }
                category = {
                    "title": name,
                    "desc": desc,
                    "section": section,
                    "sort": sort,
                    "nav": bool(self.category_nav_var.get()),
                    "children": [],
                }
                if link:
                    category["to"] = link
                self.categories[category_id] = category
        else:
            category_id = self.editing_category
            category = self.categories.get(category_id)
            if not category:
                return
            is_child = bool(category.get("parent"))

            if not is_child and parent_id:
                messagebox.showwarning("不能修改层级", "一级分类不能直接改为二级分类，请新建二级分类后再移动商品。")
                return
            if is_child and not parent_id:
                messagebox.showwarning("缺少上级", "二级分类必须选择上级一级分类。")
                return
            if is_child and parent_id != category.get("parent"):
                if not (self.categories.get(parent_id) or {}).get("section"):
                    messagebox.showwarning("上级没有分区", "该一级分类没有商品分区，不能作为上级。")
                    return
                assigned = self._assignments_for_child(category_id)
                if assigned:
                    messagebox.showwarning(
                        "不能改上级",
                        f"该二级分类下还有 {len(assigned)} 个商品，请先把商品移到其它分类。",
                    )
                    return
                old_parent = self.categories.get(category.get("parent")) or {}
                old_parent["children"] = [
                    cid for cid in old_parent.get("children", []) if cid != category_id
                ]
                self.categories[parent_id].setdefault("children", []).append(category_id)
                category["parent"] = parent_id

            category["title"] = name
            category["desc"] = desc
            category["sort"] = sort
            if is_child:
                category["nav"] = True
            else:
                category["nav"] = bool(self.category_nav_var.get())
                if link:
                    category["to"] = link
                else:
                    category.pop("to", None)
                section_id = category.get("section")
                if section_id and section_id in self.sections:
                    self.sections[section_id]["title"] = name
                elif not category.get("to"):
                    section_id = category_id
                    category["section"] = section_id
                    self.sections[section_id] = {
                        "id": section_id,
                        "title": name,
                        "sort": sort,
                        "products": [],
                    }

        self._sort_children()
        self.save_all()
        self._refresh_all()
        if category_id in self.categories and self.category_tree.exists(category_id):
            self.category_tree.selection_set(category_id)
            self.category_tree.see(category_id)
        self.category_mode = "edit"
        self.editing_category = category_id
        self.category_id_entry.configure(state="disabled")
        self.status_var.set(f"已保存分类：{name}")

    def delete_category(self):
        selection = self.category_tree.selection()
        category_id = selection[0] if selection else self.editing_category
        category = self.categories.get(category_id) if category_id else None
        if not category:
            messagebox.showinfo("未选择分类", "请先在左侧选择一个分类。")
            return

        parent_id = category.get("parent")
        if parent_id:
            assigned = self._assignments_for_child(category_id)
            if assigned:
                messagebox.showwarning(
                    "分类下还有商品",
                    f"该二级分类还有 {len(assigned)} 个商品，请先移到其它分类。",
                )
                return
            if not messagebox.askyesno("删除分类", f"确定删除二级分类“{category.get('title', '')}”吗？"):
                return
            parent = self.categories.get(parent_id) or {}
            parent["children"] = [cid for cid in parent.get("children", []) if cid != category_id]
            self.categories.pop(category_id, None)
        else:
            if category_id == "hot":
                messagebox.showwarning("不能删除", "“热门产品”是首页核心分类，不能删除。")
                return
            children = children_of(self.categories, category_id)
            if children:
                messagebox.showwarning(
                    "还有二级分类",
                    "该一级分类下还有二级分类，请先删除或调整这些二级分类。",
                )
                return
            section_id = category.get("section")
            products = self.sections.get(section_id, {}).get("products", []) if section_id else []
            if products:
                messagebox.showwarning(
                    "分类下还有商品",
                    f"该分类还有 {len(products)} 个商品，请先删除或移动商品。",
                )
                return
            if not messagebox.askyesno("删除分类", f"确定删除一级分类“{category.get('title', '')}”吗？"):
                return
            self.categories.pop(category_id, None)
            if section_id:
                still_used = any(
                    item.get("section") == section_id for item in self.categories.values()
                )
                if not still_used and section_id in self.sections:
                    self.sections.pop(section_id, None)
                    path = SECTIONS_DIR / f"{section_id}.json"
                    if path.exists():
                        path.unlink()

        self._sort_children()
        self.save_all()
        self.new_top_category()
        self._refresh_all()
        self.status_var.set("分类已删除")

    # -- 保存 / 发布 ------------------------------------------------------

    def save_all(self):
        for section_id, section in list(self.sections.items()):
            write_json(SECTIONS_DIR / f"{section_id}.json", section)
        write_json(CATEGORIES_FILE, self.categories)

    def _has_unsaved_changes(self):
        title = self.title_var.get().strip()
        price = self.price_var.get().strip()
        description = self.description_text.get("1.0", "end").strip()
        image = self.image_var.get().strip()
        if not any((title, price, description, image)) and not self._extra_has_data():
            return False
        if not self.current_section or self.current_index is None:
            return True

        products = self.sections.get(self.current_section, {}).get("products", [])
        if self.current_index >= len(products):
            return True
        product = products[self.current_index]
        top_id = self.product_top_labels.get(self.product_top_var.get())
        sub_id = self.product_sub_labels.get(self.product_sub_var.get())
        existing_top_id, _top = self._top_for_section(self.current_section)
        return (
            title != str(product.get("title", ""))
            or price != str(product.get("price", ""))
            or description != str(product.get("description", ""))
            or image != str(product.get("localImage", ""))
            or top_id != existing_top_id
            or sub_id != (product.get("subcategory") or None)
            or self.extra != self._extra_from_product(product)
        )

    def reset_data(self):
        product_count = sum(
            len(section.get("products", [])) for section in self.sections.values()
        )
        image_count = (
            sum(1 for path in IMAGES_DIR.rglob("*") if path.is_file())
            if IMAGES_DIR.exists()
            else 0
        )
        if product_count == 0 and image_count == 0:
            messagebox.showinfo("已经是空数据", "当前没有商品和商品图片，不需要初始化。")
            return

        if not messagebox.askyesno(
            "初始化数据",
            f"将删除全部 {product_count} 个商品和 {image_count} 张商品图片。\n\n"
            "分类、导航、品牌信息、微信二维码会保留。\n\n"
            "清空前会自动备份到 tools\\.backups\\。\n"
            "不会自动发布，线上数据要等你点「发布到 GitHub」才会更新。\n\n"
            "确定继续吗？",
            icon="warning",
            default=messagebox.NO,
        ):
            return

        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = BACKUP_DIR / f"reset-{stamp}.zip"
        try:
            BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as archive:
                for folder in (DATA_DIR, IMAGES_DIR):
                    if not folder.exists():
                        continue
                    for path in folder.rglob("*"):
                        if path.is_file():
                            archive.write(path, path.relative_to(ROOT).as_posix())
        except Exception as error:
            messagebox.showerror("备份失败，已取消初始化", str(error))
            return

        for section in self.sections.values():
            section["products"] = []
        self.save_all()

        removed_images = 0
        if IMAGES_DIR.exists():
            for path in IMAGES_DIR.rglob("*"):
                if not path.is_file():
                    continue
                try:
                    path.unlink()
                    removed_images += 1
                except OSError:
                    pass

        self.current_section = None
        self.current_index = None
        self.pending_image = None
        self.new_product()
        self._refresh_all()
        self.status_var.set(
            f"已初始化：删除 {product_count} 个商品、{removed_images} 张图片"
        )
        messagebox.showinfo(
            "初始化完成",
            f"已删除 {product_count} 个商品、{removed_images} 张商品图片。\n"
            "分类和导航已保留。\n\n"
            f"备份：{backup_path}\n\n"
            "添加完真实商品后，点「发布到 GitHub」才会更新线上。",
        )

    def export_package(self):
        if not CATEGORIES_FILE.exists():
            messagebox.showerror(
                "找不到项目数据",
                "没有找到 src/data/site/categories.json。\n\n"
                "请把工具放在项目文件夹里（例如 tools\\）再打开。",
            )
            return
        self.save_all()
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        desktop = Path.home() / "Desktop"
        target = filedialog.asksaveasfilename(
            title="导出商品数据包",
            defaultextension=".zip",
            initialfile=f"paopao-data-{stamp}.zip",
            initialdir=str(desktop if desktop.exists() else ROOT),
            filetypes=[("ZIP 压缩包", "*.zip")],
        )
        if not target:
            return
        try:
            with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
                for folder in (DATA_DIR, IMAGES_DIR):
                    if not folder.exists():
                        continue
                    for path in folder.rglob("*"):
                        if path.is_file():
                            archive.write(path, path.relative_to(ROOT).as_posix())
        except Exception as error:
            messagebox.showerror("导出失败", str(error))
            return
        self.status_var.set(f"已导出数据包：{target}")
        messagebox.showinfo(
            "导出成功",
            "已导出商品数据和图片：\n\n"
            + target
            + "\n\n在另一台有 Git 的电脑上，把压缩包解压并覆盖到项目根目录，"
            "然后打开工具点「发布到 GitHub」即可。",
        )

    def publish(self):
        if self._has_unsaved_changes():
            if not messagebox.askyesno(
                "有未保存的修改",
                "当前表单里的商品信息还没有保存，直接发布会丢失这些修改。\n\n是否先保存商品，再发布？",
            ):
                return
            if not self.save_product():
                return
        self.save_all()
        if not shutil.which("git"):
            self.status_var.set("已保存到本地；这台电脑没有 Git，无法直接发布")
            messagebox.showwarning(
                "这台电脑没有 Git",
                "数据已经保存到本地，但这台电脑没有安装 Git，不能直接发布。\n\n"
                "请点「导出数据包」，把 zip 拷到有 Git 的电脑上，解压覆盖项目后发布。",
            )
            return
        if not (ROOT / ".git").exists():
            self.status_var.set("已保存到本地；当前目录不是 Git 仓库")
            messagebox.showwarning(
                "不是 Git 仓库",
                "数据已经保存到本地，但当前目录不是 Git 仓库，不能直接发布。\n\n"
                "请点「导出数据包」，把 zip 拷到有 Git 的项目里发布。",
            )
            return
        if not messagebox.askyesno(
            "发布到 GitHub",
            "将提交 src/data 和 public/images/products 的改动，并推送到 GitHub。\n\n"
            "GitHub Actions 会自动重新构建和部署。继续吗？",
        ):
            return

        self.status_var.set("正在提交并推送...")
        self.update_idletasks()

        add_paths = ["src/data", "public/images/products", "public/images/categories", "public/images/brands"]
        if PAYMENT_IMAGE.exists():
            add_paths.append("public/images/payment-qr.webp")
        if (ROOT / "public" / "animations").exists():
            add_paths.append("public/animations")
        add = self._run_git(["add", *add_paths])
        if add.returncode != 0:
            messagebox.showerror("git add 失败", self._command_output(add))
            return
        diff = self._run_git(["diff", "--cached", "--quiet"])
        if diff.returncode == 0:
            self.status_var.set("没有需要发布的更改")
            messagebox.showinfo("没有更改", "商品/分类数据没有变化，不需要发布。")
            return

        commit = self._run_git(
            ["commit", "-m", f"更新商品/分类数据 {datetime.now():%Y-%m-%d %H:%M}"]
        )
        if commit.returncode != 0:
            messagebox.showerror("git commit 失败", self._command_output(commit))
            return

        push = self._run_git(["push"])
        if push.returncode != 0:
            self.status_var.set("已提交到本地，推送失败")
            messagebox.showwarning(
                "已提交，但推送失败",
                "本地提交已生成，但 push 失败。检查网络/SSH 后手动执行：\n\n"
                "git push\n\n" + self._command_output(push),
            )
            return

        self.status_var.set("发布成功，等待 GitHub Actions 部署")
        messagebox.showinfo(
            "发布成功",
            "已推送到 GitHub。\n\n稍等 1-3 分钟，GitHub Actions 会自动构建并更新 Pages。\n\n"
            + self._command_output(push),
        )

    def _run_git(self, args):
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        try:
            return subprocess.run(
                ["git", *args],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
                creationflags=flags,
            )
        except FileNotFoundError:
            return subprocess.CompletedProcess(
                args, 127, stdout="", stderr="git not found"
            )

    @staticmethod
    def _command_output(result):
        return ((result.stdout or "") + (result.stderr or "")).strip()[-4000:]

    def open_manual(self):
        candidates = (ROOT / "tools" / "使用手册.md", ROOT / "README.md")
        path = next((item for item in candidates if item.exists()), None)
        if not path:
            messagebox.showwarning(
                "找不到使用说明",
                "没有找到 tools\\使用手册.md。\n\n请确认工具和项目文件夹在一起。",
            )
            return
        try:
            if os.name == "nt":
                os.startfile(path)  # type: ignore[attr-defined]
            else:
                subprocess.Popen(
                    ["open" if sys.platform == "darwin" else "xdg-open", str(path)]
                )
        except OSError:
            subprocess.Popen(["notepad.exe", str(path)])

    def open_data_dir(self):
        target = DATA_DIR
        if os.name == "nt":
            os.startfile(target)  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", str(target)])


def main() -> int:
    if "--check" in sys.argv:
        return check_data()
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0
    if Image is None:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "缺少 Pillow",
            "商品图片处理需要 Pillow。\n\n请在项目目录执行：\n"
            "pip install -r tools/requirements.txt\n\n"
            "然后重新打开工具。",
        )
        root.destroy()
        return 1
    if not CATEGORIES_FILE.exists():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "找不到项目数据",
            "没有找到 src/data/site/categories.json。\n\n"
            "请把工具放在项目文件夹里（例如 tools\\）再打开。\n\n"
            f"工具当前查找的目录：\n{ROOT}",
        )
        root.destroy()
        return 1
    try:
        app = ProductAdmin()
        app.mainloop()
    except Exception as error:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("工具启动失败", str(error))
        root.destroy()
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

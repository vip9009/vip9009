#!/usr/bin/env python3
"""
泡泡哥雾化 · 本地商品管理工具

不依赖线上后台，直接编辑项目里的 JSON 和图片：
- 商品新增 / 修改 / 删除 / 排序
- 分类新增 / 修改 / 删除
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


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "src" / "data"
SECTIONS_DIR = DATA_DIR / "sections"
CATEGORIES_FILE = DATA_DIR / "site" / "categories.json"
IMAGES_DIR = ROOT / "public" / "images" / "products"
BACKUP_DIR = ROOT / "tools" / ".backups"
CATEGORY_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


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
    return sorted(sections.values(), key=lambda item: (item.get("sort", 999), item.get("id", "")))


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
            local_image = product.get("localImage", "")
            path = image_path(local_image)
            if not path or not path.exists():
                errors.append(f"{section_id}[{index}]: 图片不存在：{local_image}")

    for category_id, category in categories.items():
        section_id = category.get("section")
        if section_id and section_id not in sections:
            errors.append(f"分类 {category_id}: 关联分区 {section_id} 不存在")

    print(f"分区：{len(sections)}")
    print(f"商品：{product_count}")
    print(f"分类：{len(categories)}")
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
        self.geometry("1220x820")
        self.minsize(1040, 700)

        self.sections = load_sections()
        self.categories = load_json(CATEGORIES_FILE)

        self.row_map = {}
        self.label_to_category = {}
        self.current_section = None
        self.current_index = None
        self.pending_image = None
        self._preview_photo = None
        self.category_mode = "edit"

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

    def _build_status(self):
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", padding=(10, 5)).pack(fill="x")

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(10, 0))
        self._build_products_tab()
        self._build_categories_tab()

    # -- 商品页 -----------------------------------------------------------

    def _build_products_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="商品管理")

        toolbar = ttk.Frame(tab)
        toolbar.pack(fill="x", pady=(0, 10))
        ttk.Label(toolbar, text="分类筛选").pack(side="left")
        self.filter_var = tk.StringVar(value="全部分类")
        self.filter_combo = ttk.Combobox(toolbar, textvariable=self.filter_var, state="readonly", width=20)
        self.filter_combo.pack(side="left", padx=(6, 18))
        self.filter_combo.bind("<<ComboboxSelected>>", lambda _event: self.refresh_product_tree())

        ttk.Label(toolbar, text="搜索").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_args: self.refresh_product_tree())
        ttk.Entry(toolbar, textvariable=self.search_var, width=28).pack(side="left", padx=6)

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
        self.product_tree.heading("category", text="分类")
        self.product_tree.column("title", width=360, anchor="w")
        self.product_tree.column("price", width=90, anchor="center")
        self.product_tree.column("category", width=140, anchor="center")
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

        ttk.Label(right, text="分类").grid(row=1, column=0, sticky="w", pady=4)
        self.product_category_var = tk.StringVar()
        self.product_category_combo = ttk.Combobox(
            right, textvariable=self.product_category_var, state="readonly"
        )
        self.product_category_combo.grid(row=1, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(right, text="价格").grid(row=2, column=0, sticky="w", pady=4)
        self.price_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.price_var, width=18).grid(row=2, column=1, sticky="w", pady=4)
        ttk.Label(right, text="元").grid(row=2, column=2, sticky="w")

        ttk.Label(right, text="图片").grid(row=3, column=0, sticky="w", pady=4)
        self.image_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.image_var, state="readonly").grid(
            row=3, column=1, sticky="ew", pady=4
        )
        ttk.Button(right, text="选择图片", command=self.choose_image).grid(
            row=3, column=2, sticky="w", padx=(6, 0)
        )

        self.preview_label = tk.Label(
            right,
            text="未选择图片",
            bg="#F7FFFB",
            fg="#9AA0A6",
            width=24,
            height=10,
            relief="solid",
            borderwidth=1,
        )
        self.preview_label.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

        ttk.Label(right, text="商品描述").grid(row=5, column=0, sticky="nw", pady=4)
        self.description_text = tk.Text(
            right,
            height=9,
            wrap="word",
            relief="solid",
            borderwidth=1,
            font=("Microsoft YaHei UI", 10),
        )
        self.description_text.grid(row=5, column=1, columnspan=2, sticky="nsew", pady=4)
        right.rowconfigure(5, weight=1)

        buttons = ttk.Frame(right)
        buttons.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(12, 0))
        ttk.Button(buttons, text="保存商品", style="Accent.TButton", command=self.save_product).pack(
            side="left"
        )
        ttk.Button(buttons, text="清空表单", command=self.new_product).pack(side="left", padx=8)

    # -- 分类页 -----------------------------------------------------------

    def _build_categories_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="分类管理")

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
            columns=("id", "title", "section", "count"),
            show="headings",
            selectmode="browse",
        )
        self.category_tree.heading("id", text="分类 ID")
        self.category_tree.heading("title", text="名称")
        self.category_tree.heading("section", text="关联分区")
        self.category_tree.heading("count", text="商品数")
        self.category_tree.column("id", width=130, anchor="w")
        self.category_tree.column("title", width=170, anchor="w")
        self.category_tree.column("section", width=130, anchor="center")
        self.category_tree.column("count", width=80, anchor="center")
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=scroll.set)
        self.category_tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        self.category_tree.bind("<<TreeviewSelect>>", self.load_category)

        actions = ttk.Frame(left)
        actions.pack(fill="x", pady=(10, 0))
        ttk.Button(actions, text="新增分类", style="Accent.TButton", command=self.new_category).pack(
            side="left"
        )
        ttk.Button(actions, text="删除分类", command=self.delete_category).pack(side="left", padx=8)

        right.columnconfigure(1, weight=1)

        ttk.Label(right, text="分类 ID").grid(row=0, column=0, sticky="w", pady=4)
        self.category_id_var = tk.StringVar()
        self.category_id_entry = ttk.Entry(right, textvariable=self.category_id_var)
        self.category_id_entry.grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Label(right, text="英文小写，例如 new-pods", foreground="#777").grid(
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
            height=6,
            wrap="word",
            relief="solid",
            borderwidth=1,
            font=("Microsoft YaHei UI", 10),
        )
        self.category_desc_text.grid(row=3, column=1, sticky="nsew", pady=4)
        right.rowconfigure(3, weight=1)

        ttk.Label(right, text="关联商品分区").grid(row=4, column=0, sticky="w", pady=4)
        self.category_section_var = tk.StringVar()
        self.category_section_combo = ttk.Combobox(
            right, textvariable=self.category_section_var, state="readonly"
        )
        self.category_section_combo.grid(row=4, column=1, sticky="ew", pady=4)

        buttons = ttk.Frame(right)
        buttons.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        ttk.Button(buttons, text="保存分类", style="Accent.TButton", command=self.save_category).pack(
            side="left"
        )
        ttk.Button(buttons, text="清空表单", command=self.new_category).pack(side="left", padx=8)

    # -- 数据刷新 ---------------------------------------------------------

    def _category_labels(self):
        labels = []
        self.label_to_category = {}
        for category_id, category in self.categories.items():
            section_id = category.get("section")
            if not section_id or section_id not in self.sections:
                continue
            label = str(category.get("title") or category_id)
            if label in self.label_to_category:
                label = f"{label}（{category_id}）"
            labels.append(label)
            self.label_to_category[label] = category_id
        return labels

    def _category_for_section(self, section_id):
        for category_id, category in self.categories.items():
            if category.get("section") == section_id:
                return category_id, category.get("title", section_id)
        return None, self.sections.get(section_id, {}).get("title", section_id)

    def _filter_section_id(self):
        category_id = self.label_to_category.get(self.filter_var.get())
        if not category_id:
            return None
        return self.categories.get(category_id, {}).get("section")

    def _refresh_all(self):
        self._refresh_category_options()
        self._refresh_product_category_combo()
        self._refresh_product_tree()
        self._refresh_category_tree()

    def _refresh_category_options(self):
        values = ["全部分类"] + self._category_labels()
        current = self.filter_var.get()
        self.filter_combo["values"] = values
        if current not in values:
            self.filter_var.set("全部分类")

    def _refresh_product_category_combo(self):
        values = self._category_labels()
        current = self.product_category_var.get()
        self.product_category_combo["values"] = values
        if current not in values:
            self.product_category_var.set(values[0] if values else "")

    def _refresh_product_tree(self):
        selected = self.product_tree.selection()
        selected_id = selected[0] if selected else None
        self.product_tree.delete(*self.product_tree.get_children())
        self.row_map = {}
        filter_section = self._filter_section_id()
        search = self.search_var.get().strip().lower()

        for section in sorted_sections(self.sections):
            section_id = section.get("id")
            if filter_section and section_id != filter_section:
                continue
            category_id, category_title = self._category_for_section(section_id)
            for index, product in enumerate(section.get("products", [])):
                title = str(product.get("title", ""))
                if search and search not in title.lower():
                    continue
                iid = f"{section_id}:{index}"
                self.product_tree.insert(
                    "",
                    "end",
                    iid=iid,
                    values=(title, f"￥{product.get('price', '')}", category_title),
                )
                self.row_map[iid] = (section_id, index)

        if selected_id and selected_id in self.row_map:
            self.product_tree.selection_set(selected_id)
            self.product_tree.see(selected_id)

    def _refresh_category_tree(self):
        selected = self.category_tree.selection()
        selected_id = selected[0] if selected else None
        self.category_tree.delete(*self.category_tree.get_children())
        for category_id, category in self.categories.items():
            section_id = category.get("section") or "（无）"
            count = 0
            if section_id in self.sections:
                count = len(self.sections[section_id].get("products", []))
            self.category_tree.insert(
                "",
                "end",
                iid=category_id,
                values=(category_id, category.get("title", ""), section_id, count),
            )
        if selected_id and selected_id in self.category_tree.get_children():
            self.category_tree.selection_set(selected_id)
            self.category_tree.see(selected_id)

    # -- 商品操作 ---------------------------------------------------------

    def _clear_preview(self):
        self._preview_photo = None
        self.preview_label.configure(image="", text="未选择图片")

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
                image.thumbnail((220, 220), resampling.LANCZOS)
                self._preview_photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=self._preview_photo, text="")
        except Exception as error:
            self.preview_label.configure(image="", text=f"预览失败：{error}")

    def new_product(self):
        self.current_section = None
        self.current_index = None
        self.pending_image = None
        self.title_var.set("")
        self.price_var.set("")
        self.image_var.set("")
        self.description_text.delete("1.0", "end")
        values = self._category_labels()
        if not values:
            self.product_category_var.set("")
            messagebox.showwarning("没有可用分类", "请先在分类管理中创建带商品分区的分类。")
        else:
            current = self.filter_var.get()
            self.product_category_var.set(current if current in values else values[0])
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

        self.title_var.set(product.get("title", ""))
        self.price_var.set(str(product.get("price", "")))
        self.image_var.set(product.get("localImage", ""))
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", product.get("description", ""))

        category_id, category_title = self._category_for_section(section_id)
        label = None
        for candidate, candidate_id in self.label_to_category.items():
            if candidate_id == category_id:
                label = candidate
                break
        self.product_category_var.set(label or category_title)

        self._show_preview(product.get("localImage", ""))
        self.status_var.set(f"正在编辑：{product.get('title', '')}")

    def choose_image(self):
        path = filedialog.askopenfilename(
            title="选择商品图片",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.webp *.bmp"),
                ("所有文件", "*.*"),
            ],
        )
        if not path:
            return
        self.pending_image = path
        self.image_var.set(path)
        self._show_preview(path)
        self.status_var.set("已选择新图片，保存时会自动压缩为 800px WebP")

    def save_product(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("缺少名称", "请填写商品名称。")
            return
        try:
            price = compact_price(self.price_var.get().strip())
            if float(price) <= 0:
                raise ValueError
        except (TypeError, ValueError):
            messagebox.showwarning("价格不正确", "请填写大于 0 的商品价格。")
            return

        category_id = self.label_to_category.get(self.product_category_var.get())
        if not category_id:
            messagebox.showwarning("缺少分类", "请选择一个已关联商品分区的分类。")
            return
        section_id = self.categories.get(category_id, {}).get("section")
        if not section_id or section_id not in self.sections:
            messagebox.showwarning("分类未关联分区", "该分类没有可用商品分区，请先在分类管理中处理。")
            return

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
                return
        if not local_image:
            messagebox.showwarning("缺少图片", "请选择一张商品图片。")
            return

        product = dict(existing) if existing else {}
        product.update(
            {
                "title": title,
                "price": price,
                "imageAlt": title,
                "localImage": local_image,
            }
        )
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

    def new_category(self):
        self.category_mode = "new"
        self.category_tree.selection_remove(self.category_tree.selection())
        self.category_id_var.set("")
        self.category_name_var.set("")
        self.category_desc_text.delete("1.0", "end")
        self.category_id_entry.configure(state="normal")
        self.category_section_combo.configure(values=["（自动创建同名分区）"], state="disabled")
        self.category_section_var.set("（自动创建同名分区）")
        self.status_var.set("新建分类：ID 会自动创建同名商品分区")

    def load_category(self, _event=None):
        selection = self.category_tree.selection()
        if not selection:
            return
        category_id = selection[0]
        category = self.categories.get(category_id)
        if not category:
            return
        self.category_mode = "edit"
        self.category_id_var.set(category_id)
        self.category_id_entry.configure(state="disabled")
        self.category_name_var.set(category.get("title", ""))
        self.category_desc_text.delete("1.0", "end")
        self.category_desc_text.insert("1.0", category.get("desc", ""))
        values = [section.get("id") for section in sorted_sections(self.sections)] + ["（无）"]
        self.category_section_combo.configure(values=values, state="readonly")
        self.category_section_var.set(category.get("section") or "（无）")
        self.status_var.set(f"正在编辑分类：{category.get('title', '')}")

    def save_category(self):
        category_id = self.category_id_var.get().strip()
        name = self.category_name_var.get().strip()
        desc = self.category_desc_text.get("1.0", "end").strip()
        if not name:
            messagebox.showwarning("缺少名称", "请填写分类名称。")
            return

        if self.category_mode == "new":
            if not CATEGORY_ID_RE.match(category_id):
                messagebox.showwarning("ID 不正确", "分类 ID 只能使用小写字母、数字和短横线，例如 new-pods。")
                return
            if category_id in self.categories:
                messagebox.showwarning("ID 重复", "该分类 ID 已存在。")
                return
            if category_id in self.sections:
                messagebox.showwarning("分区重复", "该商品分区已存在，请换一个 ID。")
                return
            max_sort = max((section.get("sort", 0) for section in self.sections.values()), default=0)
            self.sections[category_id] = {
                "id": category_id,
                "title": name,
                "sort": max_sort + 1,
                "products": [],
            }
            self.categories[category_id] = {
                "title": name,
                "desc": desc,
                "section": category_id,
            }
            self.category_mode = "edit"
            self.category_id_entry.configure(state="disabled")
            section_values = [section.get("id") for section in sorted_sections(self.sections)] + ["（无）"]
            self.category_section_combo.configure(values=section_values, state="readonly")
            self.category_section_var.set(category_id)
        else:
            category = self.categories.get(category_id)
            if not category:
                return
            section_id = self.category_section_var.get()
            section_id = None if section_id in ("", "（无）") else section_id
            if section_id and section_id not in self.sections:
                messagebox.showwarning("分区不存在", "请选择一个存在的商品分区。")
                return
            category["title"] = name
            category["desc"] = desc
            category["section"] = section_id
            if section_id:
                self.sections[section_id]["title"] = name

        self.save_all()
        self._refresh_all()
        if category_id in self.category_tree.get_children():
            self.category_tree.selection_set(category_id)
            self.category_tree.see(category_id)
        self._refresh_product_category_combo()
        self.status_var.set(f"已保存分类：{name}")

    def delete_category(self):
        selection = self.category_tree.selection()
        if not selection:
            return
        category_id = selection[0]
        if category_id == "hot":
            messagebox.showwarning("不能删除", "“热门产品”是首页核心分类，不能删除。")
            return
        category = self.categories.get(category_id)
        if not category:
            return
        section_id = category.get("section")
        products = self.sections.get(section_id, {}).get("products", []) if section_id else []
        if products:
            messagebox.showwarning(
                "分类下还有商品",
                f"该分类还有 {len(products)} 个商品，请先删除或移动商品。",
            )
            return
        if not messagebox.askyesno("删除分类", f"确定删除分类“{category.get('title', '')}”吗？"):
            return
        self.categories.pop(category_id)
        still_used = any(item.get("section") == section_id for item in self.categories.values())
        if section_id and not still_used and section_id in self.sections:
            self.sections.pop(section_id)
            path = SECTIONS_DIR / f"{section_id}.json"
            if path.exists():
                path.unlink()
        self.save_all()
        self.new_category()
        self._refresh_all()
        self.status_var.set("分类已删除")

    # -- 保存 / 发布 ------------------------------------------------------

    def save_all(self):
        for section_id, section in list(self.sections.items()):
            write_json(SECTIONS_DIR / f"{section_id}.json", section)
        write_json(CATEGORIES_FILE, self.categories)

    def publish(self):
        self.save_all()
        if not (ROOT / ".git").exists():
            messagebox.showerror("不是 Git 仓库", "当前项目目录不是 Git 仓库，无法发布。")
            return
        if not messagebox.askyesno(
            "发布到 GitHub",
            "将提交 src/data 和 public/images/products 的改动，并推送到 GitHub。\n\n"
            "GitHub Actions 会自动重新构建和部署。继续吗？",
        ):
            return

        self.status_var.set("正在提交并推送...")
        self.update_idletasks()

        add = self._run_git(["add", "src/data", "public/images/products"])
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

    @staticmethod
    def _command_output(result):
        return ((result.stdout or "") + (result.stderr or "")).strip()[-4000:]

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

# 泡泡哥雾化 · Vue 静态站点

使用 **UI UX Pro Max** 生成的 E-commerce 设计系统重设计的响应式电子烟信息展示站，基于 **Vue 3 + Vite** 构建，纯静态、无后端，可直接托管到 **GitHub Pages**。

设计系统：**Feature-Rich Showcase + Vibrant & Block-based**，主色松石绿、CTA 橙色，字体 Rubik / Nunito Sans。

> 本站仅做商品信息展示，不包含下单、购物车、支付等交易功能。页面中的商品、价格、图片和文案为演示数据，正式使用前请替换为你自己的品牌素材与内容。

## 技术栈

- Vue 3（`<script setup>`）
- Vue Router 4（Hash 路由，GitHub Pages 无需 404 重写）
- Vite 4
- 原生 CSS（Grid + Flex，响应式）
- 数据源：本地 JSON，无需接口
- UI/UX 设计系统：UI UX Pro Max（`design-system/laovape/MASTER.md`）

## 页面与设计

- 顶部深绿工具栏：网站地图、产品搜索
- 主导航：品牌文字 Logo、7 个栏目、多级下拉、橙色「立即咨询」CTA
- 新 Hero：大字号标题、信任徽章、CTA、产品拼贴卡、浮动保障标签
- 「按分类找产品」分类入口：一次性、烟弹、烟杆、烟油、积木、国标系列
- 热门产品、一次性电子烟、积木电子烟、烟弹 4 个商品区
- 新商品卡：绿色边框、仅展示产品名称与参考价、查看详情
- 深绿 5 栏页脚：品牌介绍、客服 CTA、下单方式、4 组链接
- 右侧悬浮客服：微信二维码、QQ 号展示（不跳转），移动端默认收起
- 桌面、平板、手机三档响应式；手机端双列商品卡、抽屉菜单、触控热区优化
- 附加页面：分类列表、商品详情、搜索、联系我们、帮助页、网站地图、404

## 目录结构

```
vip9009/
├─ .github/workflows/deploy.yml   # GitHub Pages 自动部署
├─ .opencode/skills/              # UI UX Pro Max 等开发期 skill（不参与打包）
├─ design-system/laovape/         # 设计系统 MASTER.md
├─ public/
│  ├─ images/                     # 二维码、商品图（WebP）
│  └─ .nojekyll
├─ src/
│  ├─ assets/styles/main.css      # 全局基础样式与响应式
│  ├─ components/                 # 页头、页脚、商品卡、客服悬浮窗
│  ├─ data/
│  │  ├─ index.js                 # 自动聚合 sections/*.json
│  │  ├─ sections/                # 每个分类一个分区 JSON，可自由新增
│  │  │  ├─ hot.json              # 热门产品
│  │  │  ├─ disposables.json      # 一次性电子烟
│  │  │  ├─ jimu.json             # 积木电子烟
│  │  │  └─ pods.json             # 烟弹
│  │  └─ site/
│  │     ├─ general.json          # 品牌、Banner、导航
│  │     ├─ categories.json       # 一级/二级分类与导航配置
│  │     ├─ footer.json           # 页脚栏目
│  │     ├─ contacts.json         # 微信二维码 / QQ 号
│  │     └─ info-pages.json       # 帮助页文案
│  ├─ router/
│  │  ├─ index.js                 # Hash 路由
│  │  └─ lazyViews.js             # 路由分包与预加载
│  ├─ utils/                      # 资源路径、分类筛选、图片预取等
│  ├─ views/                      # 首页及各内页
│  ├─ App.vue                     # 页面骨架、切换进度条
│  └─ main.js
├─ index.html
├─ tools/                          # 本地商品管理工具（不参与打包）
│  ├─ product_admin.py             # Tkinter 管理界面
│  ├─ requirements.txt             # Pillow
│  └─ 启动商品管理工具.bat         # Windows 双击启动
├─ vite.config.js                 # base: './'，支持仓库子路径部署
└─ package.json
```

## 本地开发

要求 Node.js 16.19+（推荐 18/20）。

```bash
npm install
npm run dev
```

打开终端提示的地址（默认 `http://localhost:5173/`）。

生产构建与本地预览：

```bash
npm run build
npm run preview
```

## 本地商品管理工具（推荐）

不想手改 JSON 的话，用项目自带的本地工具即可完成日常维护，**不需要线上后台、不需要数据库、不需要服务器**。

双击运行：

```text
tools\启动商品管理工具.bat
```

或命令行运行：

```bash
python -m pip install -r tools/requirements.txt
python tools/product_admin.py
```

工具能做什么：

| 功能 | 说明 |
| --- | --- |
| 新增 / 修改商品 | 商品名称、参考价、一级分类、二级分类、商品描述 |
| 分类 / 导航 | 新增一级分类、二级分类，自动生成顶部导航和下拉菜单 |
| 商品归类 | 保存商品时可直接选到末级分类，例如「一次性电子烟 / 悦刻一次性电子烟」 |
| 移动商品 | 改商品的一级 / 二级分类后保存，前台立即归到新分类 |
| 选择图片 | 自动转成 800px WebP，写入 `public/images/products/` |
| 排序 | 商品上移 / 下移；分类用「排序」数字控制导航顺序 |
| 保存 | 直接写回 `src/data/` 下的 JSON，并自动备份旧文件 |
| 导出数据包 | 没有 Git 的电脑可用：导出 `src/data` + 商品图片的 zip，拷回主电脑发布 |
| 发布 | 一键提交 `src/data` + `public/images/products` 并 push，GitHub Actions 自动重新部署 |

注意事项：

- 一级分类的 ID 只能用小写字母、数字和短横线，例如 `new-pods`，它会同时作为该分类的商品分区文件名。
- 二级分类不需要单独的分区文件，商品统一放在上级分类的分区里，通过 `subcategory` 标记归属。
- 删除一级分类前，先删除它的二级分类；删除二级分类前，先把商品移到其它分类。
- 顶部导航由 `categories.json` 自动生成：一级分类是菜单，二级分类是下拉项，`排序` 越小越靠前，取消勾选「显示在顶部导航」可隐藏。
- 工具只提交 `src/data` 和 `public/images/products`，不会提交工具本身的改动。
- 旧 JSON 会备份到 `tools/.backups/`（已在 `.gitignore` 中忽略）。
- 检查数据是否完整：

```bash
python tools/product_admin.py --check
```

> 新增一级分类后，如果本地 `npm run dev` 还开着，需要重启一次开发服务器，Vite 才会加载新的分区 JSON。线上构建不受影响。

### 没有 Python 的电脑（独立 exe）

另一台 Windows 电脑没有 Python 也可以使用，直接双击打包好的独立程序：

```text
tools\dist\泡泡哥商品管理工具.exe
```

它内置了 Python、Tkinter 和 Pillow，不需要安装任何环境。

注意：

- exe 必须放在项目文件夹里（例如 `tools\dist\`），因为它要读写项目的 `src\data` 和 `public\images\products`。
- 换电脑时把**整个项目文件夹**拷过去（包含 exe），不要只拷 exe。
- exe 约 25MB，不提交到 Git。工具代码更新后需要重新打包：

```bash
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "泡泡哥商品管理工具" --icon "tools\app.ico" --distpath "tools\dist" --workpath "tools\build" --specpath "tools" "tools\product_admin.py"
```

### 没有 Git / GitHub 的电脑

没有 Git 也能正常新增、修改、保存商品和分类，数据会写到本地 JSON，只是不能直接发布：

- 点「发布到 GitHub」时，工具会提示没有 Git，并建议改用「导出数据包」。
- 点「导出数据包」会生成一个 zip，里面是 `src/data` 和 `public/images/products`。
- 把 zip 拷到有 Git 的主电脑，解压并覆盖到项目根目录，再打开工具点「发布到 GitHub」。
- 也可以把项目放在 OneDrive / 网盘同步目录，在另一台电脑改完，回主电脑发布。

## 修改数据

数据已按业务拆分为多个 JSON 文件，修改时只需要动对应文件，不需要改组件代码。

### 商品分区

文件：`src/data/sections/*.json`

```json
{
  "id": "disposables",
  "title": "一次性电子烟",
  "sort": 2,
  "products": [
    {
      "title": "商品名称",
      "price": 288,
      "imageAlt": "图片描述",
      "localImage": "/images/products/disposables-1-800.webp",
      "subcategory": "relx-disposable",
      "description": "可选：商品详情里的介绍文案，支持换行"
    }
  ]
}
```

- `src/data/index.js` 用 `import.meta.glob('./sections/*.json')` 自动加载全部分区，按 `sort` 升序排列；新增或删除分区文件不需要改代码。
- 现有分区：`hot`（1）、`disposables`（2）、`jimu`（3）、`pods`（4）、`pod-system`（5）、`e-liquid`（6）、`gbxl`（7）。后三个目前是空分区，用于以后上架烟杆、烟油和国标商品。
- `localImage` 填 `public` 下的相对路径，建议使用 800px 宽的 WebP。
- `subcategory` 是二级分类 ID，对应 `categories.json` 里的子分类；留空表示只归到一级分类。
- `description` 可选，留空时商品详情使用默认介绍文案：
  「加泡泡哥微信或 QQ 获取实时价格、口味与物流方案。泡泡哥只做正品，支持扫码验证，不同国家与地区的配送方式由泡泡哥一对一确认。」
- 商品详情路由为 `/product/:sectionId/:index`，`index` 是商品在分区中的下标（从 0 开始）。
- 商品卡只展示产品名称与参考价，不再展示库存、人气、折扣和划线原价。
- HOT / NEW 角标是部分商品图片本身自带的效果，无需额外字段。

### 分类与导航

文件：`src/data/site/categories.json`

导航不再手写在 `general.json` 里，而是从分类结构自动生成：一级分类 = 顶部菜单，二级分类 = 下拉项。

```json
{
  "disposables": {
    "title": "一次性电子烟",
    "desc": "分类页描述",
    "section": "disposables",
    "sort": 1,
    "nav": true,
    "children": ["relx-disposable", "snowplus-disposable"]
  },
  "relx-disposable": {
    "title": "悦刻一次性电子烟",
    "desc": "二级分类描述",
    "parent": "disposables",
    "sort": 1
  },
  "contact": {
    "title": "联系客服",
    "to": "/contact",
    "nav": true,
    "sort": 99
  }
}
```

- 一级分类用 `section` 指向商品分区；二级分类用 `parent` 指向一级分类，商品通过 `subcategory` 归到二级。
- `sort` 控制顺序，`nav: false` 表示不在顶部导航显示（例如「热门产品」）。
- `to` 用于非商品菜单，例如「联系客服」指向 `/contact`。
- 二级分类页地址为 `/category/:一级ID?sub=:二级ID`，例如 `/category/disposables?sub=relx-disposable`。
- 一级分类页显示该分类下全部商品，并带二级分类筛选条；二级分类页只显示对应商品。

### 导航、页脚、联系方式

这些配置在 `src/data/site/` 下：

| 文件 | 内容 |
| --- | --- |
| `general.json` | 品牌信息、顶部链接（主导航由 `categories.json` 自动生成） |
| `categories.json` | 一级 / 二级分类、导航顺序、商品分区映射 |
| `footer.json` | 页脚四组链接（含下单方式） |
| `contacts.json` | 微信二维码、QQ 号 |
| `info-pages.json` | 付款方式、配送说明、退换政策等帮助页文案 |

`src/data/index.js` 会把上述文件聚合成组件使用的 `site` 与 `productsData`，商品分区统一从 `sections` 导出。

### 配置 QQ

编辑 `src/data/site/contacts.json`，填入 QQ 号即可自动出现在联系页、页脚和悬浮客服中：

```json
{
  "qq": {
    "label": "泡泡哥 QQ",
    "number": "1220820788"
  }
}
```

- QQ 号只做展示，点击不会跳转，方便用户直接查看和复制。
- 留空时，QQ 入口会自动隐藏，不影响微信咨询。
- 当前只保留微信与 QQ 两种下单咨询方式。

### 客服图片

| 文件 | 用途 |
| --- | --- |
| `public/images/paopao-face.jpg` | 泡泡哥头像，用于微信卡片和悬浮客服 |
| `public/images/paopao-avatar-600.jpg` | 泡泡哥主理人展示图，用于首页和联系页 |
| `public/images/paopao-qr.png` | 泡泡哥微信二维码 |
| `public/favicon.png` | 网站 favicon（泡泡云头像） |

### 图片怎么放

用工具时**不需要提前把图片放进项目**：

1. 在商品页点「选择图片」，从电脑任意文件夹选图（桌面、下载、U 盘都可以）。
2. 点「保存商品」，工具会自动压缩成 800px WebP，并复制到 `public/images/products/`。
3. 文件名自动生成，例如 `disposables-20261126143000123456.webp`，不需要手动改名。

原图建议单独放在一个文件夹，例如 `桌面\泡泡哥商品原图\`，不要一起提交到 Git，避免仓库变大。

手动替换时：

1. 将图片压缩为 800px 宽左右的 WebP，放入 `public/images/products/`；
2. 更新对应 JSON 的 `localImage`；
3. 建议保留 `-800.webp` 命名习惯，方便区分未压缩原图。

## 性能优化说明

- **数据拆分**：商品按分区、站点配置按用途拆分，方便维护；构建期静态引入，不产生额外接口请求。
- **路由预加载**：首页空闲时自动预取各内页 JS；鼠标悬停/键盘聚焦链接时再次按需预取。
- **图片预取**：悬停分类或商品卡时，提前加载首屏商品图。
- **切换进度条**：路由切换超过 120ms 才显示顶部进度条，避免闪烁；配合预加载，正常切换基本无感。
- **图片压缩**：商品图转为 800px WebP，首页完整滚动加载从约 6.6MB 降至约 0.84MB。
- **懒加载与占位**：首屏 4 个商品优先加载，其余图片懒加载；图片区域带微光占位，避免白屏跳动。

## 无障碍与交互

在不改变原站排版的前提下，补充了以下可用性细节：

- **键盘导航**：全站可见的 `:focus-visible` 焦点环；下拉菜单支持键盘聚焦展开；移动端菜单支持 Esc 关闭与焦点循环。
- **跳转链接**：Tab 第一项为「跳到主要内容」，回车后聚焦主内容区。
- **移动菜单语义**：抽屉使用 `role="dialog"` + `aria-modal="true"`，打开后焦点进入关闭按钮，关闭后回到菜单按钮。
- **触控热区**：移动端菜单、搜索、关闭等小图标按钮通过伪元素扩大点击区域，不改变视觉尺寸。
- **减少动画**：尊重 `prefers-reduced-motion`，关闭过渡、微光占位与进度条动画。
- **高对比度**：尊重 `prefers-contrast: more`，自动加深次要文字和页脚文字。
- **图片语义**：商品卡图片作为装饰（`alt=""`），链接名称由标题提供，避免读屏重复朗读。
- **加载状态**：进度条配合 `aria-busy` 与 `role="status"`，让辅助技术感知页面切换。

## UI/UX 设计检查（可选开发工具）

项目已安装 UI UX Pro Max 到 `.opencode/skills/`，用于后续 UI/UX 审查和实现建议。它只参与开发，不会打包进 `dist`。

```bash
# 重新安装 / 更新
npx ui-ux-pro-max-cli init --ai opencode

# 针对某个问题做检索
python .opencode/skills/ui-ux-pro-max/scripts/search.py "keyboard focus visible" --domain ux
python .opencode/skills/ui-ux-pro-max/scripts/search.py "image loading layout shift" --domain ux
python .opencode/skills/ui-ux-pro-max/scripts/search.py "mobile menu touch target" --domain ux
```

> 当前项目采用 UI UX Pro Max 生成的 E-commerce 设计系统，只把该 skill 用于 UX、无障碍、响应式与性能建议，不再追求原站 1:1 还原。

## 设计系统

完整规则见 [`design-system/laovape/MASTER.md`](design-system/laovape/MASTER.md)。

| 角色 | 值 |
| --- | --- |
| 主色 | `#059669` |
| 辅助色 | `#10B981` |
| CTA | `#EA580C` |
| 背景 | `#ECFDF5` |
| 前景 | `#064E3B` |
| 卡片 | `#FFFFFF` |
| 弱化背景 | `#E8F1F3` |
| 弱化文字 | `#475569` |
| 边框 | `#A7F3D0` |
| 标题字体 | Rubik |
| 正文字体 | Nunito Sans |

所有颜色、圆角、阴影、字体均已收敛到 `src/assets/styles/main.css` 的 CSS 变量中。

## 部署到 GitHub Pages

1. 新建 GitHub 仓库，将本项目推送到 `main` 分支。
2. 打开仓库 **Settings → Pages**。
3. 在 **Build and deployment → Source** 选择 **GitHub Actions**。
4. 推送代码后，`.github/workflows/deploy.yml` 会自动安装依赖、构建并发布。
5. 在 **Actions** 或 **Settings → Pages** 中查看站点地址，形如：
   `https://<用户名>.github.io/<仓库名>/`

项目已设置 `base: './'` 并使用 Hash 路由，因此：

- 部署在 `用户名.github.io/仓库名/` 子路径下无需修改配置；
- 刷新内页不会 404；
- 不需要额外的 `404.html` 或服务器重写规则。

## 常用路由

| 路由 | 页面 |
| --- | --- |
| `/` | 首页 |
| `/category/:id` | 商品分类（`hot`、`disposables`、`jimu`、`pods` 等） |
| `/category/:id?sub=:subId` | 二级分类（例如 `/category/disposables?sub=relx-disposable`） |
| `/product/:section/:index` | 商品详情 |
| `/search?q=关键词` | 产品搜索 |
| `/contact` | 联系我们 |
| `/info/:slug` | 帮助页 |
| `/sitemap` | 网站地图 |

## 说明

- 所有数据均在浏览器端从 JSON 读取，无任何接口请求。
- 页面为纯静态资源，可直接部署到 GitHub Pages、Netlify、Vercel 或任意静态服务器。
- 若用于正式商业项目，请替换原站图片、Logo、文案与联系方式，并确认符合当地关于电子烟展示与销售的法律法规。

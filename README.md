# 泡泡哥雾化 · Vue 静态站点

基于 **Vue 3 + Vite** 构建的响应式电子雾化商城，纯静态、无后端，可直接托管到 **GitHub Pages**。整体版式参考 vapepu.com 的黑白 + 粉色极简风格，品牌、商品和图片使用泡泡哥自己的内容。

设计系统：**黑白极简 + 粉色强调**，字体 Lato，细边框、无圆角卡片、三列商品网格。

> 本站包含本地购物车和结算页，但**不接入任何支付接口**；下单后复制订单信息，加客服微信 / QQ 由客服人工确认商品、运费和付款方式。页面商品、价格、图片为演示数据，正式使用前请替换为真实内容。
>
> 当前商品数据、商品图片、分类图标与 Lottie 动画均为本地素材，不引用参考站原图或 `wp-content` 链接。

> 完整操作、打包、部署说明见 [`tools/使用手册.md`](tools/使用手册.md)。

## 技术栈

- Vue 3（`<script setup>`）
- Vue Router 4（Hash 路由，GitHub Pages 无需 404 重写）
- Vite 4
- 原生 CSS（Grid + Flex，响应式）
- 数据源：本地 JSON，无需接口
- 购物车：浏览器 localStorage；不生成订单记录，结算页生成可复制文本
- 字体：Lato（`@fontsource/lato`，本地打包）

## 页面与设计

- 黑色公告条：滚动公告与下单提示
- 居中 Logo 头部：左侧导航 + 搜索、右侧购物车，移动端抽屉菜单
- 首页：黑粉大 Banner、7 个手绘分类入口、NEW 分页商品、TAG / BRAND 切换、NO SMOKING 分割、品牌墙
- 分类页：左侧分类栏 + 三列商品网格 + 排序 / 分页，移动端筛选折叠
- 商品页：大图、品牌 / 标签订、价格区间、口味规格、数量、加入购物车、详情 Tabs
- 购物车、结算页（收货信息 + 一键复制订单信息 + 微信 / QQ 联系方式）
- 18+ 年龄验证弹层
- 右下角粉色客服按钮：在线客服（微信二维码 + QQ 复制）
- 桌面 / 手机响应式：桌面三列商品，手机两列
- 附加页面：搜索、联系泡泡哥、帮助页、网站地图、404

## 目录结构

```
vip9009/
├─ .github/workflows/deploy.yml   # GitHub Pages 自动部署
├─ .opencode/skills/              # UI UX Pro Max 等开发期 skill（不参与打包）
├─ design-system/laovape/         # 设计系统 MASTER.md
├─ public/
│  ├─ images/                     # 二维码、商品图、详情图（WebP）
│  ├─ videos/products/            # 商品详情视频（MP4 / WebM）
│  ├─ animations/                 # FAQ / 火箭 / NO SMOKING Lottie（占位）
│  └─ .nojekyll
├─ src/
│  ├─ assets/styles/main.css      # 全局基础样式与响应式
│  ├─ components/                 # 页头、页脚、商品卡、客服悬浮窗
│  ├─ data/
│  │  ├─ index.js                 # 自动聚合 sections/*.json
│  │  ├─ sections/                # 每个分类一个分区 JSON，可自由新增
│  │  │  ├─ disposables.json      # 一次性系列
│  │  │  ├─ pods.json             # 换弹系列
│  │  │  ├─ jimu.json             # 积木系列
│  │  │  ├─ gbxl.json             # 国标系列
│  │  │  ├─ shisha.json           # 水烟系列
│  │  │  ├─ wanghong.json         # 网红系列
│  │  │  └─ combo.json            # 组合专区
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
│  ├─ app.ico                      # exe 图标
│  ├─ build_exe.bat                # 一键打包免 Python 的 exe
│  ├─ make_package.py              # 一键打包“发给别人”的 zip
│  ├─ 启动商品管理工具.bat         # Windows 双击启动（需要 Python）
│  └─ 使用手册.md                  # 完整操作、打包、部署手册
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
| 商品更多信息 | 品牌、角标、价格区间、库存、HOT、店长推荐、口味/规格、参数 |
| 图文/视频详情 | 文字、小标题、多张详情图片、视频，按顺序显示在商品详情页 |
| 站点设置 | 公告、首页 Banner 链接、包邮门槛/运费、客服微信名称/头像/二维码、QQ |
| 排序 | 商品上移 / 下移；分类用「排序」数字控制导航顺序 |
| 保存 | 直接写回 `src/data/` 下的 JSON，并自动备份旧文件 |
| 导出数据包 | 没有 Git 的电脑可用：导出 `src/data`、商品图片和客服二维码的 zip，拷回主电脑发布；不包含参考站外链 |
| 初始化数据 | 清空全部商品和商品图片，保留分类；清空前自动备份 |
| 发布 | 一键提交 `src/data`、商品图片和工具上传的二维码图片并 push，GitHub Actions 自动重新部署 |

注意事项：

- 一级分类的 ID 只能用小写字母、数字和短横线，例如 `new-pods`，它会同时作为该分类的商品分区文件名。
- 二级分类不需要单独的分区文件，商品统一放在上级分类的分区里，通过 `subcategory` 标记归属。
- 删除一级分类前，先删除它的二级分类；删除二级分类前，先把商品移到其它分类。
- 顶部导航由 `categories.json` 自动生成：一级分类是菜单，二级分类是下拉项，`排序` 越小越靠前，取消勾选「显示在顶部导航」可隐藏。
- 工具只提交 `src/data`、`public/images/products` 和工具里上传的二维码图片，不会提交工具本身的改动。
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
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "泡泡哥商品管理工具" --icon "tools\app.ico" --distpath "tools\dist" --workpath "tools\build" --specpath "." "tools\product_admin.py"
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
      "priceMax": 318,
      "brand": "ZGAR",
      "badges": ["HOT", "上新"],
      "stock": true,
      "hot": true,
      "options": ["黑色", { "label": "蓝色", "price": 298, "stock": false }],
      "specs": { "口数": "30000", "电池": "800mAh" },
      "imageAlt": "图片描述",
      "localImage": "/images/products/disposables-1-800.webp",
      "subcategory": "relx-disposable",
      "description": "可选：商品详情里的介绍文案，支持换行",
      "detailBlocks": [
        { "type": "heading", "text": "产品细节" },
        { "type": "text", "text": "支持换行的文字段落" },
        { "type": "image", "src": "/images/details/detail-1.webp", "caption": "实拍图" },
        { "type": "video", "src": "/videos/products/video-1.mp4", "poster": "/images/details/detail-1.webp" }
      ]
    }
  ]
}
```

- `src/data/index.js` 用 `import.meta.glob('./sections/*.json')` 自动加载全部分区，按 `sort` 升序排列；新增或删除分区文件不需要改代码。
- 现有分区：`disposables`（1，一次性系列）、`gbxl`（2，国标系列）、`pods`（4，换弹系列）、`shisha`（5，水烟系列）、`jimu`（6，积木系列）、`combo`（7，组合专区）、`wanghong`（8，网红系列）、`recommend`（3，店长推荐）。
- `localImage` 填 `public` 下的相对路径，建议使用 800px 宽的 WebP。
- `subcategory` 是二级分类 ID，对应 `categories.json` 里的子分类；留空表示只归到一级分类。
- `description` 可选，留空时商品详情使用默认介绍文案：
  「加泡泡哥微信或 QQ 获取实时价格、口味与物流方案。泡泡哥只做正品，支持扫码验证，不同国家与地区的配送方式由泡泡哥一对一确认。」
- 商品详情路由为 `/product/:sectionId/:index`，`index` 是商品在分区中的下标（从 0 开始）。
- 可选字段：
  - `brand`：品牌，建议使用站点固定品牌名，确保前台 Logo 与品牌链接匹配；留空时自动从标题识别。工具下拉会同时列出固定品牌和现有商品已在用的品牌
  - `badges`：活动角标显示在图片右上角，例如 `["HOT", "上新"]`；非活动标签（如自定义、呼吸灯、凉度调节）会自动显示在图片左下角。工具中从常用标签列表选择
  - `priceMax`：价格区间上限，前台显示 `¥最低 – ¥最高`
  - `stock`：`false` 时显示“无货”并禁用购买
  - `hot`：`true` 时显示 HOT 标记
  - `recommend`：`true` 时自动显示“店长推荐”标签
  - `options`：口味/规格，字符串数组或 `{label, price, stock}` 数组；有值时商品卡显示 SELECT 下拉。选中后显示对应口味价格；该口味 `stock: false` 时购买按钮置灰
  - `specs`：参数对象，显示在商品页“参数”Tab
  - `gallery`：详情图数组，留空使用 `localImage`
  - `detailBlocks`：图文/视频详情块数组，按顺序显示在详情页「商品详情」Tab。类型支持 `text`、`heading`、`image`、`video`；有该字段时优先于 `description` 显示
- 工具里的「更多信息」和「图文/视频详情」可以编辑以上字段，不需要手改 JSON。

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
- `sort` 控制顺序，`nav: false` 表示不在顶部导航显示。
- `to` 用于非商品菜单，例如「联系客服」指向 `/contact`。
- 二级分类页地址为 `/category/:一级ID?sub=:二级ID`，例如 `/category/disposables?sub=relx-disposable`。
- 一级分类页显示该分类下全部商品，并带二级分类筛选条；二级分类页只显示对应商品。

### 导航、页脚、联系方式

这些配置在 `src/data/site/` 下：

| 文件 | 内容 |
| --- | --- |
| `general.json` | 品牌、公告、首页 Banner、包邮门槛 / 运费 |
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
| 主色 / CTA | `#E6007E` 粉色 |
| 深色 | `#242125` |
| 背景 | `#FFFFFF` |
| 弱化背景 | `#F5F5F5` |
| 弱化文字 | `#777777` |
| 边框 | `#E5E5E5` |
| 标题字体 | Lato 700 / 900 |
| 正文字体 | Lato 400 |

> 当前 UI 方向：**黑白 + 粉色**的极简商城风格，参考 vapepu.com 的版式：细边框、无圆角卡片、三列商品、居中 Logo、右下角客服按钮。
>
> 首页 FAQ 横幅、优惠活动小火箭、NO SMOKING 动画暂时使用参考站的 Lottie 素材作为占位（`public/animations/*.json`），正式上线前请替换为自己的动画素材。

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
| `/category/:id` | 商品分类（`disposables`、`jimu`、`pods` 等） |
| `/category/:id?sub=:subId` | 二级分类（例如 `/category/disposables?sub=relx-disposable`） |
| `/product/:section/:index` | 商品详情 |
| `/search?q=关键词` | 产品搜索 |
| `/contact` | 联系我们 |
| `/cart` | 购物车 |
| `/checkout` | 填写收货信息 / 复制订单 / 联系客服确认付款 |
| `/info/:slug` | 帮助页 |
| `/sitemap` | 网站地图 |

## 说明

- 所有数据均在浏览器端从 JSON 读取，无任何接口请求。
- 页面为纯静态资源，可直接部署到 GitHub Pages、Netlify、Vercel 或任意静态服务器。
- 若用于正式商业项目，请替换原站图片、Logo、文案与联系方式，并确认符合当地关于电子烟展示与销售的法律法规。

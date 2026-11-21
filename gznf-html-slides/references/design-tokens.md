# 广州南方学院模板 · 设计 Token 与组件清单

从已验收成品 HTML 提炼。新建页优先复用这些语义化 class 与变量，保持全篇一致。

## 目录
1. 色彩 / 字体 / 舞台尺寸
2. 全局骨架与翻页
3. 页型与组件 class 映射
4. 卡片/图表/流程族 class
5. 强调与虚线约定

---

## 1. 色彩 / 字体 / 舞台尺寸

CSS 变量（写在 `:root`）：

| 变量 | 值 | 用途 |
|---|---|---|
| `--red` | `#780000` | 主色：导航条、竖栏、方块页码、强调 |
| `--red-dark` | `#5a0000` | 深红悬停/深色块 |
| `--red-soft` | `#a33333` | 虚线、弱化红、箭头 |
| `--ink` | `#1F2328` | 正文/主标题墨色 |
| `--gray` | `#555555` | 说明文字 |
| `--muted` | `#8a8a8a` | 弱注、英文副题、占位 |
| `--bg` | `#fbfafa` | 浅暖底（强调条底色） |
| `--line` | `#e6d9d9` | 卡片浅红灰描边 |

派生底色：浅红卡底 `#fdf6f6`；舞台外屏背景 `#2b2020`（深褐，非幻灯片色）。

字体：
- 中文栈 `"Microsoft YaHei","PingFang SC","Source Han Sans SC","等线",sans-serif`（Linux 渲染回退 Noto Sans CJK / Droid Sans Fallback）。
- 英文、数字标签、PART/LINE/OUTPUT 编号用 `Georgia,"Times New Roman",serif`。
- 层级靠字号+字重+颜色，不新增字体。主色之外不随意引入新色，需要派生时沿同色相调明度。

舞台与安全区：
- 固定舞台 `.stage{width:1280px;height:720px}`，16:9；`overflow:hidden`。
- `body` flex 居中；JS `fit()` 用 `Math.min(innerWidth/1280,innerHeight/720)` 做 `transform:scale`，等比不留白不裁切。
- 内容页 `.body{height:calc(720px-72px);padding:34px 46px}`，**内容可用高度约 580px、宽度约 1188px**，任何模块总高不得超过 580。

## 2. 全局骨架与翻页

- 每张幻灯片一个 `<section class="slide" data-nav="...">`，封面额外 `.active`；目录用 `.slide.toc`，章节过渡用 `.slide.chapter`。
- 显隐铁规则（修复叠加重影的关键，勿删）：
  - `.slide{position:absolute;inset:0;display:none}` `.slide.active{display:block}`
  - `.slide.chapter{display:none}` `.slide.chapter.active{display:grid}`
  - `.toc .chapter{display:grid}`（目录内的 chapter 常驻显示）
- 翻页脚本暴露全局 `slides`（数组）、`show(i)`、`cur`；支持左右方向键与底部按钮；counter 文本由 `show()` 用 `slides.length` 覆盖，静态占位也要改成 `1 / 总页数`。
- 文件 UTF-8（可带 BOM），保留 `<meta charset="utf-8">`。

## 3. 页型与组件 class 映射

| 蓝图页型 | 顶层结构 | 关键 class |
|---|---|---|
| 封面 | `.cover`（红框+红横条+校徽） | `.cover-head img`、`.cover-mid h1/.sub-cn/.sub-en`、`.cover-info .ci`（答辩人/导师/班级/日期，`.ic` 红方块首字） |
| 目录 | `.slide.toc > .chapter` | 左 `.left .frame/.inner`，右 `.toc-item .idx/.tt`（01–04） |
| 章节过渡 | `.slide.chapter` | `.left`（红竖栏+白细框 `.frame`，`.no` NO.x、`.part` PART ONE）+ `.right h2/.en/.pts` |
| 内容页通用 | `.topbar + .body` | `.section-head h2 + .en`；右下角 `.pagenum`（46×46 红方块白字） |
| 顶部导航 | `.topbar` | `.tb-title`（白竖块 `.dot`+小节名）；`.tb-nav span` 四章节，当前项加 `.cur`（白底红字） |
| 收尾致谢 | `.end` 红底 | `.end h2` 白字、`.end p` Georgia 英文 |

内容页标题区：`.section-head` 内中文 h2（约 30px/800）+ 灰色 Georgia `.en`。

## 4. 卡片 / 图表 / 流程族 class

随蓝图元素选 class，命名保持语义、同类复用：

- 通用强调条：`.review`/`.method-bar`（左 5px 红竖条+浅暖底，圆角右侧）。
- 两栏：`.dual`（grid 1fr 1fr），栏 `.col h3` 带红色 `.tag` 小徽章。
- 普通要点卡：`.exp-box`/`.m-card`/`.mini-card`/`.out-card`/`.eff-card`，统一浅描边圆角、红字 h 标题、灰文 p、`p b` 着墨色。
- 编号并列卡：卡内 `.no`（Georgia 字母间距，LINE 01/OUTPUT 01/RISK 01）。
- 网格：`.merge-grid`（4 列）、`.an-grid`（3 列）、`.feas-grid`（5 列）、`.risk-grid`（2 列，末卡 `.wide` 跨 2 列）。栅格列数保证末行不孤卡。
- KPI：`.kpi .v`（大数字+`<small>`单位）`.l`（指标名）`.src`（国别·年份口径）。
- 条形图：`.bar-row`/`.bar-fill`；迷你表 `.mini-table`；缺口比例用 meter 双色条；误区/政策用 chip 标签。
- 时间轴：`.timeline`（7 列等宽）+ `.tl-item .tl-dot/.tl-date/.tl-tx`，`::before` 横线，圆点中心与线对齐；紧凑版加 `.mtl`。
- 步骤链：`.stepper` > `.stp`（`.sn` 红圆序号、`.st-t`、`.st-s`），`.stp:not(:last-child)::after` 生成向右箭头。
- 风险配对：`.risk-card`（左红竖边）内 `.rk` 风险 + `.ar` 箭头 + 对策文本。
- 技术路线（推荐图片方案）：`.route-wrap`（固定高约 508px、flex 居中）内 `img{max-height/width:100%;object-fit:contain}`，用高清原图锁死防溢出。仅在高度预算确定可控时才用自绘 `.rt-*` 泳道。
- 未来/局限：`.f-up`/`.diff-card`/`.rt-n.fut` 用 `dashed` 描边+灰/浅红底，与实线正式内容区分。

## 5. 强调与虚线约定

- 红字加粗只给关键词与结论，每卡控制在 2–3 处；`.red` 工具类用于行内红字。
- 实线红框=正式内容/主流程；**虚线（dashed）只用于非本期实现、未来扩展、局限/风险**，配文字明确标注"非本期"。
- 流程箭头用实红单向；连向"未来扩展"用虚线箭头（`⇢` 或 dashed 竖线）。
- 并列卡片之间不出现任何连接箭头；箭头只在时间轴、步骤链、卡内"证据→启示/风险→对策"中出现。
- 数据来源脚注统一页底最小灰字（如 `.src-note`），写清来源、年份、口径与可比性限制。

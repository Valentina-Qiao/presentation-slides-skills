# PPTX 模板摄入与 theme spec 确认

## 目录
1. PPTX 内部结构地图
2. inspect_pptx.py 输出解读
3. theme spec schema（确认件）
4. 版式与组件识别
5. 素材抽取与图片处理
6. 信息不足提问清单
7. 强制确认关与 16:9 关卡

---

## 1. PPTX 内部结构地图

.pptx 本质是 zip，先 `unzip -l 模板.pptx` 看清单，需要细看再解压：

| 路径 | 看什么 |
|---|---|
| `ppt/presentation.xml` | `<p:sldSz cx cy>` 画幅（EMU）；幻灯片挂载顺序 |
| `ppt/theme/theme1.xml` | `<a:clrScheme>` 主题色、`<a:fontScheme>` 主/次字体（latin 与 ea 东亚） |
| `ppt/slideMasters/slideMaster1.xml` | 母版：统一导航、页眉页脚、页码占位的总样式 |
| `ppt/slideLayouts/layoutN.xml` | 各类版式：封面、章节页、标题+内容、双栏、收尾 |
| `ppt/slides/slideN.xml` | 真实页面，确认配色与组件的实际用法（主题色可能被局部覆盖） |
| `ppt/media/` | 图片/校徽/logo（png/jpeg/svg），按引用关系定位 |
| `ppt/_rels/*.rels` | 部件间引用，帮助把 media 图片对应到具体版式 |

注意：theme 里的 accent 是候选色，真正的品牌主色要结合 slide/master 实际使用判断（例如某模板 accent1 即大面积导航底色）。主题色与实际用色冲突时，以实际页面大面积使用的颜色为准，并在确认关里向用户点明。

## 2. inspect_pptx.py 输出解读

`python3 scripts/inspect_pptx.py 模板.pptx` 输出 JSON：
- `size_px_96dpi`：96dpi 下像素，16:9 标准模板为 1280×720，直接作为舞台尺寸。
- `ratio_w_h` / `is_16_9`：比例与是否 16:9；非 true 立即停止（见第 7 节）。
- `slide_count`：模板页数，仅用于了解模板规模，不等于你要产出的页数。
- `theme_colors`：`dk1/lt1`（黑/白）、`dk2/lt2`、`accent1..6`、超链接色。挑出主色（通常 accent1）、辅色，再据实际页面补墨色/灰阶/浅底/描边。
- `fonts.majorFont/minorFont`：标题与正文字体，`eastAsian` 是中文字体、`latin` 是西文/数字字体。HTML font-family 按该字体在前、通用 sans 回退书写；英文衬线需求（如 Georgia）若模板使用则照配。
- `media`：素材文件名与字节数，配合 rels 找 logo。

## 3. theme spec schema（确认件）

解析后填下面规格，**发给用户确认后才动工**。值尽量给十六进制与具体字体名。

```yaml
stage: { width_px: 1280, height_px: 720, ratio: "16:9" }
color:
  primary: "#780000"        # 主色：导航/竖栏/页码/强调
  primary_dark: "#5a0000"   # 主色深色（悬停/深块），无则按同色相派生
  ink: "#1F2328"            # 正文与主标题墨色
  text_gray: "#555555"      # 说明文字
  muted: "#8a8a8a"          # 弱注/英文副题
  page_bg: "#fbfafa"        # 浅暖底
  line: "#e6d9d9"           # 卡片描边
font:
  cjk: ["模板中文字体","回退 sans-serif"]
  latin_serif: "Georgia"    # 模板若用衬线英文则填，否则 null
components:
  cover: 封面版式描述（红框/主色块/校徽位/信息栅格）
  topnav: 内容页顶部导航（底色、左小节、右侧章节标签与当前项样式）
  chapter: 章节过渡版式（如左深红竖栏+白细框+NO.x）
  pagenum: 页码形态（位置、形状、底色、字号；哪些页不显示）
  ending: 收尾页版式
assets:
  - { name: 校徽校名, source: ppt/media/imageN.png, upload_url: 待上传 }
notes: 提取存疑或需用户拍板的点
```

确认话术简短具体：列出主色/字体/舞台/四个关键组件，问"以上规格是否准确，确认后开始制作"。

## 4. 版式与组件识别

- 先翻模板真实幻灯片，归类页型：封面、目录、章节过渡、内容页（单栏/双栏/多卡）、收尾。
- 记录重复出现的结构性元素：顶部导航条及其章节标签、侧边竖栏、页码块、标题前的竖块/装饰、卡片描边与圆角、强调色用法。
- HTML 用语义化 class 复现这些组件；骨架已提供通用 topbar/chapter/pagenum 结构，按 spec 改颜色与几何（宽高、圆角、留白），不要发明模板里没有的组件。
- 模板没有的组件（如时间轴、KPI 卡）若蓝图需要，用模板主色与描边风格新建，保持同一视觉语言。

## 5. 素材抽取与图片处理

- 需要的位图从 `ppt/media` 解压导出；同名 svg 可选 png 兜底（浏览器对部分 pptx svg 兼容性不一，优先 png）。
- 用 `file`/图像工具确认尺寸与透明通道；校徽校名常为横幅长条，按原比例 `object-fit:contain`，勿拉伸。
- 云电脑：每张图 `lark-cli drive +html-image-upload --file <path>` 取 `data.url` 写进 `src`；不要用 FileBatchUpload，不要把会过期的外链写进交付 HTML。
- 图片只通过 `<img src>` 或 CSS `url()` 引用，不放进 JS 数组或 data-src。

## 6. 信息不足提问清单（一次问清，避免返工）

- 主题色在 theme 与实际页面不一致时：以哪个为准？
- 模板字体环境没有（如指定某商用字体）：用哪个本地字体回退？
- 模板里看不清的组件/页码规则：章节页是否显示页码？当前章节标签如何高亮？
- logo/校徽有多个版本：用哪个、放封面还是每页？
- 蓝图页数与模板版式不完全对应时：缺的版式允许用同风格新建吗？

## 7. 强制确认关与 16:9 关卡

- **确认关不可跳过**：未拿到用户对 theme spec 的确认，不批量制作页面，避免色板/字体整体跑偏。
- **16:9 关卡**：`is_16_9=false`（如 4:3、宽屏异形）立即停止并告知本期仅支持 16:9；不要改舞台比例或留黑边硬凑。等积累其他比例经验后再扩展本 Skill。
- 确认后的 spec 是后续所有页面的唯一视觉依据，制作中不得临时换色换字体；确需变更回确认关更新。

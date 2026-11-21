---
name: gznf-html-slides
description: "高度复刻「广州南方学院」深红学术答辩模板（主色 #780000、顶部深红导航条、左侧深红竖栏章节页、右下角红色方块页码、红字重点、微软雅黑/等线+Georgia 英文），把幻灯片/答辩内容做成单个自包含、16:9 固定舞台、键盘左右翻页的 HTML 演讲页，并在确认无误后导出为同版式 PDF。用于：用户要求按广州南方学院模板/该 .pptx 复刻、做深红学术风答辩或汇报 HTML、把已做好的该模板 HTML 转 PDF。内容拆页与逻辑先用 ppt-content-blueprint 产出逐页蓝图，本 Skill 只负责忠实视觉化与导出，不擅自改动文案内容。"
---

# 广州南方学院模板 · HTML 演讲页复刻与 PDF 导出（表现层）

把逐页内容蓝图视觉化为深红学术风的单文件 HTML，并可靠导出 PDF。内容结构问题不在本 Skill 解决——**没有逐页蓝图时，先调用 `ppt-content-blueprint`**，拿到蓝图后再开工。

## 前置与边界

- 内容以蓝图为准；只做视觉呈现，**不删减、不改写用户文案**（蓝图铁律在此同样生效）。
- 同时遵守通用 `html` Skill 的硬规则：单文件自包含、CSS/JS 全内联、原生 JS、不用框架、交付一个 .html。本 Skill 只补充品牌规范、固定舞台工艺与 PDF 导出。
- 云电脑环境图片：必须 `lark-cli drive +html-image-upload --file <path>` 取返回的 `data.url` 写进 `src`；**严禁 FileBatchUpload**，外链会过期导致裂图。本地电脑可用相对路径 `assets/`。

## 工作流

1. **解析模板/取素材**：从用户给的 .pptx 解压（unzip）确认色板、字体、比例、校徽校名图片；校徽导出为本地 png 后上传换 URL。素材参考 `references/design-tokens.md`。
2. **搭骨架**：直接基于 `assets/boilerplate.html` 改造（已内置修正后的章节页显隐规则、舞台缩放、翻页脚本），不要从零写，避免重犯显隐 bug。
3. **逐页填内容**：按蓝图选对应页型组件（封面/目录/章节过渡/内容/收尾），用语义化 class；数据脚注、名词解释、虚线边界照蓝图落位。
4. **控高与对齐**：每页内容必须落在 16:9 舞台内，优先用栅格与紧凑组件，不靠目测缩字号；并列卡等高、末行不留孤卡。具体纪律见 `references/pitfalls.md`。
5. **自检页码与总数**：增删页后顺移方块页码，翻页总数由 `slides.length` 自动计算，同步改静态占位文本。
6. **交付 HTML**：用 present_files 只交付最终一个 .html。
7. **确认无误后再导 PDF**：用户确认版式后，按 `references/pdf-export.md` 用 `scripts/export_pdf.py` 逐页渲染合成 16:9 PDF。

## 品牌设计 Token（摘要）

- 主色 `--red:#780000`，深红 `--red-dark:#5a0000`；正文墨色 `--ink:#1F2328`，灰文 `#555`，弱注 `#8a8a8a`；浅红底 `#fdf6f6`，分隔线 `#e6d9d9`，页面底 `#fbfafa`。
- 中文栈 `"Microsoft YaHei","PingFang SC","等线",sans-serif`；英文/数字标题点缀用 `Georgia, serif`。
- 舞台固定 1280×720（16:9），`transform:scale` 等比适配窗口；内容盒安全高度约 580px，所有内容以此为限。
- 标识组件：顶部深红导航条（左小节标题＋右侧四章节标签，当前项白底红字）、章节页左侧深红竖栏内嵌白细框、右下角 46×46 红色方块页码、红字/红框强调、虚线框表未来工作或局限。
- 完整组件清单与可复用 class 命名见 `references/design-tokens.md`。

## 必须守住的坑（精华，逐条详解见 pitfalls.md）

1. **章节页叠加重影**：`.chapter{display:grid}` 会覆盖 `.slide{display:none}`，导致多个章节页常驻叠加。必须显式写 `.slide.chapter{display:none}` 与 `.slide.chapter.active{display:grid}`，目录态另用 `.toc .chapter{display:grid}`。
2. **禁止靠目测缩字号防溢出**：自绘流程图两次溢出过。给容器写死高度并用 `object-fit:contain` 放图，或用紧凑栅格按安全高度预算排版；复杂技术路线优先用用户高清原图 contain 锁高，浏览器保证不溢出。
3. **裂图**：在线图床 URL 会过期；封面校徽不显示先查 src 是否失效，重新 lark 上传换新 URL。
4. **中文乱码**：文件存 UTF-8（可带 BOM）并保留 `<meta charset>` 与 http-equiv 双保险。
5. **并列模块禁因果箭头**，箭头只用于时间/流程或卡内推导；虚线元素专表非本期/局限。
6. **不擅改文案、不固定死高裁切内容**；对称等高，但溢出问题用重构与紧凑组件解决，不删用户的字。
7. **页码顺移、section 开闭配平、翻页总数同步**；导出 PDF 前确认是最终版。

## PDF 导出（用户确认 HTML 后才做）

不要用浏览器直接 print（其余幻灯片 `display:none` 只会导出当前页），也不要用 LibreOffice（对 flex/transform 复刻差）。固定路径是 Playwright 调系统 Chromium 逐页 `show(i)` 截 `#stage`（2 倍分辨率），再用 PyMuPDF 按 1280×720 合成 PDF。完整步骤、依赖、离线图片处理见 `references/pdf-export.md`，可直接运行 `scripts/export_pdf.py`。

## 资源索引

- `references/design-tokens.md`：完整色板/字体/版式/组件与 class 命名、页型对应组件。
- `references/pitfalls.md`：本次全部踩坑复盘、根因与避坑写法、防溢出清单。
- `references/pdf-export.md`：HTML→16:9 PDF 的可靠工艺与故障排查。
- `assets/boilerplate.html`：可直接改造的单文件骨架（含已修复的显隐规则、舞台缩放、翻页、方块页码）。
- `scripts/export_pdf.py`：逐页截图合成 PDF 的参数化脚本。

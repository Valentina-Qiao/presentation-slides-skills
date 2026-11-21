---
name: pptx-stage-slides
description: "当用户提供一个 .pptx 模板，要求按该模板的配色/字体/版式复刻成单个自包含、16:9 固定舞台、键盘左右翻页的 HTML 演讲页，并在确认无误后导出同版式 PDF 时使用。本 Skill 先解析 PPTX 生成一份主题规格 theme spec（画幅、色板、字体、封面/导航/章节/页码版式、logo 素材），经用户确认后再驱动通用骨架视觉化，因此能适配任意品牌模板而非写死某一套。当前仅支持 .pptx 输入、仅做 16:9 画幅。内容拆页逻辑先用 ppt-content-blueprint 产出逐页蓝图；若用户指定的是已内置的广州南方学院模板，改用更快捷的 gznf-html-slides。"
---

# PPTX 模板驱动 · 通用固定舞台 HTML 与 PDF（表现层 · 模板可插拔）

把"任意 PPTX 模板 → 同风格 16:9 HTML 演讲页 → PDF"做成标准工艺。模板不是硬编码，而是先解析成一份 **theme spec**，确认后注入通用骨架。

## 适用边界（本期）

- 输入仅支持 **.pptx**；参考图片、手绘稿、现成 HTML 不在本期范围，遇到则说明并请用户提供 pptx。
- 仅做 **16:9**：`inspect_pptx.py` 报 `is_16_9=false` 时停止并告知当前不支持其他画幅，不要自行拉伸。
- 内容结构来自 `ppt-content-blueprint` 的逐页蓝图；没有蓝图先调用它。本 Skill 不擅自改文案。
- 广州南方学院这一已知模板有内置快捷 Skill `gznf-html-slides`，可直接用；本 Skill 面向新模板。
- 同时遵守通用 `html` Skill：单文件自包含、CSS/JS 内联、原生 JS、只交付一个 .html。

## 工作流

### 1. 解析模板（确定性提取，不靠目测）
运行 `scripts/inspect_pptx.py <模板.pptx>`，得到画幅像素与比例、幻灯片数、主题色板（accent 等）、major/minor 拉丁与东亚字体、媒体清单。再 `unzip` 查看 `ppt/slideMasters`、`ppt/slideLayouts` 辨识封面/章节/内容/收尾版式与导航、页码形态，并从 `ppt/media` 定位 logo/校徽等素材。

### 2. 生成 theme spec 并强制确认（关键关卡，不可跳过）
按 `references/template-intake.md` 的 schema 填一份主题规格：主色/辅色/墨色/灰阶/描边、中英字体、舞台尺寸、各页型版式与组件、需要抽取的图片素材。**先把这份 spec 简明呈现给用户确认色板、字体、版式，再进入制作**；信息提取不到或有歧义时按该文档的提问清单问清，不要猜。

### 3. 准备素材
导出需要的 logo/图片为本地文件；云电脑用 `lark-cli drive +html-image-upload --file <path>` 取不过期 `data.url` 写入 `src`，严禁 FileBatchUpload；本地电脑可用相对路径 `assets/`。

### 4. 注入规格、搭建骨架
复制 `assets/boilerplate.generic.html`，把确认后的色板/字体填入 `:root` 变量，按 spec 调整封面、导航条、章节竖栏、页码等组件外观；保持骨架已内置的舞台、显隐规则与翻页接口不变。

### 5. 按蓝图填充并守住工艺
逐页把蓝图内容视觉化为卡片/图表/时间轴等，遵循 `references/stagecraft.md`：内容安全高约 580px、显隐铁规则、并列禁箭头、虚线表未来/局限、不删文案、对称等高、数据带口径。

### 6. 交付前核对
显隐无重影、无元素超舞台、图片无裂图、方块页码连续且总页数同步、section 配平、编码 UTF-8。用 present_files 交付唯一一个最终 .html。

### 7. 用户确认后再导 PDF
禁用浏览器直接打印与 LibreOffice。按 `references/pdf-export.md` 运行 `scripts/export_pdf.py`，Playwright 逐页 `show(i)` 截 `#stage`、PyMuPDF 合成 1280×720 PDF；离线图片用 `--map "URL|本地路径"`。

## 资源索引

- `references/template-intake.md`：PPTX 内部结构、解析输出解读、theme spec schema 与确认话术、素材识别、信息不足提问清单、16:9 关卡。
- `references/stagecraft.md`：模板无关的固定舞台工艺与避坑（显隐、防溢出、翻页接口契约、传图、编码、页码、关系箭头）。
- `references/pdf-export.md`：HTML→16:9 PDF 工艺、依赖与故障排查。
- `scripts/inspect_pptx.py`：解析 pptx 输出 JSON 主题信息（标准库，已实测）。
- `scripts/export_pdf.py`：逐页截图合成 PDF 的参数化脚本（已实测）。
- `assets/boilerplate.generic.html`：中性通用骨架，颜色走 CSS 变量，按 spec 注入。

# Presentation Slides Skills

一组把「内容文档 → 幻灯片 → HTML 演讲页 → PDF」流程化、可复用的 AI Agent Skills。三个 Skill 分层解耦，可单独使用，也可串联。

## 目录结构

```
presentation-slides-skills/
├── ppt-content-blueprint/   # A 内容层（通用）：拆页逻辑与逐页蓝图，与模板无关
├── pptx-stage-slides/       # C 表现层（通用工艺）：解析任意 PPTX → 主题规格确认 → 16:9 HTML/PDF
└── gznf-html-slides/        # B 表现层（品牌特化）：广州南方学院深红模板的快捷通道
```

## 分工与调用关系

| Skill | 层级 | 输入 | 产物 |
|---|---|---|---|
| `ppt-content-blueprint` | 内容层 | 论文/报告/方案等内容文档 | 逐页内容蓝图（页型、要点、并列/流程/因果关系、强调点、数据口径） |
| `pptx-stage-slides` | 表现层·通用 | 任意 16:9 `.pptx` 模板 + 内容蓝图 | 同风格单文件 HTML、并可导出 16:9 PDF |
| `gznf-html-slides` | 表现层·特化 | 广州南方学院模板场景 + 内容蓝图 | 同上，内置品牌规格、省去模板解析 |

- 只做内容大纲：单独用 `ppt-content-blueprint`。
- 套用新模板：`pptx-stage-slides` 先解析 PPTX 生成主题规格（theme spec），确认后再制作。
- 广州南方学院场景：用内置规格的 `gznf-html-slides` 快速通道。

## 关键约定

- 单文件、自包含、原生 JS 的 16:9 固定舞台 HTML，键盘左右翻页。
- 内容只重组不删减；并列模块之间不使用因果箭头；虚线元素专表未来工作/局限。
- HTML 转 PDF 采用 Playwright 逐页截图 + PyMuPDF 合成，保证与屏幕版式一致（见各 Skill `scripts/`）。
- `pptx-stage-slides` 当前仅支持 `.pptx` 输入与 16:9 画幅。

每个 Skill 目录内含 `SKILL.md`、按需的 `references/`、`scripts/`、`assets/`。

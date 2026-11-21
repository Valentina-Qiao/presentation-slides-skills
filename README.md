# Presentation Slides Skills（导航入口）

把「内容文档 → 幻灯片 → HTML 演讲页 → PDF」流程化的一组 AI Agent Skills。已拆分为三个**相互独立、可单独安装复用**的公开仓库；本仓为导航与总览入口，权威实现以三个独立仓为准（仓内早期版本子目录仅留档，不再更新）。

## 三个独立仓库

| Skill | 层级 | 一句话作用 | 仓库 |
|---|---|---|---|
| `ppt-content-blueprint` | 内容层·通用 | 把内容文档拆成逐页蓝图（页型/要点/关系/表达元素/数据口径），不绑模板 | [打开仓库](https://github.com/Valentina-Qiao/ppt-content-blueprint) |
| `pptx-stage-slides` | 表现层·通用工艺 | 解析任意 16:9 `.pptx` → 主题规格确认 → 固定舞台 HTML/PDF | [打开仓库](https://github.com/Valentina-Qiao/pptx-stage-slides) |
| `gznf-html-slides` | 表现层·品牌特化 | 广州南方学院深红模板的快捷复刻通道与 PDF 导出 | [打开仓库](https://github.com/Valentina-Qiao/gznf-html-slides) |

## 怎么选用

- 只做内容大纲：单独用 `ppt-content-blueprint`。
- 套用新 PPTX 模板：`pptx-stage-slides`（先解析出 theme spec，确认后再制作；仅支持 .pptx、16:9）。
- 广州南方学院场景：用内置品牌规格的 `gznf-html-slides`，省去模板解析。
- 成套使用：先 `ppt-content-blueprint` 出蓝图，再交 `gznf-html-slides` 或 `pptx-stage-slides` 视觉化并导出 PDF。

## 共同约定

- 单文件、自包含、原生 JS 的 16:9 固定舞台 HTML，键盘左右翻页。
- 内容只重组不删减；并列模块之间不用因果箭头；虚线元素专表未来工作/局限。
- HTML 转 PDF 统一用 Playwright 逐页截图 + PyMuPDF 合成，保证与屏幕版式一致。

# 固定舞台 HTML → 16:9 PDF 工艺

## 为什么不用常规打印
- 非当前幻灯片是 `display:none`，Chromium `--print-to-pdf` 只会导出当前一张；手工注入打印 CSS 重排固定舞台易出错。
- LibreOffice 对 flex/transform/现代 CSS 复刻差，禁止使用。
- 可靠路径：**Playwright 驱动系统 Chromium，逐页 `show(i)` 激活并对 `#stage` 2 倍截图，PyMuPDF 按 1280×720 合成 PDF**，分页天然正确、视觉与屏幕一致。

## 依赖
- 系统 Chromium（脚本自动探测 chromium / chromium-browser / google-chrome）。
- Python 包：`python -m pip install pymupdf playwright`（浏览器可直接用系统 Chromium，无需另下载）。
- 中文字体：`fc-list :lang=zh | wc -l` 非 0；为空则装 Noto CJK，否则出豆腐块。

## 用法
```bash
# 在线图片可访问
python3 export_pdf.py --html /path/slides.html --out /path/slides.pdf

# 离线/防图床失效：把在线 URL 换本地文件，--map 可重复
python3 export_pdf.py \
  --html /path/slides.html --out /path/slides.pdf \
  --map "https://host/old.png|/abs/assets/logo.png"
```
参数：`--width/--height` 默认 1280/720（本 Skill 仅 16:9，不要改）；`--scale` 默认 2（输出 2560×1440 再缩回 1280×720 点，高清）；`--wait` 切页等待毫秒默认 220。

## 契约与边界
- 页面需暴露全局 `slides` 与 `show(i)`、舞台 id `stage`，通用骨架已满足；脚本检测不到会报错提示。
- `--map` 只改临时副本，不动交付 HTML；交付 HTML 仍保留不过期在线 URL。
- PDF 每页 1280×720 点、无页边距，图片填满整页。
- 非 16:9 模板本期不支持，无需调整脚本宽高去硬适配。

## 故障排查
- 中文方块：查中文字体与 font-family 回退。
- 裂图：用 `--map` 换本地 file 资源，load 后保留等待时间。
- `slides/show is not defined`：未用约定骨架，改回标准翻页命名。
- 找不到浏览器：确认 `which chromium`，或让 Playwright 安装自带浏览器。
- 画面未稳定就截：调大 `--wait` 或等待 networkidle。
- 生成后直接交付，不再重开逐页审校。

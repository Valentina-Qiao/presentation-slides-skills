# HTML 演讲页 → 16:9 PDF 可靠工艺

## 为什么不用常规"打印/另存 PDF"
- 幻灯片其余页是 `.slide{display:none}`，靠 `.active` 切换。Chromium 直接 `--print-to-pdf` 只会导出当前一张；注入打印 CSS 重排固定舞台易出错。
- LibreOffice headless 对 flex/transform/现代 CSS 复刻差，版面会错位，禁止用于这类页面。
- 可靠做法：**Playwright 驱动系统 Chromium，逐页激活并对 `#stage` 截图，再用 PyMuPDF 把等尺寸图片合成 PDF**。视觉与屏幕 100% 一致，分页天然正确。

## 依赖（一次性）
- 系统 Chromium（`which chromium`，也可用 chromium-browser/google-chrome）。
- Python 包：`playwright`（仅用其驱动，浏览器可指向系统 Chromium，无需另下载）、`pymupdf`。
  - 安装：`python -m pip install pymupdf playwright`
- 中文字体：`fc-list :lang=zh | wc -l` 应非 0；若为 0 安装 Noto CJK（如 `fonts-noto-cjk`），否则 PDF 出豆腐块。

## 用法
脚本：`scripts/export_pdf.py`

```bash
# 在线 URL 可访问时，直接渲染
python3 export_pdf.py --html /path/幻灯片.html --out /path/幻灯片.pdf

# 离线/防止图床失效：把某个在线图片 URL 换成本地文件，可重复 --map
python3 export_pdf.py \
  --html /path/幻灯片.html --out /path/幻灯片.pdf \
  --map "https://media.doubao.com/.../xxx|/path/assets/校徽校名.png" \
  --map "https://media.doubao.com/.../yyy|/path/assets/技术路线图.png"
```

参数：`--width/--height` 默认 1280/720（不要改，保持 16:9）；`--scale` 默认 2（输出 2560×1440 高清位图再缩回 1280×720 点）；`--wait` 每页等待毫秒默认 220。

## 脚本约定（骨架需满足）
- 页面暴露全局 `slides`（Node 数组）与 `show(i)`，舞台元素 id 为 `stage`——`assets/boilerplate.html` 已满足，自建页面保持同名即可。
- PDF 每页 1280×720 点，图片 `insert_image` 填满整页，无页边距。
- `--map` 仅作用于临时副本，不改动交付的 HTML；交付 HTML 内仍保留不过期的在线 URL。

## 故障排查
- 中文方块：先查中文字体；确认 font-family 含可回退的 sans-serif，重跑。
- 图片空白/裂图：用 `--map` 换本地 `file://` 资源离线渲染；确认 `goto wait_until=load` 后留有等待时间。
- 报 `slides/show is not defined`：页面没按骨架暴露全局翻页接口，改用 boilerplate 的脚本命名。
- Playwright 找不到浏览器：给 `executable_path` 指定 `which chromium` 的结果；脚本已内置常见路径探测。
- 某页动画未稳定就截：调大 `--wait`，或对图片 `wait_for_load_state('networkidle')`。
- 生成后按 pdf Skill 规则直接交付，不再重开逐页审校。

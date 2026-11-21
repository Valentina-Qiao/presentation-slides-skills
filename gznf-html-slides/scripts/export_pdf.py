#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把固定 16:9 舞台的单文件 HTML 演讲页逐页渲染并合成为 PDF。

原理：Playwright + 系统 Chromium 逐页调用 show(i)，对 #stage 做 2x 截图，
再用 PyMuPDF 按 1280x720 合成每页一张幻灯片的 PDF（视觉与屏幕一致）。

用法：
  python3 export_pdf.py --html slides.html --out slides.pdf
  python3 export_pdf.py --html slides.html --out slides.pdf \
      --map "https://host/old.png|/abs/local/new.png"
"""
import argparse
import pathlib
import shutil
import tempfile

import pymupdf
from playwright.sync_api import sync_playwright


def find_chromium():
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        path = shutil.which(name)
        if path:
            return path
    return None  # 回退到 Playwright 自带浏览器


def parse_maps(values):
    pairs = []
    for v in values or []:
        if "|" not in v:
            raise SystemExit(f"--map 格式应为 '在线URL|本地路径'，收到：{v}")
        url, local = v.split("|", 1)
        pairs.append((url.strip(), pathlib.Path(local.strip()).resolve().as_uri()))
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True, help="源 HTML 路径")
    ap.add_argument("--out", required=True, help="输出 PDF 路径")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--scale", type=float, default=2.0, help="设备像素比，控制清晰度")
    ap.add_argument("--wait", type=int, default=220, help="每页切换后等待毫秒")
    ap.add_argument("--map", action="append", help="在线URL|本地文件，可重复，用于离线替换图片")
    args = ap.parse_args()

    html_path = pathlib.Path(args.html).resolve()
    out_path = pathlib.Path(args.out).resolve()
    html = html_path.read_text(encoding="utf-8-sig")
    for url, file_uri in parse_maps(args.map):
        if url not in html:
            print(f"[warn] 未在 HTML 中找到待替换 URL：{url}")
        html = html.replace(url, file_uri)

    work = pathlib.Path(tempfile.mkdtemp(prefix="html_pdf_"))
    tmp_html = work / "print.html"
    tmp_html.write_text(html, encoding="utf-8")
    png_dir = work / "pages"
    png_dir.mkdir()

    pngs = []
    with sync_playwright() as p:
        launch_kwargs = {"args": ["--no-sandbox", "--disable-dev-shm-usage",
                                  "--force-color-profile=srgb", "--font-render-hinting=none"]}
        exe = find_chromium()
        if exe:
            launch_kwargs["executable_path"] = exe
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale)
        page.goto(tmp_html.as_uri(), wait_until="load")
        page.wait_for_timeout(800)

        total = page.evaluate("typeof slides !== 'undefined' ? slides.length : 0")
        if not total:
            raise SystemExit("页面未暴露全局 slides/show，请使用约定骨架（id=stage、window.slides、show(i)）。")
        page.evaluate("const st=document.getElementById('stage'); if(st) st.style.boxShadow='none';")
        stage = page.locator("#stage")
        for i in range(total):
            page.evaluate(f"show({i})")
            page.wait_for_timeout(args.wait)
            png = png_dir / f"p{i:02d}.png"
            stage.screenshot(path=str(png))
            pngs.append(png)
        browser.close()

    doc = pymupdf.open()
    for png in pngs:
        pg = doc.new_page(width=args.width, height=args.height)
        pg.insert_image(pymupdf.Rect(0, 0, args.width, args.height), filename=str(png))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path, garbage=4, deflate=True)
    doc.close()
    shutil.rmtree(work, ignore_errors=True)
    print(f"PDF saved: {out_path} pages: {len(pngs)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析 .pptx 模板，提取复刻固定舞台 HTML 所需的主题规格原始信息。

仅用标准库。输出 JSON：画幅(EMU/像素/比例/是否16:9)、幻灯片数、主题色板、
主/次字体（拉丁与东亚）、媒体素材清单。供生成 theme spec 并与用户确认。

用法：python3 inspect_pptx.py template.pptx
"""
import argparse
import json
import zipfile
import xml.etree.ElementTree as ET

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
EMU_PER_PX = 9525.0  # 96dpi: 914400 EMU/英寸 ÷ 96
EMU_PER_IN = 914400.0


def q(ns, tag):
    return f"{{{ns}}}{tag}"


def color_of(node):
    """取 clr 节点下的 srgbClr val 或 sysClr lastClr。"""
    srgb = node.find(f".//{q(A,'srgbClr')}")
    if srgb is not None:
        return "#" + srgb.get("val", "").upper()
    sysc = node.find(f".//{q(A,'sysClr')}")
    if sysc is not None:
        return "#" + (sysc.get("lastClr") or sysc.get("val") or "").upper()
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    args = ap.parse_args()

    with zipfile.ZipFile(args.pptx) as z:
        names = set(z.namelist())

        # 画幅与幻灯片数
        pres = ET.fromstring(z.read("ppt/presentation.xml"))
        sld = pres.find(f".//{q(P,'sldSz')}")
        cx, cy = int(sld.get("cx")), int(sld.get("cy"))
        slide_count = len([n for n in names if n.startswith("ppt/slides/slide") and n.endswith(".xml")])

        # 主题色与字体（取 theme1）
        colors, fonts = {}, {}
        theme_path = "ppt/theme/theme1.xml"
        if theme_path in names:
            theme = ET.fromstring(z.read(theme_path))
            scheme = theme.find(f".//{q(A,'clrScheme')}")
            if scheme is not None:
                for child in scheme:
                    val = color_of(child)
                    if val:
                        colors[child.tag.split("}")[-1]] = val
            fscheme = theme.find(f".//{q(A,'fontScheme')}")
            if fscheme is not None:
                for role in ("majorFont", "minorFont"):
                    f = fscheme.find(q(A, role))
                    if f is None:
                        continue
                    latin = f.find(q(A, "latin"))
                    ea = f.find(q(A, "ea"))
                    fonts[role] = {
                        "latin": latin.get("typeface") if latin is not None else None,
                        "eastAsian": ea.get("typeface") if ea is not None else None,
                    }

        media = sorted(n for n in names if n.startswith("ppt/media/") and not n.endswith("/"))
        media_list = [{"file": n.split("/")[-1], "bytes": z.getinfo(n).file_size} for n in media]

    w_px, h_px = round(cx / EMU_PER_PX), round(cy / EMU_PER_PX)
    ratio = round(cx / cy, 4)
    result = {
        "file": args.pptx,
        "size_emu": {"cx": cx, "cy": cy},
        "size_inch": {"w": round(cx / EMU_PER_IN, 3), "h": round(cy / EMU_PER_IN, 3)},
        "size_px_96dpi": {"w": w_px, "h": h_px},
        "ratio_w_h": ratio,
        "is_16_9": abs(ratio - 16 / 9) < 0.01,
        "stage_target_px": {"w": 1280, "h": 720} if abs(ratio - 16 / 9) < 0.01 else None,
        "slide_count": slide_count,
        "theme_colors": colors,
        "fonts": fonts,
        "media": media_list,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

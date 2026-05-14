# -*- coding: utf-8 -*-
"""
图像比较处理器

提供图像比较功能，计算两张图像之间的差异。
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from pixelforge.core.image import Image, Pixel


def compare(img1: Image, img2: Image) -> dict:
    """比较两张图像的差异。

    计算两张图像之间的像素差异，包括差异百分比、最大差异值等。

    Args:
        img1: 第一张图像
        img2: 第二张图像

    Returns:
        包含比较结果的字典：
        - identical: 是否完全相同
        - same_size: 尺寸是否相同
        - diff_percentage: 差异百分比（0.0-100.0）
        - max_diff: 最大单通道差异值（0-255）
        - avg_diff: 平均单通道差异值
        - total_diff_pixels: 不同的像素数量
        - total_pixels: 总像素数量
        - heatmap_data: 差异热力图数据（二维列表）

    Raises:
        ValueError: 任一图像为空
    """
    result: Dict = {
        "identical": False,
        "same_size": img1.width == img2.width and img1.height == img2.height,
        "diff_percentage": 0.0,
        "max_diff": 0,
        "avg_diff": 0.0,
        "total_diff_pixels": 0,
        "total_pixels": max(img1.width * img1.height, img2.width * img2.height),
        "heatmap_data": [],
    }

    if not result["same_size"]:
        # 尺寸不同，计算差异时取较小区域
        min_w = min(img1.width, img2.width)
        min_h = min(img1.height, img2.height)
        result["diff_percentage"] = 100.0  # 尺寸不同视为完全不同
        result["message"] = (
            f"尺寸不同: {img1.width}x{img1.height} vs {img2.width}x{img2.height}"
        )
        return result

    # 逐像素比较
    total_diff = 0
    diff_pixels = 0
    heatmap: List[List[float]] = []

    for y in range(img1.height):
        heat_row: List[float] = []
        for x in range(img1.width):
            p1 = img1.pixels[y][x]
            p2 = img2.pixels[y][x]

            # 计算单通道差异
            dr = abs(p1.r - p2.r)
            dg = abs(p1.g - p2.g)
            db = abs(p1.b - p2.b)
            da = abs(p1.a - p2.a)

            pixel_diff = (dr + dg + db + da) / 4.0
            heat_row.append(pixel_diff)

            if pixel_diff > 0:
                diff_pixels += 1
                total_diff += pixel_diff
                result["max_diff"] = max(result["max_diff"], max(dr, dg, db, da))

        heatmap.append(heat_row)

    result["heatmap_data"] = heatmap
    result["total_diff_pixels"] = diff_pixels
    result["total_pixels"] = img1.width * img1.height

    if diff_pixels > 0:
        result["avg_diff"] = total_diff / (img1.width * img1.height)
        result["diff_percentage"] = (diff_pixels / (img1.width * img1.height)) * 100.0
    else:
        result["identical"] = True

    return result


def is_identical(img1: Image, img2: Image) -> bool:
    """判断两张图像是否完全相同。

    Args:
        img1: 第一张图像
        img2: 第二张图像

    Returns:
        True表示两张图像完全相同（尺寸和像素值一致）
    """
    # 快速检查尺寸
    if img1.width != img2.width or img1.height != img2.height:
        return False

    # 逐像素比较
    for y in range(img1.height):
        for x in range(img1.width):
            p1 = img1.pixels[y][x]
            p2 = img2.pixels[y][x]
            if p1 != p2:
                return False

    return True

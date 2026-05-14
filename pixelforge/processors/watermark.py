# -*- coding: utf-8 -*-
"""
文本水印处理器

为图像添加文本水印，支持多种位置和透明度设置。
使用内置位图字体渲染文本。
"""

from __future__ import annotations

from typing import Optional

from pixelforge.core.image import Image, Pixel
from pixelforge.utils.text import measure_text, render_text_to_pixels


def add_text_watermark(
    img: Image,
    text: str,
    position: str = "bottom-right",
    opacity: float = 0.5,
    font_size: int = 12,
    color: tuple = (255, 255, 255),
    margin: int = 10
) -> Image:
    """为图像添加文本水印。

    Args:
        img: 输入图像
        text: 水印文本
        position: 水印位置，可选值：
            'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'
        opacity: 透明度，0.0（完全透明）到1.0（完全不透明）
        font_size: 字体大小（像素），默认12
        color: 水印颜色 (R, G, B)，默认白色
        margin: 边距（像素），默认10

    Returns:
        添加水印后的图像（新Image对象）

    Raises:
        ValueError: 不支持的位置参数
    """
    if position not in ("top-left", "top-right", "bottom-left",
                        "bottom-right", "center"):
        raise ValueError(
            f"不支持的水印位置: {position}，"
            f"可选: top-left, top-right, bottom-left, bottom-right, center"
        )

    opacity = max(0.0, min(1.0, opacity))
    result = img.copy()

    # 渲染文本为像素矩阵
    text_pixels = render_text_to_pixels(text, font_size, color)
    if not text_pixels:
        return result

    text_height = len(text_pixels)
    text_width = len(text_pixels[0]) if text_pixels else 0

    # 计算水印位置
    if position == "top-left":
        start_x = margin
        start_y = margin
    elif position == "top-right":
        start_x = img.width - text_width - margin
        start_y = margin
    elif position == "bottom-left":
        start_x = margin
        start_y = img.height - text_height - margin
    elif position == "bottom-right":
        start_x = img.width - text_width - margin
        start_y = img.height - text_height - margin
    else:  # center
        start_x = (img.width - text_width) // 2
        start_y = (img.height - text_height) // 2

    # 确保不越界
    start_x = max(0, start_x)
    start_y = max(0, start_y)

    # 将水印像素混合到图像上
    for ty, row in enumerate(text_pixels):
        img_y = start_y + ty
        if img_y >= img.height:
            break
        for tx, text_pixel in enumerate(row):
            img_x = start_x + tx
            if img_x >= img.width:
                break

            # text_pixel 是 (r, g, b, a) 或 None
            if text_pixel is None:
                continue

            tr, tg, tb, ta = text_pixel
            # 应用用户设定的透明度
            effective_alpha = ta * opacity / 255.0

            if effective_alpha <= 0:
                continue

            # Alpha混合
            dst = result.pixels[img_y][img_x]
            new_r = int(dst.r * (1 - effective_alpha) + tr * effective_alpha)
            new_g = int(dst.g * (1 - effective_alpha) + tg * effective_alpha)
            new_b = int(dst.b * (1 - effective_alpha) + tb * effective_alpha)

            result.pixels[img_y][img_x] = Pixel(
                max(0, min(255, new_r)),
                max(0, min(255, new_g)),
                max(0, min(255, new_b)),
                dst.a
            )

    return result

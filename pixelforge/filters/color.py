# -*- coding: utf-8 -*-
"""
颜色操作滤镜

提供色调、饱和度和色温调整功能。
基于RGB与HSL色彩空间的转换实现。
"""

from __future__ import annotations

import math
from typing import List

from pixelforge.core.image import Image, Pixel


def _rgb_to_hsl(r: int, g: int, b: int) -> tuple:
    """将RGB颜色值转换为HSL色彩空间。

    Args:
        r: 红色 (0-255)
        g: 绿色 (0-255)
        b: 蓝色 (0-255)

    Returns:
        (h, s, l) 元组，h为0-360度，s和l为0.0-1.0
    """
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0

    c_max = max(r_norm, g_norm, b_norm)
    c_min = min(r_norm, g_norm, b_norm)
    delta = c_max - c_min

    # 亮度
    l = (c_max + c_min) / 2.0

    # 饱和度
    if delta == 0:
        s = 0.0
        h = 0.0
    else:
        s = delta / (1.0 - abs(2.0 * l - 1.0)) if (1.0 - abs(2.0 * l - 1.0)) != 0 else 0.0

        # 色调
        if c_max == r_norm:
            h = 60.0 * (((g_norm - b_norm) / delta) % 6)
        elif c_max == g_norm:
            h = 60.0 * (((b_norm - r_norm) / delta) + 2)
        else:
            h = 60.0 * (((r_norm - g_norm) / delta) + 4)

    if h < 0:
        h += 360.0

    return (h, s, l)


def _hsl_to_rgb(h: float, s: float, l: float) -> tuple:
    """将HSL颜色值转换为RGB色彩空间。

    Args:
        h: 色调 (0-360)
        s: 饱和度 (0.0-1.0)
        l: 亮度 (0.0-1.0)

    Returns:
        (r, g, b) 元组，每个值0-255
    """
    c = (1.0 - abs(2.0 * l - 1.0)) * s
    x = c * (1.0 - abs((h / 60.0) % 2 - 1.0))
    m = l - c / 2.0

    if h < 60:
        r1, g1, b1 = c, x, 0
    elif h < 120:
        r1, g1, b1 = x, c, 0
    elif h < 180:
        r1, g1, b1 = 0, c, x
    elif h < 240:
        r1, g1, b1 = 0, x, c
    elif h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x

    r = int((r1 + m) * 255)
    g = int((g1 + m) * 255)
    b = int((b1 + m) * 255)

    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def adjust_hue(img: Image, degrees: float) -> Image:
    """调整图像色调。

    Args:
        img: 输入图像
        degrees: 色调偏移量（度），正值顺时针偏移，负值逆时针偏移

    Returns:
        色调调整后的图像（新Image对象）
    """
    new_pixels: List[List[Pixel]] = []
    for row in img.pixels:
        new_row: List[Pixel] = []
        for pixel in row:
            h, s, l = _rgb_to_hsl(pixel.r, pixel.g, pixel.b)
            # 偏移色调
            h = (h + degrees) % 360
            if h < 0:
                h += 360
            r, g, b = _hsl_to_rgb(h, s, l)
            new_row.append(Pixel(r, g, b, pixel.a))
        new_pixels.append(new_row)
    return Image(img.width, img.height, new_pixels, img.format)


def saturate(img: Image, factor: float) -> Image:
    """调整图像饱和度。

    Args:
        img: 输入图像
        factor: 饱和度因子，>1增加饱和度，<1降低饱和度，0为灰度

    Returns:
        饱和度调整后的图像（新Image对象）
    """
    factor = max(0.0, factor)
    new_pixels: List[List[Pixel]] = []
    for row in img.pixels:
        new_row: List[Pixel] = []
        for pixel in row:
            h, s, l = _rgb_to_hsl(pixel.r, pixel.g, pixel.b)
            # 调整饱和度
            s = max(0.0, min(1.0, s * factor))
            r, g, b = _hsl_to_rgb(h, s, l)
            new_row.append(Pixel(r, g, b, pixel.a))
        new_pixels.append(new_row)
    return Image(img.width, img.height, new_pixels, img.format)


def color_temperature(img: Image, value: int) -> Image:
    """调整图像色温。

    正值使图像偏暖（增加红色，减少蓝色），
    负值使图像偏冷（增加蓝色，减少红色）。

    Args:
        img: 输入图像
        value: 色温调整值，建议范围-100到100

    Returns:
        色温调整后的图像（新Image对象）
    """
    value = max(-255, min(255, value))
    new_pixels: List[List[Pixel]] = []
    for row in img.pixels:
        new_row: List[Pixel] = []
        for pixel in row:
            r = pixel.r
            g = pixel.g
            b = pixel.b

            if value > 0:
                # 偏暖：增加红色，减少蓝色
                r = max(0, min(255, int(r + value)))
                b = max(0, min(255, int(b - value)))
                # 绿色略微增加
                g = max(0, min(255, int(g + value * 0.1)))
            else:
                # 偏冷：增加蓝色，减少红色
                r = max(0, min(255, int(r + value)))
                b = max(0, min(255, int(b - value)))
                # 绿色略微增加
                g = max(0, min(255, int(g - value * 0.1)))

            new_row.append(Pixel(r, g, b, pixel.a))
        new_pixels.append(new_row)
    return Image(img.width, img.height, new_pixels, img.format)

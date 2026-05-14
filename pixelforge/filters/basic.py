# -*- coding: utf-8 -*-
"""
基础图像滤镜

提供常用的图像处理滤镜，包括灰度化、反色、亮度调整、对比度调整、
二值化和复古色调等。
"""

from __future__ import annotations

from typing import List

from pixelforge.core.image import Image, Pixel


def grayscale(img: Image) -> Image:
    """将图像转换为灰度。

    使用ITU-R BT.601标准加权公式：
    Gray = 0.299 * R + 0.587 * G + 0.114 * B

    Args:
        img: 输入图像

    Returns:
        灰度图像（新Image对象）
    """
    new_pixels: List[List[Pixel]] = []
    for row in img.pixels:
        new_row: List[Pixel] = []
        for pixel in row:
            # 标准灰度公式
            gray = int(0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b)
            gray = max(0, min(255, gray))
            new_row.append(Pixel(gray, gray, gray, pixel.a))
        new_pixels.append(new_row)
    return Image(img.width, img.height, new_pixels, img.format)


def invert(img: Image) -> Image:
    """图像反色处理。

    将每个像素的RGB值取反（255 - 原值）。

    Args:
        img: 输入图像

    Returns:
        反色图像（新Image对象）
    """
    new_pixels: List[List[Pixel]] = []
    for row in img.pixels:
        new_row: List[Pixel] = []
        for pixel in row:
            new_row.append(Pixel(
                255 - pixel.r,
                255 - pixel.g,
                255 - pixel.b,
                pixel.a
            ))
        new_pixels.append(new_row)
    return Image(img.width, img.height, new_pixels, img.format)


def brightness(img: Image, factor: float) -> Image:
    """调整图像亮度。

    Args:
        img: 输入图像
        factor: 亮度因子，>0增加亮度，<0降低亮度，范围建议-255到255

    Returns:
        调整后的图像（新Image对象）
    """
    new_pixels: List[List[Pixel]] = []
    for row in img.pixels:
        new_row: List[Pixel] = []
        for pixel in row:
            new_row.append(Pixel(
                max(0, min(255, int(pixel.r + factor))),
                max(0, min(255, int(pixel.g + factor))),
                max(0, min(255, int(pixel.b + factor))),
                pixel.a
            ))
        new_pixels.append(new_row)
    return Image(img.width, img.height, new_pixels, img.format)


def contrast(img: Image, factor: float) -> Image:
    """调整图像对比度。

    Args:
        img: 输入图像
        factor: 对比度因子，>1增加对比度，<1降低对比度，建议范围0.0-3.0

    Returns:
        调整后的图像（新Image对象）
    """
    # 对比度调整公式：new = factor * (old - 128) + 128
    new_pixels: List[List[Pixel]] = []
    for row in img.pixels:
        new_row: List[Pixel] = []
        for pixel in row:
            new_row.append(Pixel(
                max(0, min(255, int(factor * (pixel.r - 128) + 128))),
                max(0, min(255, int(factor * (pixel.g - 128) + 128))),
                max(0, min(255, int(factor * (pixel.b - 128) + 128))),
                pixel.a
            ))
        new_pixels.append(new_row)
    return Image(img.width, img.height, new_pixels, img.format)


def threshold(img: Image, value: int = 128) -> Image:
    """图像二值化处理。

    将图像转为黑白两色，灰度值大于阈值的为白色，否则为黑色。

    Args:
        img: 输入图像
        value: 二值化阈值，0-255，默认128

    Returns:
        二值化图像（新Image对象）
    """
    value = max(0, min(255, value))
    new_pixels: List[List[Pixel]] = []
    for row in img.pixels:
        new_row: List[Pixel] = []
        for pixel in row:
            # 计算灰度值
            gray = int(0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b)
            # 二值化
            bw = 255 if gray >= value else 0
            new_row.append(Pixel(bw, bw, bw, pixel.a))
        new_pixels.append(new_row)
    return Image(img.width, img.height, new_pixels, img.format)


def sepia(img: Image) -> Image:
    """复古色调滤镜。

    将图像转换为棕褐色（sepia）色调。

    转换公式：
    - new_r = 0.393 * r + 0.769 * g + 0.189 * b
    - new_g = 0.349 * r + 0.686 * g + 0.168 * b
    - new_b = 0.272 * r + 0.534 * g + 0.131 * b

    Args:
        img: 输入图像

    Returns:
        复古色调图像（新Image对象）
    """
    new_pixels: List[List[Pixel]] = []
    for row in img.pixels:
        new_row: List[Pixel] = []
        for pixel in row:
            new_r = int(0.393 * pixel.r + 0.769 * pixel.g + 0.189 * pixel.b)
            new_g = int(0.349 * pixel.r + 0.686 * pixel.g + 0.168 * pixel.b)
            new_b = int(0.272 * pixel.r + 0.534 * pixel.g + 0.131 * pixel.b)
            new_row.append(Pixel(
                max(0, min(255, new_r)),
                max(0, min(255, new_g)),
                max(0, min(255, new_b)),
                pixel.a
            ))
        new_pixels.append(new_row)
    return Image(img.width, img.height, new_pixels, img.format)

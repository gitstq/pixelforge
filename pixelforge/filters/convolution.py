# -*- coding: utf-8 -*-
"""
卷积滤镜

使用卷积核实现图像处理效果，包括模糊、锐化、边缘检测和浮雕效果。
卷积操作对图像的每个像素应用一个权重矩阵（卷积核）。
"""

from __future__ import annotations

from typing import List, Tuple

from pixelforge.core.image import Image, Pixel


# 预定义卷积核
KERNELS = {
    # 3x3 均值模糊核
    "blur_3": [
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9],
    ],
    # 5x5 均值模糊核
    "blur_5": [
        [1/25, 1/25, 1/25, 1/25, 1/25],
        [1/25, 1/25, 1/25, 1/25, 1/25],
        [1/25, 1/25, 1/25, 1/25, 1/25],
        [1/25, 1/25, 1/25, 1/25, 1/25],
        [1/25, 1/25, 1/25, 1/25, 1/25],
    ],
    # 高斯模糊核（3x3近似）
    "gaussian_3": [
        [1/16, 2/16, 1/16],
        [2/16, 4/16, 2/16],
        [1/16, 2/16, 1/16],
    ],
    # 锐化核
    "sharpen": [
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0],
    ],
    # 边缘检测核（Laplacian）
    "edge_detect": [
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1],
    ],
    # 浮雕核
    "emboss": [
        [-2, -1,  0],
        [-1,  1,  1],
        [ 0,  1,  2],
    ],
}


def _apply_kernel(img: Image, kernel: List[List[float]]) -> Image:
    """对图像应用卷积核。

    边界像素使用边缘扩展（edge extension）处理。

    Args:
        img: 输入图像
        kernel: 卷积核矩阵（奇数尺寸的方阵）

    Returns:
        卷积处理后的图像（新Image对象）
    """
    k_size = len(kernel)
    k_half = k_size // 2

    new_pixels: List[List[Pixel]] = []

    for y in range(img.height):
        new_row: List[Pixel] = []
        for x in range(img.width):
            r_sum = 0.0
            g_sum = 0.0
            b_sum = 0.0

            # 应用卷积核
            for ky in range(k_size):
                for kx in range(k_size):
                    # 计算源像素坐标（边界扩展）
                    src_x = max(0, min(img.width - 1, x + kx - k_half))
                    src_y = max(0, min(img.height - 1, y + ky - k_half))

                    weight = kernel[ky][kx]
                    src_pixel = img.pixels[src_y][src_x]

                    r_sum += src_pixel.r * weight
                    g_sum += src_pixel.g * weight
                    b_sum += src_pixel.b * weight

            # 限制到0-255范围
            new_row.append(Pixel(
                max(0, min(255, int(r_sum))),
                max(0, min(255, int(g_sum))),
                max(0, min(255, int(b_sum))),
                img.pixels[y][x].a
            ))
        new_pixels.append(new_row)

    return Image(img.width, img.height, new_pixels, img.format)


def blur(img: Image, radius: int = 1) -> Image:
    """模糊滤镜。

    使用均值模糊或高斯模糊对图像进行模糊处理。

    Args:
        img: 输入图像
        radius: 模糊半径，1=3x3核，2=5x5核

    Returns:
        模糊后的图像（新Image对象）

    Raises:
        ValueError: 不支持的模糊半径
    """
    if radius == 1:
        kernel = KERNELS["gaussian_3"]
    elif radius == 2:
        kernel = KERNELS["blur_5"]
    else:
        raise ValueError(f"不支持的模糊半径: {radius}，可选: 1, 2")

    return _apply_kernel(img, kernel)


def sharpen(img: Image) -> Image:
    """锐化滤镜。

    使用拉普拉斯锐化核增强图像边缘。

    Args:
        img: 输入图像

    Returns:
        锐化后的图像（新Image对象）
    """
    return _apply_kernel(img, KERNELS["sharpen"])


def edge_detect(img: Image) -> Image:
    """边缘检测滤镜。

    使用拉普拉斯算子检测图像边缘。

    Args:
        img: 输入图像

    Returns:
        边缘检测结果（新Image对象）
    """
    return _apply_kernel(img, KERNELS["edge_detect"])


def emboss(img: Image) -> Image:
    """浮雕效果滤镜。

    使用浮雕卷积核创建立体浮雕效果。

    Args:
        img: 输入图像

    Returns:
        浮雕效果图像（新Image对象）
    """
    return _apply_kernel(img, KERNELS["emboss"])

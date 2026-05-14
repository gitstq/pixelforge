# -*- coding: utf-8 -*-
"""
图像元数据处理器

提供图像信息获取、元数据去除和图像哈希计算功能。
"""

from __future__ import annotations

import hashlib
import os
from typing import Optional


def get_info(img, file_path: Optional[str] = None) -> dict:
    """获取图像详细信息。

    Args:
        img: Image对象
        file_path: 图像文件路径（可选，用于获取文件大小）

    Returns:
        包含图像信息的字典
    """
    info = {
        "width": img.width,
        "height": img.height,
        "format": img.format,
        "total_pixels": img.width * img.height,
        "has_alpha": False,
    }

    # 文件大小
    if file_path and os.path.exists(file_path):
        info["file_size"] = os.path.getsize(file_path)
        info["file_size_str"] = _format_size(info["file_size"])
        info["file_name"] = os.path.basename(file_path)

    # 颜色统计
    r_sum = 0
    g_sum = 0
    b_sum = 0
    a_sum = 0
    min_brightness = 255
    max_brightness = 0
    brightness_sum = 0

    for row in img.pixels:
        for pixel in row:
            r_sum += pixel.r
            g_sum += pixel.g
            b_sum += pixel.b
            a_sum += pixel.a

            gray = int(0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b)
            brightness_sum += gray
            min_brightness = min(min_brightness, gray)
            max_brightness = max(max_brightness, gray)

            if pixel.a < 255:
                info["has_alpha"] = True

    total = img.width * img.height
    info["avg_color"] = (
        r_sum // total,
        g_sum // total,
        b_sum // total,
    )
    info["avg_brightness"] = brightness_sum / total
    info["min_brightness"] = min_brightness
    info["max_brightness"] = max_brightness
    info["aspect_ratio"] = _simplify_ratio(img.width, img.height)

    return info


def strip_metadata(img) -> object:
    """去除图像元数据。

    创建图像的副本，清除所有元数据信息。

    Args:
        img: Image对象

    Returns:
        清除元数据后的新Image对象
    """
    result = img.copy()
    result.metadata = {}
    return result


def calculate_hash(img, algorithm: str = "md5") -> str:
    """计算图像内容的哈希值。

    基于图像像素数据计算哈希，相同内容的图像会产生相同的哈希值。

    Args:
        img: Image对象
        algorithm: 哈希算法，可选 'md5', 'sha1', 'sha256'

    Returns:
        哈希值的十六进制字符串

    Raises:
        ValueError: 不支持的哈希算法
    """
    algorithm = algorithm.lower()
    if algorithm not in ("md5", "sha1", "sha256"):
        raise ValueError(
            f"不支持的哈希算法: {algorithm}，可选: md5, sha1, sha256"
        )

    hasher = hashlib.new(algorithm)
    # 使用像素数据计算哈希
    for row in img.pixels:
        for pixel in row:
            hasher.update(bytes([pixel.r, pixel.g, pixel.b, pixel.a]))

    return hasher.hexdigest()


def _format_size(size_bytes: int) -> str:
    """将字节数格式化为可读的文件大小字符串。

    Args:
        size_bytes: 字节数

    Returns:
        格式化后的字符串，如 '1.5 MB'
    """
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def _simplify_ratio(w: int, h: int) -> str:
    """简化宽高比为字符串。

    Args:
        w: 宽度
        h: 高度

    Returns:
        简化后的比例字符串，如 '16:9'
    """
    if h == 0:
        return "0:0"

    def gcd(a: int, b: int) -> int:
        """计算最大公约数。"""
        while b:
            a, b = b, a % b
        return a

    d = gcd(w, h)
    return f"{w // d}:{h // d}"

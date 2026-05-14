# -*- coding: utf-8 -*-
"""
PPM/PGM/PBM格式读写器

使用Python标准库实现Netpbm格式图像的读取和写入。
支持的格式：
- PPM (P3/P6): RGB真彩色图像
- PGM (P2/P5): 灰度图像
- PBM (P1/P4): 黑白图像

格式说明：
- P1/P2/P3: ASCII文本格式
- P4/P5/P6: 二进制格式
"""

from __future__ import annotations

import os
from typing import List, Tuple

from pixelforge.core.image import Image, Pixel


def _skip_whitespace_and_comments(data: bytes, pos: int) -> int:
    """跳过空白字符和注释。

    Args:
        data: 文件数据
        pos: 当前位置

    Returns:
        跳过后的位置
    """
    while pos < len(data):
        # 跳过空白字符
        if data[pos:pos + 1] in (b" ", b"\t", b"\n", b"\r"):
            pos += 1
        # 跳过注释（从#到行尾）
        elif data[pos:pos + 1] == b"#":
            while pos < len(data) and data[pos:pos + 1] != b"\n":
                pos += 1
        else:
            break
    return pos


def _read_ascii_number(data: bytes, pos: int) -> Tuple[int, int]:
    """从ASCII数据中读取一个整数。

    Args:
        data: 文件数据
        pos: 当前位置

    Returns:
        (数值, 新位置)
    """
    pos = _skip_whitespace_and_comments(data, pos)
    start = pos
    while pos < len(data) and chr(data[pos]).isdigit():
        pos += 1
    if pos == start:
        raise ValueError(f"PPM/PGM/PBM: 位置{pos}处期望数字")
    return int(data[start:pos]), pos


def read_ppm(path: str) -> Image:
    """读取PPM/PGM/PBM文件。

    Args:
        path: PPM/PGM/PBM文件路径

    Returns:
        Image对象

    Raises:
        ValueError: 不支持的格式或文件损坏
        IOError: 文件读取错误
    """
    with open(path, "rb") as f:
        data = f.read()

    if len(data) < 3:
        raise ValueError("文件太小，不是有效的PPM/PGM/PBM文件")

    # 读取魔数
    magic = data[0:2].decode("ascii")

    if magic not in ("P1", "P2", "P3", "P4", "P5", "P6"):
        raise ValueError(f"不支持的格式: {magic}")

    pos = 2

    if magic in ("P1", "P4"):
        # PBM（黑白图像）
        width, pos = _read_ascii_number(data, pos)
        height, pos = _read_ascii_number(data, pos)

        pixels: List[List[Pixel]] = []

        if magic == "P1":
            # ASCII格式
            for y in range(height):
                row: List[Pixel] = []
                for x in range(width):
                    val, pos = _read_ascii_number(data, pos)
                    # PBM中0=白色，1=黑色
                    v = 0 if val == 1 else 255
                    row.append(Pixel(v, v, v, 255))
                pixels.append(row)
        else:
            # P4 二进制格式
            pos = _skip_whitespace_and_comments(data, pos)
            row_bytes = (width + 7) // 8
            for y in range(height):
                row = []
                for x in range(width):
                    byte_idx = pos + y * row_bytes + x // 8
                    bit_idx = 7 - (x % 8)
                    val = (data[byte_idx] >> bit_idx) & 1
                    v = 0 if val == 1 else 255
                    row.append(Pixel(v, v, v, 255))
                pixels.append(row)

        return Image(width, height, pixels, "pbm")

    elif magic in ("P2", "P5"):
        # PGM（灰度图像）
        width, pos = _read_ascii_number(data, pos)
        height, pos = _read_ascii_number(data, pos)
        max_val, pos = _read_ascii_number(data, pos)

        if max_val <= 0:
            raise ValueError(f"无效的最大灰度值: {max_val}")

        pixels = []

        if magic == "P2":
            # ASCII格式
            for y in range(height):
                row: List[Pixel] = []
                for x in range(width):
                    val, pos = _read_ascii_number(data, pos)
                    v = int(val * 255 / max_val)
                    row.append(Pixel(v, v, v, 255))
                pixels.append(row)
        else:
            # P5 二进制格式
            pos = _skip_whitespace_and_comments(data, pos)
            bytes_per_val = 1 if max_val < 256 else 2
            for y in range(height):
                row: List[Pixel] = []
                for x in range(width):
                    if bytes_per_val == 1:
                        v = data[pos]
                        pos += 1
                    else:
                        v = (data[pos] << 8) | data[pos + 1]
                        pos += 2
                    v = int(v * 255 / max_val)
                    row.append(Pixel(v, v, v, 255))
                pixels.append(row)

        return Image(width, height, pixels, "pgm")

    else:
        # P3/P6 - PPM（RGB真彩色图像）
        width, pos = _read_ascii_number(data, pos)
        height, pos = _read_ascii_number(data, pos)
        max_val, pos = _read_ascii_number(data, pos)

        if max_val <= 0:
            raise ValueError(f"无效的最大颜色值: {max_val}")

        pixels = []

        if magic == "P3":
            # ASCII格式
            for y in range(height):
                row: List[Pixel] = []
                for x in range(width):
                    r, pos = _read_ascii_number(data, pos)
                    g, pos = _read_ascii_number(data, pos)
                    b, pos = _read_ascii_number(data, pos)
                    r = int(r * 255 / max_val)
                    g = int(g * 255 / max_val)
                    b = int(b * 255 / max_val)
                    row.append(Pixel(r, g, b, 255))
                pixels.append(row)
        else:
            # P6 二进制格式
            pos = _skip_whitespace_and_comments(data, pos)
            bytes_per_val = 1 if max_val < 256 else 2
            for y in range(height):
                row: List[Pixel] = []
                for x in range(width):
                    if bytes_per_val == 1:
                        r = data[pos]
                        g = data[pos + 1]
                        b = data[pos + 2]
                        pos += 3
                    else:
                        r = (data[pos] << 8) | data[pos + 1]
                        g = (data[pos + 2] << 8) | data[pos + 3]
                        b = (data[pos + 4] << 8) | data[pos + 5]
                        pos += 6
                    r = int(r * 255 / max_val)
                    g = int(g * 255 / max_val)
                    b = int(b * 255 / max_val)
                    row.append(Pixel(r, g, b, 255))
                pixels.append(row)

        return Image(width, height, pixels, "ppm")


def write_ppm(img: Image, path: str) -> None:
    """将图像写入PPM文件（P6二进制格式）。

    Args:
        img: Image对象
        path: 输出文件路径

    Raises:
        IOError: 文件写入错误
    """
    header = f"P6\n{img.width} {img.height}\n255\n".encode("ascii")

    pixel_data = bytearray()
    for row in img.pixels:
        for pixel in row:
            pixel_data.extend([pixel.r, pixel.g, pixel.b])

    with open(path, "wb") as f:
        f.write(header)
        f.write(pixel_data)


def write_pgm(img: Image, path: str) -> None:
    """将图像写入PGM文件（P5二进制格式）。

    先将图像转为灰度，再保存。

    Args:
        img: Image对象
        path: 输出文件路径

    Raises:
        IOError: 文件写入错误
    """
    header = f"P5\n{img.width} {img.height}\n255\n".encode("ascii")

    pixel_data = bytearray()
    for row in img.pixels:
        for pixel in row:
            # 使用标准灰度公式
            gray = int(0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b)
            pixel_data.append(gray)

    with open(path, "wb") as f:
        f.write(header)
        f.write(pixel_data)


def write_pbm(img: Image, path: str) -> None:
    """将图像写入PBM文件（P4二进制格式）。

    先将图像转为黑白（阈值128），再保存。

    Args:
        img: Image对象
        path: 输出文件路径

    Raises:
        IOError: 文件写入错误
    """
    header = f"P4\n{img.width} {img.height}\n".encode("ascii")

    row_bytes = (img.width + 7) // 8
    pixel_data = bytearray()

    for row in img.pixels:
        byte_val = 0
        for x in range(img.width):
            pixel = row[x]
            gray = int(0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b)
            # PBM中1=黑色，0=白色
            if gray < 128:
                byte_val |= (1 << (7 - (x % 8)))
            if x % 8 == 7 or x == img.width - 1:
                pixel_data.append(byte_val)
                byte_val = 0

    with open(path, "wb") as f:
        f.write(header)
        f.write(pixel_data)

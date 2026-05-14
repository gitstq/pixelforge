# -*- coding: utf-8 -*-
"""
BMP格式读写器

使用Python标准库（struct）实现BMP文件的读取和写入。
支持24位和32位BMP格式。

BMP文件结构：
- 文件头（14字节）：'BM'标识、文件大小、保留字段、像素数据偏移
- 信息头（40字节）：信息头大小、宽高、位平面数、位深度、压缩方式等
- 可选调色板
- 像素数据（按行存储，每行4字节对齐，从下到上）
"""

from __future__ import annotations

import struct
from typing import List

from pixelforge.core.image import Image, Pixel


def read_bmp(path: str) -> Image:
    """读取BMP文件。

    Args:
        path: BMP文件路径

    Returns:
        Image对象

    Raises:
        ValueError: 不支持的BMP格式或文件损坏
        IOError: 文件读取错误
    """
    with open(path, "rb") as f:
        data = f.read()

    if len(data) < 54:
        raise ValueError("BMP文件太小，不是有效的BMP文件")

    # 解析文件头（14字节）
    file_type = data[0:2]
    if file_type != b"BM":
        raise ValueError(f"不是有效的BMP文件：文件标识为 {file_type!r}")

    pixel_offset = struct.unpack_from("<I", data, 10)[0]

    # 解析信息头
    header_size = struct.unpack_from("<I", data, 14)[0]

    if header_size == 40:
        # BITMAPINFOHEADER（标准40字节信息头）
        width = struct.unpack_from("<i", data, 18)[0]
        height = struct.unpack_from("<i", data, 22)[0]
        bit_planes = struct.unpack_from("<H", data, 26)[0]
        bits_per_pixel = struct.unpack_from("<H", data, 28)[0]
        compression = struct.unpack_from("<I", data, 30)[0]
        # image_size = struct.unpack_from("<I", data, 34)[0]
        # x_ppm = struct.unpack_from("<i", data, 38)[0]
        # y_ppm = struct.unpack_from("<i", data, 42)[0]
        # colors_used = struct.unpack_from("<I", data, 46)[0]
        # colors_important = struct.unpack_from("<I", data, 50)[0]
    else:
        raise ValueError(f"不支持的BMP信息头大小: {header_size}")

    if bit_planes != 1:
        raise ValueError(f"不支持的位平面数: {bit_planes}")

    if bits_per_pixel not in (1, 4, 8, 16, 24, 32):
        raise ValueError(f"不支持的BMP位深度: {bits_per_pixel}")

    if compression != 0:
        raise ValueError(f"不支持的BMP压缩方式: {compression}")

    # 处理高度方向（BMP高度可以为负值表示从上到下存储）
    top_down = height < 0
    abs_height = abs(height)

    # 计算每行字节数（BMP每行需要4字节对齐）
    row_bytes = ((width * bits_per_pixel + 31) // 32) * 4

    # 解析调色板（如果有）
    palette: List[tuple] = []
    if bits_per_pixel <= 8:
        # 调色板位于信息头之后、像素数据之前
        palette_offset = 14 + header_size
        palette_size = pixel_offset - palette_offset
        num_colors = palette_size // 4
        for i in range(num_colors):
            b = data[palette_offset + i * 4]
            g = data[palette_offset + i * 4 + 1]
            r = data[palette_offset + i * 4 + 2]
            # alpha = data[palette_offset + i * 4 + 3]  # 通常为0
            palette.append((r, g, b))

    # 解析像素数据
    pixels: List[List[Pixel]] = []

    for y in range(abs_height):
        # BMP从下到上存储（除非高度为负值）
        if top_down:
            row_idx = y
        else:
            row_idx = abs_height - 1 - y

        row_offset = pixel_offset + row_idx * row_bytes
        row_data = data[row_offset:row_offset + row_bytes]

        row_pixels: List[Pixel] = []

        if bits_per_pixel == 24:
            # 24位BMP：BGR顺序
            for x in range(width):
                offset = x * 3
                b = row_data[offset]
                g = row_data[offset + 1]
                r = row_data[offset + 2]
                row_pixels.append(Pixel(r, g, b, 255))

        elif bits_per_pixel == 32:
            # 32位BMP：BGRA顺序
            for x in range(width):
                offset = x * 4
                b = row_data[offset]
                g = row_data[offset + 1]
                r = row_data[offset + 2]
                a = row_data[offset + 3]
                row_pixels.append(Pixel(r, g, b, a))

        elif bits_per_pixel == 8:
            # 8位索引色
            for x in range(width):
                idx = row_data[x]
                if idx < len(palette):
                    r, g, b = palette[idx]
                else:
                    r, g, b = 0, 0, 0
                row_pixels.append(Pixel(r, g, b, 255))

        elif bits_per_pixel == 4:
            # 4位索引色
            for x in range(width):
                byte_idx = x // 2
                if x % 2 == 0:
                    idx = (row_data[byte_idx] >> 4) & 0x0F
                else:
                    idx = row_data[byte_idx] & 0x0F
                if idx < len(palette):
                    r, g, b = palette[idx]
                else:
                    r, g, b = 0, 0, 0
                row_pixels.append(Pixel(r, g, b, 255))

        elif bits_per_pixel == 1:
            # 1位黑白
            for x in range(width):
                byte_idx = x // 8
                bit_idx = 7 - (x % 8)
                idx = (row_data[byte_idx] >> bit_idx) & 1
                if idx < len(palette):
                    r, g, b = palette[idx]
                else:
                    # 默认黑白调色板
                    r, g, b = (255, 255, 255) if idx == 0 else (0, 0, 0)
                row_pixels.append(Pixel(r, g, b, 255))

        elif bits_per_pixel == 16:
            # 16位高彩色（RGB565或RGB555）
            for x in range(width):
                offset = x * 2
                pixel_val = struct.unpack_from("<H", row_data, offset)[0]
                # 尝试RGB565格式
                r = ((pixel_val >> 11) & 0x1F) * 255 // 31
                g = ((pixel_val >> 5) & 0x3F) * 255 // 63
                b = (pixel_val & 0x1F) * 255 // 31
                row_pixels.append(Pixel(r, g, b, 255))

        pixels.append(row_pixels)

    return Image(width, abs_height, pixels, "bmp")


def write_bmp(img: Image, path: str) -> None:
    """将图像写入BMP文件（24位格式）。

    Args:
        img: Image对象
        path: 输出文件路径

    Raises:
        IOError: 文件写入错误
    """
    width = img.width
    height = img.height

    # 每行字节数（4字节对齐）
    row_bytes = ((width * 3 + 3) // 4) * 4
    padding = row_bytes - width * 3

    # 像素数据大小
    pixel_data_size = row_bytes * height

    # 文件总大小
    file_size = 54 + pixel_data_size

    # 构建文件头（14字节）
    file_header = struct.pack(
        "<2sIHHI",
        b"BM",          # 文件标识
        file_size,      # 文件大小
        0,              # 保留字段1
        0,              # 保留字段2
        54              # 像素数据偏移
    )

    # 构建信息头（40字节）
    info_header = struct.pack(
        "<IiiHHIIiiII",
        40,             # 信息头大小
        width,          # 宽度
        height,         # 高度（正值=从下到上）
        1,              # 位平面数
        24,             # 位深度
        0,              # 压缩方式（无压缩）
        pixel_data_size,  # 图像数据大小
        2835,           # 水平分辨率（72 DPI）
        2835,           # 垂直分辨率（72 DPI）
        0,              # 使用的颜色数
        0               # 重要的颜色数
    )

    # 构建像素数据（BMP从下到上存储，BGR顺序）
    pixel_data = bytearray()
    for y in range(height - 1, -1, -1):
        for x in range(width):
            pixel = img.pixels[y][x]
            pixel_data.extend([pixel.b, pixel.g, pixel.r])  # BGR顺序
        # 行末填充
        pixel_data.extend(b"\x00" * padding)

    # 写入文件
    with open(path, "wb") as f:
        f.write(file_header)
        f.write(info_header)
        f.write(pixel_data)

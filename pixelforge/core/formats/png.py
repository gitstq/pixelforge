# -*- coding: utf-8 -*-
"""
PNG格式读写器

使用Python标准库（struct, zlib）实现PNG文件的读取和写入。
支持RGBA真彩色图像（8位深度）。

PNG文件结构：
- 8字节签名: \\x89PNG\\r\\n\\x1a\\n
- IHDR chunk: 图像头信息
- 可选chunk: PLTE, tEXt, etc.
- IDAT chunk(s): 压缩的图像数据
- IEND chunk: 文件结束标记

每个chunk结构：
- 4字节长度（数据部分）
- 4字节类型
- N字节数据
- 4字节CRC32校验（类型+数据）
"""

from __future__ import annotations

import struct
import zlib
from typing import Optional

from pixelforge.core.image import Image, Pixel


# PNG文件签名
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# PNG颜色类型
COLOR_TYPE_RGB = 2
COLOR_TYPE_RGBA = 6
COLOR_TYPE_GRAY = 0
COLOR_TYPE_GRAY_ALPHA = 4
COLOR_TYPE_PALETTE = 3

# 支持的颜色类型映射
SUPPORTED_COLOR_TYPES = {
    COLOR_TYPE_RGB: (3, "RGB"),
    COLOR_TYPE_RGBA: (4, "RGBA"),
    COLOR_TYPE_GRAY: (1, "Grayscale"),
    COLOR_TYPE_GRAY_ALPHA: (2, "Grayscale+Alpha"),
    COLOR_TYPE_PALETTE: (1, "Palette"),
}


def _make_chunk(chunk_type: bytes, data: bytes) -> bytes:
    """构造PNG chunk。

    Args:
        chunk_type: 4字节chunk类型标识
        data: chunk数据

    Returns:
        完整的chunk字节序列（含长度、类型、数据、CRC）
    """
    chunk_len = struct.pack(">I", len(data))
    crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    return chunk_len + chunk_type + data + crc


def _read_chunk(file_obj) -> tuple:
    """从文件对象读取一个PNG chunk。

    Args:
        file_obj: 文件对象（二进制模式）

    Returns:
        (chunk_type, chunk_data) 元组

    Raises:
        ValueError: 文件格式错误
    """
    # 读取chunk长度（4字节，大端序）
    length_data = file_obj.read(4)
    if len(length_data) < 4:
        raise ValueError("PNG文件不完整：无法读取chunk长度")
    length = struct.unpack(">I", length_data)[0]

    # 读取chunk类型（4字节）
    chunk_type = file_obj.read(4)
    if len(chunk_type) < 4:
        raise ValueError("PNG文件不完整：无法读取chunk类型")

    # 读取chunk数据
    chunk_data = file_obj.read(length)
    if len(chunk_data) < length:
        raise ValueError(f"PNG文件不完整：chunk {chunk_type} 数据不足")

    # 读取并验证CRC（4字节）
    crc_data = file_obj.read(4)
    if len(crc_data) < 4:
        raise ValueError("PNG文件不完整：无法读取CRC")
    expected_crc = struct.unpack(">I", crc_data)[0]
    actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF

    if expected_crc != actual_crc:
        raise ValueError(
            f"PNG CRC校验失败：chunk {chunk_type.decode('ascii', errors='replace')}，"
            f"期望CRC={expected_crc:#010x}，实际CRC={actual_crc:#010x}"
        )

    return chunk_type, chunk_data


def read_png(path: str) -> Image:
    """读取PNG文件。

    Args:
        path: PNG文件路径

    Returns:
        Image对象

    Raises:
        ValueError: 不支持的PNG格式或文件损坏
        IOError: 文件读取错误
    """
    with open(path, "rb") as f:
        # 验证PNG签名
        signature = f.read(8)
        if signature != PNG_SIGNATURE:
            raise ValueError("不是有效的PNG文件：签名不匹配")

        # 解析chunk
        width = 0
        height = 0
        bit_depth = 0
        color_type = 0
        idat_data = bytearray()
        palette: Optional[list] = None

        while True:
            chunk_type, chunk_data = _read_chunk(f)

            if chunk_type == b"IHDR":
                # 图像头chunk
                if len(chunk_data) != 13:
                    raise ValueError("IHDR chunk数据长度错误")
                width, height, bit_depth, color_type, \
                    compression, filter_method, interlace = struct.unpack(
                        ">IIBBBBB", chunk_data
                    )
                # 验证参数
                if bit_depth not in (1, 2, 4, 8, 16):
                    raise ValueError(f"不支持的位深度: {bit_depth}")
                if color_type not in SUPPORTED_COLOR_TYPES:
                    raise ValueError(f"不支持的颜色类型: {color_type}")
                if compression != 0:
                    raise ValueError(f"不支持的压缩方法: {compression}")
                if filter_method != 0:
                    raise ValueError(f"不支持的过滤方法: {filter_method}")

            elif chunk_type == b"PLTE":
                # 调色板chunk
                if len(chunk_data) % 3 != 0:
                    raise ValueError("PLTE chunk数据长度错误")
                palette = []
                for i in range(0, len(chunk_data), 3):
                    palette.append((
                        chunk_data[i],
                        chunk_data[i + 1],
                        chunk_data[i + 2]
                    ))

            elif chunk_type == b"IDAT":
                # 图像数据chunk（可能有多个IDAT）
                idat_data.extend(chunk_data)

            elif chunk_type == b"IEND":
                # 文件结束
                break

            # 其他chunk（如tEXt, gAMA等）暂时忽略

        if width == 0 or height == 0:
            raise ValueError("PNG文件缺少有效的IHDR chunk")

        # 解压缩IDAT数据
        try:
            raw_data = zlib.decompress(bytes(idat_data))
        except zlib.error as e:
            raise ValueError(f"PNG数据解压失败: {e}")

        # 根据颜色类型解析像素数据
        channels, color_name = SUPPORTED_COLOR_TYPES[color_type]
        bytes_per_pixel = max(1, (bit_depth * channels + 7) // 8)

        # 计算每行字节数（包含1字节过滤类型前缀）
        if bit_depth < 8:
            # 低位深：每行按位打包
            row_bytes = (width * bit_depth * channels + 7) // 8
        else:
            row_bytes = width * bytes_per_pixel

        pixels: list[list[Pixel]] = []
        offset = 0

        for y in range(height):
            # 读取过滤类型
            if offset >= len(raw_data):
                raise ValueError(f"PNG数据不完整：第{y}行")
            filter_type = raw_data[offset]
            offset += 1

            # 读取当前行原始数据
            if offset + row_bytes > len(raw_data):
                raise ValueError(f"PNG数据不完整：第{y}行数据不足")
            row_raw = raw_data[offset:offset + row_bytes]
            offset += row_bytes

            # 解码过滤
            scanline = _apply_filter(filter_type, row_raw, pixels, y,
                                     bytes_per_pixel, row_bytes)

            # 解析像素
            row_pixels = _parse_scanline(scanline, width, bit_depth,
                                         color_type, channels, palette)
            pixels.append(row_pixels)

    img = Image(width, height, pixels, "png")
    return img


def _apply_filter(filter_type: int, row_raw: bytes,
                  prev_pixels: list, y: int,
                  bytes_per_pixel: int, row_bytes: int) -> bytearray:
    """应用PNG行过滤并还原原始数据。

    PNG使用差分编码减少压缩数据量，每行有一个过滤类型字节。

    Args:
        filter_type: 过滤类型 (0-4)
        row_raw: 当前行过滤后的原始数据
        prev_pixels: 之前已解码的像素行列表
        y: 当前行号
        bytes_per_pixel: 每像素字节数
        row_bytes: 每行总字节数

    Returns:
        还原后的行数据
    """
    row = bytearray(row_raw)

    # 获取上一行已解码的数据
    if y > 0 and prev_pixels:
        # 从上一行像素重建原始字节
        prev_row = bytearray()
        for pixel in prev_pixels[y - 1]:
            prev_row.extend([pixel.r, pixel.g, pixel.b, pixel.a])
        prev_row = prev_row[:row_bytes]
    else:
        prev_row = bytearray(row_bytes)

    if filter_type == 0:
        # None过滤：数据不变
        pass

    elif filter_type == 1:
        # Sub过滤：与左边像素差值
        for i in range(bytes_per_pixel, row_bytes):
            row[i] = (row[i] + row[i - bytes_per_pixel]) & 0xFF

    elif filter_type == 2:
        # Up过滤：与上方像素差值
        for i in range(row_bytes):
            row[i] = (row[i] + prev_row[i]) & 0xFF

    elif filter_type == 3:
        # Average过滤：与左上方像素平均值差值
        for i in range(row_bytes):
            left = row[i - bytes_per_pixel] if i >= bytes_per_pixel else 0
            up = prev_row[i]
            row[i] = (row[i] + (left + up) // 2) & 0xFF

    elif filter_type == 4:
        # Paeth过滤：与Paeth预测值差值
        for i in range(row_bytes):
            left = row[i - bytes_per_pixel] if i >= bytes_per_pixel else 0
            up = prev_row[i]
            up_left = (prev_row[i - bytes_per_pixel]
                       if i >= bytes_per_pixel else 0)
            row[i] = (row[i] + _paeth_predictor(left, up, up_left)) & 0xFF

    else:
        raise ValueError(f"未知的PNG过滤类型: {filter_type}")

    return row


def _paeth_predictor(a: int, b: int, c: int) -> int:
    """Paeth预测器函数。

    Args:
        a: 左边像素值
        b: 上方像素值
        c: 左上方像素值

    Returns:
        预测值
    """
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)

    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    else:
        return c


def _parse_scanline(scanline: bytearray, width: int, bit_depth: int,
                    color_type: int, channels: int,
                    palette: Optional[list]) -> list:
    """将解码后的扫描行数据解析为像素列表。

    Args:
        scanline: 解码后的行数据
        width: 图像宽度
        bit_depth: 位深度
        color_type: 颜色类型
        channels: 通道数
        palette: 调色板（如果有）

    Returns:
        像素列表
    """
    pixels = []

    if color_type == COLOR_TYPE_RGBA:
        # RGBA真彩色
        for x in range(width):
            offset = x * 4
            r = scanline[offset]
            g = scanline[offset + 1]
            b = scanline[offset + 2]
            a = scanline[offset + 3]
            pixels.append(Pixel(r, g, b, a))

    elif color_type == COLOR_TYPE_RGB:
        # RGB真彩色（无alpha）
        for x in range(width):
            offset = x * 3
            r = scanline[offset]
            g = scanline[offset + 1]
            b = scanline[offset + 2]
            pixels.append(Pixel(r, g, b, 255))

    elif color_type == COLOR_TYPE_GRAY:
        # 灰度图像
        if bit_depth == 8:
            for x in range(width):
                v = scanline[x]
                pixels.append(Pixel(v, v, v, 255))
        elif bit_depth == 16:
            for x in range(width):
                offset = x * 2
                v = (scanline[offset] << 8) | scanline[offset + 1]
                v = v >> 8  # 缩放到8位
                pixels.append(Pixel(v, v, v, 255))
        else:
            # 低位深灰度（1/2/4位）
            pixels_per_byte = 8 // bit_depth
            mask = (1 << bit_depth) - 1
            for x in range(width):
                byte_idx = x // pixels_per_byte
                bit_idx = pixels_per_byte - 1 - (x % pixels_per_byte)
                v = (scanline[byte_idx] >> (bit_idx * bit_depth)) & mask
                # 缩放到0-255
                v = v * 255 // ((1 << bit_depth) - 1)
                pixels.append(Pixel(v, v, v, 255))

    elif color_type == COLOR_TYPE_GRAY_ALPHA:
        # 灰度+透明度
        for x in range(width):
            offset = x * 2
            v = scanline[offset]
            a = scanline[offset + 1]
            pixels.append(Pixel(v, v, v, a))

    elif color_type == COLOR_TYPE_PALETTE:
        # 调色板图像
        if palette is None:
            raise ValueError("调色板PNG缺少PLTE chunk")
        if bit_depth == 8:
            for x in range(width):
                idx = scanline[x]
                if idx < len(palette):
                    r, g, b = palette[idx]
                    pixels.append(Pixel(r, g, b, 255))
                else:
                    pixels.append(Pixel(0, 0, 0, 255))
        elif bit_depth < 8:
            pixels_per_byte = 8 // bit_depth
            mask = (1 << bit_depth) - 1
            for x in range(width):
                byte_idx = x // pixels_per_byte
                bit_idx = pixels_per_byte - 1 - (x % pixels_per_byte)
                idx = (scanline[byte_idx] >> (bit_idx * bit_depth)) & mask
                if idx < len(palette):
                    r, g, b = palette[idx]
                    pixels.append(Pixel(r, g, b, 255))
                else:
                    pixels.append(Pixel(0, 0, 0, 255))

    return pixels


def write_png(img: Image, path: str) -> None:
    """将图像写入PNG文件（RGBA格式）。

    Args:
        img: Image对象
        path: 输出文件路径

    Raises:
        IOError: 文件写入错误
    """
    # 构建原始图像数据（每行前加过滤类型字节0=None）
    raw_data = bytearray()

    for y in range(img.height):
        raw_data.append(0)  # 过滤类型: None
        for x in range(img.width):
            pixel = img.pixels[y][x]
            raw_data.extend([pixel.r, pixel.g, pixel.b, pixel.a])

    # 压缩图像数据
    compressed = zlib.compress(bytes(raw_data))

    # 构建IHDR
    ihdr_data = struct.pack(
        ">IIBBBBB",
        img.width,       # 宽度
        img.height,      # 高度
        8,               # 位深度
        COLOR_TYPE_RGBA, # 颜色类型（RGBA）
        0,               # 压缩方法（deflate）
        0,               # 过滤方法（标准）
        0                # 隔行扫描（非隔行）
    )

    # 写入文件
    with open(path, "wb") as f:
        f.write(PNG_SIGNATURE)
        f.write(_make_chunk(b"IHDR", ihdr_data))
        f.write(_make_chunk(b"IDAT", compressed))
        f.write(_make_chunk(b"IEND", b""))

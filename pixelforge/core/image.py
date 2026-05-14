# -*- coding: utf-8 -*-
"""
PixelForge 图像核心数据结构

提供 Pixel 和 Image 类，作为整个图像处理引擎的基础数据结构。
支持从文件加载、保存、缩放、裁剪、旋转、翻转等基本操作。
"""

from __future__ import annotations

import copy
import math
import os
from typing import List, Optional, Tuple


class Pixel:
    """像素数据类，存储RGBA颜色值。

    每个通道的值范围为 0-255。

    Attributes:
        r: 红色通道值 (0-255)
        g: 绿色通道值 (0-255)
        b: 蓝色通道值 (0-255)
        a: 透明度通道值 (0-255)，255表示完全不透明
    """

    __slots__ = ("r", "g", "b", "a")

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 255) -> None:
        """初始化像素。

        Args:
            r: 红色通道值 (0-255)
            g: 绿色通道值 (0-255)
            b: 蓝色通道值 (0-255)
            a: 透明度通道值 (0-255)
        """
        self.r = max(0, min(255, int(r)))
        self.g = max(0, min(255, int(g)))
        self.b = max(0, min(255, int(b)))
        self.a = max(0, min(255, int(a)))

    def __eq__(self, other: object) -> bool:
        """判断两个像素是否相等。"""
        if not isinstance(other, Pixel):
            return NotImplemented
        return (self.r == other.r and self.g == other.g
                and self.b == other.b and self.a == other.a)

    def __repr__(self) -> str:
        """返回像素的字符串表示。"""
        return f"Pixel(r={self.r}, g={self.g}, b={self.b}, a={self.a})"

    def __iter__(self):
        """支持解包操作。"""
        yield self.r
        yield self.g
        yield self.b
        yield self.a

    def to_tuple(self) -> Tuple[int, int, int, int]:
        """返回RGBA元组。"""
        return (self.r, self.g, self.b, self.a)

    def to_rgb(self) -> Tuple[int, int, int]:
        """返回RGB元组（不含透明度）。"""
        return (self.r, self.g, self.b)


class Image:
    """图像核心类，存储二维像素数组并提供基本图像操作。

    Attributes:
        width: 图像宽度（像素）
        height: 图像高度（像素）
        pixels: 二维像素数组，pixels[y][x] 表示第y行第x列的像素
        format: 图像格式标识（如 'png', 'bmp', 'ppm'）
        metadata: 图像元数据字典
    """

    def __init__(self, width: int, height: int,
                 pixels: Optional[List[List[Pixel]]] = None,
                 format: str = "unknown") -> None:
        """初始化图像。

        Args:
            width: 图像宽度
            height: 图像高度
            pixels: 二维像素数组，如果为None则创建全黑图像
            format: 图像格式标识
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"图像尺寸必须为正数，当前: {width}x{height}")
        self.width = width
        self.height = height
        self.format = format
        self.metadata: dict = {}

        if pixels is not None:
            # 验证像素数组尺寸
            if len(pixels) != height:
                raise ValueError(
                    f"像素数组行数({len(pixels)})与高度({height})不匹配"
                )
            for row_idx, row in enumerate(pixels):
                if len(row) != width:
                    raise ValueError(
                        f"第{row_idx}行列数({len(row)})与宽度({width})不匹配"
                    )
            self.pixels = pixels
        else:
            # 创建全黑不透明图像
            self.pixels = [
                [Pixel(0, 0, 0, 255) for _ in range(width)]
                for _ in range(height)
            ]

    @staticmethod
    def from_file(path: str) -> "Image":
        """从文件加载图像，自动检测格式。

        Args:
            path: 图像文件路径

        Returns:
            加载的Image对象

        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 不支持的文件格式
            IOError: 文件读取错误
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"文件不存在: {path}")
        # 延迟导入，避免循环依赖
        from pixelforge.core.formats import load_image
        return load_image(path)

    def save(self, path: str, format: Optional[str] = None) -> None:
        """保存图像到文件。

        Args:
            path: 输出文件路径
            format: 目标格式，如果为None则根据文件扩展名自动检测

        Raises:
            ValueError: 不支持的目标格式
            IOError: 文件写入错误
        """
        # 确保输出目录存在
        output_dir = os.path.dirname(path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 延迟导入，避免循环依赖
        from pixelforge.core.formats import save_image
        save_image(self, path, format)

    def get_pixel(self, x: int, y: int) -> Pixel:
        """获取指定位置的像素。

        Args:
            x: x坐标（列）
            y: y坐标（行）

        Returns:
            该位置的Pixel对象

        Raises:
            IndexError: 坐标超出图像范围
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError(f"坐标({x},{y})超出图像范围({self.width}x{self.height})")
        return self.pixels[y][x]

    def set_pixel(self, x: int, y: int, pixel: Pixel) -> None:
        """设置指定位置的像素。

        Args:
            x: x坐标（列）
            y: y坐标（行）
            pixel: 要设置的像素

        Raises:
            IndexError: 坐标超出图像范围
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError(f"坐标({x},{y})超出图像范围({self.width}x{self.height})")
        self.pixels[y][x] = pixel

    def resize(self, width: int, height: int, method: str = "nearest") -> "Image":
        """缩放图像。

        Args:
            width: 目标宽度
            height: 目标高度
            method: 缩放方法，'nearest'（最近邻）或 'bilinear'（双线性插值）

        Returns:
            缩放后的新Image对象

        Raises:
            ValueError: 不支持的缩放方法
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"目标尺寸必须为正数，当前: {width}x{height}")

        new_pixels: List[List[Pixel]] = []

        if method == "nearest":
            # 最近邻插值
            x_ratio = self.width / width
            y_ratio = self.height / height
            for y in range(height):
                row: List[Pixel] = []
                src_y = int(y * y_ratio)
                src_y = min(src_y, self.height - 1)
                for x in range(width):
                    src_x = int(x * x_ratio)
                    src_x = min(src_x, self.width - 1)
                    row.append(Pixel(*self.pixels[src_y][src_x].to_tuple()))
                new_pixels.append(row)

        elif method == "bilinear":
            # 双线性插值
            x_ratio = self.width / width
            y_ratio = self.height / height
            for y in range(height):
                row = []
                src_y = y * y_ratio
                y0 = int(src_y)
                y1 = min(y0 + 1, self.height - 1)
                fy = src_y - y0
                for x in range(width):
                    src_x = x * x_ratio
                    x0 = int(src_x)
                    x1 = min(x0 + 1, self.width - 1)
                    fx = src_x - x0

                    # 获取四个邻近像素
                    p00 = self.pixels[y0][x0]
                    p01 = self.pixels[y0][x1]
                    p10 = self.pixels[y1][x0]
                    p11 = self.pixels[y1][x1]

                    # 双线性插值计算每个通道
                    r = int(p00.r * (1 - fx) * (1 - fy) + p01.r * fx * (1 - fy)
                            + p10.r * (1 - fx) * fy + p11.r * fx * fy)
                    g = int(p00.g * (1 - fx) * (1 - fy) + p01.g * fx * (1 - fy)
                            + p10.g * (1 - fx) * fy + p11.g * fx * fy)
                    b = int(p00.b * (1 - fx) * (1 - fy) + p01.b * fx * (1 - fy)
                            + p10.b * (1 - fx) * fy + p11.b * fx * fy)
                    a = int(p00.a * (1 - fx) * (1 - fy) + p01.a * fx * (1 - fy)
                            + p10.a * (1 - fx) * fy + p11.a * fx * fy)

                    row.append(Pixel(r, g, b, a))
                new_pixels.append(row)
        else:
            raise ValueError(f"不支持的缩放方法: {method}，可选: nearest, bilinear")

        return Image(width, height, new_pixels, self.format)

    def crop(self, x: int, y: int, w: int, h: int) -> "Image":
        """裁剪图像。

        Args:
            x: 裁剪区域左上角x坐标
            y: 裁剪区域左上角y坐标
            w: 裁剪区域宽度
            h: 裁剪区域高度

        Returns:
            裁剪后的新Image对象

        Raises:
            ValueError: 裁剪区域超出图像范围
        """
        if x < 0 or y < 0 or w <= 0 or h <= 0:
            raise ValueError(f"裁剪参数无效: x={x}, y={y}, w={w}, h={h}")
        if x + w > self.width or y + h > self.height:
            raise ValueError(
                f"裁剪区域({x},{y},{w},{h})超出图像范围({self.width}x{self.height})"
            )

        new_pixels = []
        for row_y in range(y, y + h):
            row = []
            for col_x in range(x, x + w):
                row.append(Pixel(*self.pixels[row_y][col_x].to_tuple()))
            new_pixels.append(row)

        return Image(w, h, new_pixels, self.format)

    def rotate(self, degrees: int) -> "Image":
        """旋转图像（仅支持90度倍数）。

        Args:
            degrees: 旋转角度，支持 90, 180, 270

        Returns:
            旋转后的新Image对象

        Raises:
            ValueError: 不支持的角度值
        """
        degrees = degrees % 360

        if degrees == 0:
            return self.copy()

        if degrees == 90:
            # 顺时针90度：新宽度=旧高度，新高度=旧宽度
            new_w = self.height
            new_h = self.width
            new_pixels = []
            for y in range(new_h):
                row = []
                for x in range(new_w):
                    # 映射: 新(x,y) -> 旧(new_h-1-y, x)
                    row.append(Pixel(*self.pixels[new_h - 1 - y][x].to_tuple()))
                new_pixels.append(row)
            return Image(new_w, new_h, new_pixels, self.format)

        elif degrees == 180:
            # 旋转180度
            new_pixels = []
            for y in range(self.height - 1, -1, -1):
                row = []
                for x in range(self.width - 1, -1, -1):
                    row.append(Pixel(*self.pixels[y][x].to_tuple()))
                new_pixels.append(row)
            return Image(self.width, self.height, new_pixels, self.format)

        elif degrees == 270:
            # 顺时针270度（逆时针90度）
            new_w = self.height
            new_h = self.width
            new_pixels = []
            for y in range(new_h):
                row = []
                for x in range(new_w):
                    # 映射: 新(x,y) -> 旧(y, new_w-1-x)
                    row.append(Pixel(*self.pixels[y][new_w - 1 - x].to_tuple()))
                new_pixels.append(row)
            return Image(new_w, new_h, new_pixels, self.format)

        else:
            raise ValueError(f"仅支持90度倍数旋转，当前: {degrees}度")

    def flip(self, direction: str) -> "Image":
        """翻转图像。

        Args:
            direction: 翻转方向，'horizontal'（水平翻转）或 'vertical'（垂直翻转）

        Returns:
            翻转后的新Image对象

        Raises:
            ValueError: 不支持的翻转方向
        """
        new_pixels = []

        if direction == "horizontal":
            # 水平翻转：每行像素逆序
            for y in range(self.height):
                row = []
                for x in range(self.width - 1, -1, -1):
                    row.append(Pixel(*self.pixels[y][x].to_tuple()))
                new_pixels.append(row)
            return Image(self.width, self.height, new_pixels, self.format)

        elif direction == "vertical":
            # 垂直翻转：行逆序
            for y in range(self.height - 1, -1, -1):
                row = []
                for x in range(self.width):
                    row.append(Pixel(*self.pixels[y][x].to_tuple()))
                new_pixels.append(row)
            return Image(self.width, self.height, new_pixels, self.format)

        else:
            raise ValueError(
                f"不支持的翻转方向: {direction}，可选: horizontal, vertical"
            )

    def copy(self) -> "Image":
        """创建图像的深拷贝。

        Returns:
            新的Image对象，与原图像完全独立
        """
        new_pixels = []
        for row in self.pixels:
            new_row = [Pixel(*p.to_tuple()) for p in row]
            new_pixels.append(new_row)
        img = Image(self.width, self.height, new_pixels, self.format)
        img.metadata = copy.deepcopy(self.metadata)
        return img

    def get_raw_data(self) -> bytes:
        """获取图像原始像素数据（RGB格式，不含alpha）。

        Returns:
            按行优先顺序排列的RGB字节数据
        """
        data = bytearray()
        for row in self.pixels:
            for pixel in row:
                data.extend([pixel.r, pixel.g, pixel.b])
        return bytes(data)

    def get_raw_data_rgba(self) -> bytes:
        """获取图像原始像素数据（RGBA格式）。

        Returns:
            按行优先顺序排列的RGBA字节数据
        """
        data = bytearray()
        for row in self.pixels:
            for pixel in row:
                data.extend([pixel.r, pixel.g, pixel.b, pixel.a])
        return bytes(data)

    @staticmethod
    def from_raw_data(data: bytes, width: int, height: int,
                      channels: int = 3) -> "Image":
        """从原始字节数据创建图像。

        Args:
            data: 原始像素字节数据
            width: 图像宽度
            height: 图像高度
            channels: 通道数，3为RGB，4为RGBA

        Returns:
            新的Image对象

        Raises:
            ValueError: 数据长度与图像尺寸不匹配
        """
        expected_len = width * height * channels
        if len(data) < expected_len:
            raise ValueError(
                f"数据长度({len(data)})不足，期望: {expected_len}"
            )

        pixels: List[List[Pixel]] = []
        offset = 0
        for y in range(height):
            row: List[Pixel] = []
            for x in range(width):
                r = data[offset]
                g = data[offset + 1]
                b = data[offset + 2]
                a = data[offset + 3] if channels == 4 else 255
                row.append(Pixel(r, g, b, a))
                offset += channels
            pixels.append(row)

        return Image(width, height, pixels)

    def __repr__(self) -> str:
        """返回图像的字符串表示。"""
        return (f"Image(width={self.width}, height={self.height}, "
                f"format='{self.format}')")

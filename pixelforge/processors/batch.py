# -*- coding: utf-8 -*-
"""
批量处理器

提供批量图像处理功能，包括批量缩放、格式转换、水印添加和滤镜应用。
"""

from __future__ import annotations

import os
import sys
from typing import Callable, Optional

from pixelforge.core.image import Image
from pixelforge.processors.watermark import add_text_watermark
from pixelforge.utils.progress import ProgressBar


# 支持的图像扩展名
SUPPORTED_EXTENSIONS = {".png", ".bmp", ".ppm", ".pgm", ".pbm", ".pnm"}


def _get_image_files(input_dir: str, pattern: str = "*.png") -> list:
    """获取目录中的图像文件列表。

    Args:
        input_dir: 输入目录
        pattern: 文件匹配模式（简单通配符，支持 * 和 ?）

    Returns:
        排序后的文件路径列表
    """
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"目录不存在: {input_dir}")

    # 简单通配符匹配
    import fnmatch
    files = []
    for filename in os.listdir(input_dir):
        if fnmatch.fnmatch(filename.lower(), pattern.lower()):
            ext = os.path.splitext(filename)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                files.append(os.path.join(input_dir, filename))

    files.sort()
    return files


def _get_output_path(input_path: str, output_dir: str,
                     new_ext: Optional[str] = None) -> str:
    """根据输入路径生成输出路径。

    Args:
        input_path: 输入文件路径
        output_dir: 输出目录
        new_ext: 新的文件扩展名（含点号），如果为None则保持原扩展名

    Returns:
        输出文件路径
    """
    basename = os.path.basename(input_path)
    if new_ext:
        name = os.path.splitext(basename)[0]
        basename = name + new_ext
    return os.path.join(output_dir, basename)


def batch_resize(
    input_dir: str,
    output_dir: str,
    size: tuple,
    pattern: str = "*.png",
    method: str = "nearest"
) -> int:
    """批量缩放图像。

    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        size: 目标尺寸 (width, height)
        pattern: 文件匹配模式
        method: 缩放方法，'nearest' 或 'bilinear'

    Returns:
        成功处理的文件数量
    """
    files = _get_image_files(input_dir, pattern)
    if not files:
        print(f"警告: 在 {input_dir} 中未找到匹配 {pattern} 的图像文件")
        return 0

    os.makedirs(output_dir, exist_ok=True)
    width, height = size
    success_count = 0

    progress = ProgressBar(len(files), "批量缩放")
    for i, filepath in enumerate(files):
        try:
            img = Image.from_file(filepath)
            resized = img.resize(width, height, method)
            output_path = _get_output_path(filepath, output_dir)
            resized.save(output_path)
            success_count += 1
        except Exception as e:
            print(f"\n错误: 处理 {filepath} 失败: {e}", file=sys.stderr)
        progress.update(i + 1)

    progress.finish()
    return success_count


def batch_convert(
    input_dir: str,
    output_dir: str,
    target_format: str,
    pattern: str = "*.png"
) -> int:
    """批量转换图像格式。

    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        target_format: 目标格式（如 'png', 'bmp', 'ppm'）
        pattern: 文件匹配模式

    Returns:
        成功处理的文件数量
    """
    files = _get_image_files(input_dir, pattern)
    if not files:
        print(f"警告: 在 {input_dir} 中未找到匹配 {pattern} 的图像文件")
        return 0

    os.makedirs(output_dir, exist_ok=True)
    ext_map = {
        "png": ".png",
        "bmp": ".bmp",
        "ppm": ".ppm",
        "pgm": ".pgm",
        "pbm": ".pbm",
    }
    new_ext = ext_map.get(target_format.lower(), f".{target_format}")
    success_count = 0

    progress = ProgressBar(len(files), "批量转换")
    for i, filepath in enumerate(files):
        try:
            img = Image.from_file(filepath)
            output_path = _get_output_path(filepath, output_dir, new_ext)
            img.save(output_path, target_format.lower())
            success_count += 1
        except Exception as e:
            print(f"\n错误: 处理 {filepath} 失败: {e}", file=sys.stderr)
        progress.update(i + 1)

    progress.finish()
    return success_count


def batch_watermark(
    input_dir: str,
    output_dir: str,
    watermark_text: str,
    position: str = "bottom-right",
    pattern: str = "*.png",
    opacity: float = 0.5,
    font_size: int = 12
) -> int:
    """批量添加水印。

    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        watermark_text: 水印文本
        position: 水印位置
        pattern: 文件匹配模式
        opacity: 水印透明度
        font_size: 字体大小

    Returns:
        成功处理的文件数量
    """
    files = _get_image_files(input_dir, pattern)
    if not files:
        print(f"警告: 在 {input_dir} 中未找到匹配 {pattern} 的图像文件")
        return 0

    os.makedirs(output_dir, exist_ok=True)
    success_count = 0

    progress = ProgressBar(len(files), "批量水印")
    for i, filepath in enumerate(files):
        try:
            img = Image.from_file(filepath)
            watermarked = add_text_watermark(
                img, watermark_text, position, opacity, font_size
            )
            output_path = _get_output_path(filepath, output_dir)
            watermarked.save(output_path)
            success_count += 1
        except Exception as e:
            print(f"\n错误: 处理 {filepath} 失败: {e}", file=sys.stderr)
        progress.update(i + 1)

    progress.finish()
    return success_count


def batch_filter(
    input_dir: str,
    output_dir: str,
    filter_name: str,
    pattern: str = "*.png",
    **kwargs
) -> int:
    """批量应用滤镜。

    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        filter_name: 滤镜名称，可选：
            grayscale, invert, brightness, contrast, threshold, sepia,
            blur, sharpen, edge_detect, emboss,
            adjust_hue, saturate, color_temperature
        pattern: 文件匹配模式
        **kwargs: 滤镜参数

    Returns:
        成功处理的文件数量
    """
    # 获取滤镜函数
    filter_func = _get_filter_function(filter_name, kwargs)

    files = _get_image_files(input_dir, pattern)
    if not files:
        print(f"警告: 在 {input_dir} 中未找到匹配 {pattern} 的图像文件")
        return 0

    os.makedirs(output_dir, exist_ok=True)
    success_count = 0

    progress = ProgressBar(len(files), f"批量滤镜({filter_name})")
    for i, filepath in enumerate(files):
        try:
            img = Image.from_file(filepath)
            filtered = filter_func(img)
            output_path = _get_output_path(filepath, output_dir)
            filtered.save(output_path)
            success_count += 1
        except Exception as e:
            print(f"\n错误: 处理 {filepath} 失败: {e}", file=sys.stderr)
        progress.update(i + 1)

    progress.finish()
    return success_count


def _get_filter_function(name: str, kwargs: dict) -> Callable:
    """根据名称获取滤镜函数。

    Args:
        name: 滤镜名称
        kwargs: 滤镜参数

    Returns:
        滤镜函数（接受Image参数，返回Image）

    Raises:
        ValueError: 未知的滤镜名称
    """
    from pixelforge.filters.basic import (
        grayscale, invert, brightness, contrast, threshold, sepia
    )
    from pixelforge.filters.convolution import blur, sharpen, edge_detect, emboss
    from pixelforge.filters.color import adjust_hue, saturate, color_temperature

    filters = {
        "grayscale": lambda img: grayscale(img),
        "invert": lambda img: invert(img),
        "brightness": lambda img: brightness(img, kwargs.get("factor", 50)),
        "contrast": lambda img: contrast(img, kwargs.get("factor", 1.5)),
        "threshold": lambda img: threshold(img, kwargs.get("value", 128)),
        "sepia": lambda img: sepia(img),
        "blur": lambda img: blur(img, kwargs.get("radius", 1)),
        "sharpen": lambda img: sharpen(img),
        "edge_detect": lambda img: edge_detect(img),
        "emboss": lambda img: emboss(img),
        "adjust_hue": lambda img: adjust_hue(img, kwargs.get("degrees", 30)),
        "saturate": lambda img: saturate(img, kwargs.get("factor", 1.5)),
        "color_temperature": lambda img: color_temperature(
            img, kwargs.get("value", 30)
        ),
    }

    if name not in filters:
        available = ", ".join(filters.keys())
        raise ValueError(f"未知滤镜: {name}，可选: {available}")

    return filters[name]

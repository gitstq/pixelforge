# -*- coding: utf-8 -*-
"""
格式注册与自动检测模块

管理所有支持的图像格式，提供格式自动检测和统一的加载/保存接口。
"""

from __future__ import annotations

import os
from typing import Callable, Dict, Optional, Tuple

from pixelforge.core.image import Image

# 格式注册表：格式名 -> (读取函数, 写入函数, 扩展名列表)
_FORMAT_REGISTRY: Dict[str, Tuple[Optional[Callable], Optional[Callable], list]] = {}


def register_format(name: str, reader: Optional[Callable] = None,
                    writer: Optional[Callable] = None,
                    extensions: Optional[list] = None) -> None:
    """注册图像格式。

    Args:
        name: 格式名称（小写，如 'png', 'bmp'）
        reader: 读取函数，签名为 f(path) -> Image
        writer: 写入函数，签名为 f(img, path) -> None
        extensions: 关联的文件扩展名列表（不含点号）
    """
    _FORMAT_REGISTRY[name] = (reader, writer, extensions or [])


def get_format_info(name: str) -> Tuple[Optional[Callable], Optional[Callable], list]:
    """获取格式信息。

    Args:
        name: 格式名称

    Returns:
        (读取函数, 写入函数, 扩展名列表)

    Raises:
        ValueError: 格式未注册
    """
    if name not in _FORMAT_REGISTRY:
        raise ValueError(f"未注册的格式: {name}")
    return _FORMAT_REGISTRY[name]


def detect_format(path: str) -> str:
    """根据文件扩展名和文件头自动检测图像格式。

    Args:
        path: 文件路径

    Returns:
        格式名称字符串

    Raises:
        ValueError: 无法检测格式
    """
    ext = os.path.splitext(path)[1].lower()

    # 先通过扩展名匹配
    ext_map = {
        ".png": "png",
        ".bmp": "bmp",
        ".dib": "bmp",
        ".ppm": "ppm",
        ".pgm": "pgm",
        ".pbm": "pbm",
        ".pnm": "ppm",
    }

    if ext in ext_map:
        return ext_map[ext]

    # 扩展名无法识别时，尝试通过文件头检测
    try:
        with open(path, "rb") as f:
            header = f.read(16)

        if header[:8] == b"\x89PNG\r\n\x1a\n":
            return "png"
        elif header[:2] == b"BM":
            return "bmp"
        elif header[:2] in (b"P1", b"P2", b"P3", b"P4", b"P5", b"P6"):
            magic = header[:2].decode("ascii")
            format_map = {"P1": "pbm", "P2": "pgm", "P3": "ppm",
                          "P4": "pbm", "P5": "pgm", "P6": "ppm"}
            return format_map.get(magic, "unknown")
        elif header[:2] == b"\xff\xd8":
            # JPEG文件头
            return "jpeg"
    except (IOError, OSError):
        pass

    raise ValueError(f"无法检测文件格式: {path}")


def load_image(path: str) -> Image:
    """加载图像文件，自动检测格式。

    Args:
        path: 图像文件路径

    Returns:
        Image对象

    Raises:
        ValueError: 不支持的格式
        FileNotFoundError: 文件不存在
    """
    fmt = detect_format(path)

    # PPM/PGM/PBM统一使用ppm模块
    if fmt in ("ppm", "pgm", "pbm"):
        from pixelforge.core.formats.ppm import read_ppm
        return read_ppm(path)

    if fmt not in _FORMAT_REGISTRY:
        raise ValueError(f"不支持的图像格式: {fmt}")

    reader, _, _ = _FORMAT_REGISTRY[fmt]
    if reader is None:
        raise ValueError(f"格式 {fmt} 不支持读取")

    return reader(path)


def save_image(img: Image, path: str, format: Optional[str] = None) -> None:
    """保存图像文件。

    Args:
        img: Image对象
        path: 输出文件路径
        format: 目标格式，如果为None则自动检测

    Raises:
        ValueError: 不支持的目标格式
    """
    if format is None:
        format = detect_format(path)

    # PPM/PGM/PBM统一使用ppm模块
    if format in ("ppm", "pgm", "pbm"):
        from pixelforge.core.formats.ppm import write_ppm, write_pgm, write_pbm
        if format == "ppm":
            write_ppm(img, path)
        elif format == "pgm":
            write_pgm(img, path)
        elif format == "pbm":
            write_pbm(img, path)
        return

    if format not in _FORMAT_REGISTRY:
        raise ValueError(f"不支持的图像格式: {format}")

    _, writer, _ = _FORMAT_REGISTRY[format]
    if writer is None:
        raise ValueError(f"格式 {format} 不支持写入")

    writer(img, path)


def get_supported_formats() -> list:
    """获取所有支持的格式列表。

    Returns:
        格式名称列表
    """
    return list(_FORMAT_REGISTRY.keys())


def get_supported_extensions() -> list:
    """获取所有支持的文件扩展名列表。

    Returns:
        扩展名列表（含点号）
    """
    extensions = []
    for _, _, exts in _FORMAT_REGISTRY.values():
        for ext in exts:
            extensions.append(f".{ext}")
    return extensions


# 注册内置格式
def _register_builtin_formats() -> None:
    """注册所有内置图像格式。"""
    # 延迟导入，避免循环引用
    from pixelforge.core.formats.png import read_png, write_png
    from pixelforge.core.formats.bmp import read_bmp, write_bmp
    from pixelforge.core.formats.ppm import read_ppm, write_ppm

    register_format("png", reader=read_png, writer=write_png,
                    extensions=["png"])
    register_format("bmp", reader=read_bmp, writer=write_bmp,
                    extensions=["bmp", "dib"])
    register_format("ppm", reader=read_ppm, writer=write_ppm,
                    extensions=["ppm", "pnm"])
    register_format("pgm", reader=read_ppm, writer=None,
                    extensions=["pgm"])
    register_format("pbm", reader=read_ppm, writer=None,
                    extensions=["pbm"])


# 模块加载时自动注册内置格式
_register_builtin_formats()

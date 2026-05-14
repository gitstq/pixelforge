# -*- coding: utf-8 -*-
"""
颜色工具模块

提供颜色格式转换和颜色混合功能。
"""

from __future__ import annotations

from typing import Tuple


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """将十六进制颜色字符串转换为RGB元组。

    支持的格式：'#RRGGBB', 'RRGGBB', '#RGB', 'RGB'

    Args:
        hex_str: 十六进制颜色字符串

    Returns:
        (r, g, b) 元组，每个值0-255

    Raises:
        ValueError: 无效的颜色字符串

    Examples:
        >>> hex_to_rgb('#FF0000')
        (255, 0, 0)
        >>> hex_to_rgb('00FF00')
        (0, 255, 0)
        >>> hex_to_rgb('#F00')
        (255, 0, 0)
    """
    hex_str = hex_str.strip()

    # 去除前导 '#'
    if hex_str.startswith("#"):
        hex_str = hex_str[1:]

    # 处理缩写格式 (#RGB)
    if len(hex_str) == 3:
        hex_str = (
            hex_str[0] * 2 + hex_str[1] * 2 + hex_str[2] * 2
        )

    if len(hex_str) != 6:
        raise ValueError(
            f"无效的颜色字符串: '{hex_str}'，"
            f"期望格式: '#RRGGBB' 或 '#RGB'"
        )

    try:
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
    except ValueError:
        raise ValueError(f"无效的十六进制颜色值: '{hex_str}'")

    return (r, g, b)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """将RGB值转换为十六进制颜色字符串。

    Args:
        r: 红色 (0-255)
        g: 绿色 (0-255)
        b: 蓝色 (0-255)

    Returns:
        十六进制颜色字符串，如 '#FF0000'

    Examples:
        >>> rgb_to_hex(255, 0, 0)
        '#FF0000'
    """
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return f"#{r:02X}{g:02X}{b:02X}"


def blend_colors(
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int],
    factor: float
) -> Tuple[int, int, int]:
    """混合两个颜色。

    Args:
        color1: 第一个颜色 (r, g, b)
        color2: 第二个颜色 (r, g, b)
        factor: 混合因子，0.0返回color1，1.0返回color2

    Returns:
        混合后的颜色 (r, g, b)

    Examples:
        >>> blend_colors((255, 0, 0), (0, 0, 255), 0.5)
        (127, 0, 127)
    """
    factor = max(0.0, min(1.0, factor))
    r = int(color1[0] * (1 - factor) + color2[0] * factor)
    g = int(color1[1] * (1 - factor) + color2[1] * factor)
    b = int(color1[2] * (1 - factor) + color2[2] * factor)
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

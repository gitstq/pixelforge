"""
PixelForge - 轻量级跨平台图像智能处理CLI引擎

零外部依赖的纯Python图像处理工具，支持PNG、BMP、PPM/PGM格式读写。
"""

__version__ = "1.0.0"
__author__ = "PixelForge Team"
__license__ = "MIT"

from pixelforge.core.image import Image, Pixel

__all__ = ["Image", "Pixel", "__version__"]

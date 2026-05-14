# -*- coding: utf-8 -*-
"""PixelForge 安装配置"""

import os
from setuptools import setup, find_packages

setup(
    name="pixelforge",
    version="1.0.0",
    description="轻量级跨平台图像智能处理CLI引擎",
    long_description=open("README.md", encoding="utf-8").read()
    if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="PixelForge Team",
    license="MIT",
    python_requires=">=3.8",
    packages=find_packages(),
    package_data={
        "pixelforge": [],
    },
    entry_points={
        "console_scripts": [
            "pixelforge=pixelforge.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
        "Environment :: Console",
        "Operating System :: OS Independent",
    ],
    keywords=["image", "processing", "cli", "png", "bmp", "ppm", "pixel"],
)

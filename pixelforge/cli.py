# -*- coding: utf-8 -*-
"""
PixelForge CLI入口

使用argparse实现美观的命令行界面，提供图像处理的各种操作命令。
"""

from __future__ import annotations

import argparse
import os
import sys


def _banner() -> str:
    """返回CLI横幅文本。"""
    return r"""
╔══════════════════════════════════════════╗
║          PixelForge v1.0.0              ║
║   轻量级跨平台图像智能处理CLI引擎        ║
║   零外部依赖 · 纯Python实现             ║
╚══════════════════════════════════════════╝
"""


def create_parser() -> argparse.ArgumentParser:
    """创建CLI参数解析器。

    Returns:
        配置好的ArgumentParser对象
    """
    parser = argparse.ArgumentParser(
        prog="pixelforge",
        description="PixelForge - 轻量级跨平台图像智能处理CLI引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  pixelforge info photo.png                显示图像信息
  pixelforge convert photo.bmp photo.png   格式转换
  pixelforge resize photo.png out.png -W 800 -H 600
  pixelforge crop photo.png out.png -x 10 -y 10 -w 200 -h 200
  pixelforge rotate photo.png out.png -d 90
  pixelforge flip photo.png out.png -dir h
  pixelforge filter photo.png out.png -t grayscale
  pixelforge watermark photo.png out.png -t "Copyright"
  pixelforge batch resize ./photos -W 800 -H 600
  pixelforge batch convert ./photos -f png
  pixelforge batch filter ./photos -t blur
  pixelforge compare img1.png img2.png
        """
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="PixelForge v1.0.0"
    )

    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # === info 命令 ===
    info_parser = subparsers.add_parser(
        "info", help="显示图像信息", aliases=["i"]
    )
    info_parser.add_argument("image", help="图像文件路径")

    # === convert 命令 ===
    convert_parser = subparsers.add_parser(
        "convert", help="格式转换", aliases=["c"]
    )
    convert_parser.add_argument("input", help="输入文件路径")
    convert_parser.add_argument("output", help="输出文件路径")

    # === resize 命令 ===
    resize_parser = subparsers.add_parser(
        "resize", help="缩放图像", aliases=["r"]
    )
    resize_parser.add_argument("input", help="输入文件路径")
    resize_parser.add_argument("output", help="输出文件路径")
    resize_parser.add_argument(
        "-W", "--width", type=int, required=True, help="目标宽度"
    )
    resize_parser.add_argument(
        "-H", "--height", type=int, required=True, help="目标高度"
    )
    resize_parser.add_argument(
        "-m", "--method",
        choices=["nearest", "bilinear"],
        default="nearest",
        help="缩放方法（默认: nearest）"
    )

    # === crop 命令 ===
    crop_parser = subparsers.add_parser(
        "crop", help="裁剪图像"
    )
    crop_parser.add_argument("input", help="输入文件路径")
    crop_parser.add_argument("output", help="输出文件路径")
    crop_parser.add_argument("-x", type=int, required=True, help="裁剪区域左上角X坐标")
    crop_parser.add_argument("-y", type=int, required=True, help="裁剪区域左上角Y坐标")
    crop_parser.add_argument("-w", type=int, required=True, help="裁剪区域宽度")
    crop_parser.add_argument("--ch", type=int, required=True, help="裁剪区域高度")

    # === rotate 命令 ===
    rotate_parser = subparsers.add_parser(
        "rotate", help="旋转图像"
    )
    rotate_parser.add_argument("input", help="输入文件路径")
    rotate_parser.add_argument("output", help="输出文件路径")
    rotate_parser.add_argument(
        "-d", "--degrees",
        type=int,
        choices=[90, 180, 270],
        required=True,
        help="旋转角度（90/180/270）"
    )

    # === flip 命令 ===
    flip_parser = subparsers.add_parser(
        "flip", help="翻转图像"
    )
    flip_parser.add_argument("input", help="输入文件路径")
    flip_parser.add_argument("output", help="输出文件路径")
    flip_parser.add_argument(
        "--dir", "-dir",
        choices=["horizontal", "vertical", "h", "v"],
        required=True,
        help="翻转方向（horizontal/h 或 vertical/v）"
    )

    # === filter 命令 ===
    filter_parser = subparsers.add_parser(
        "filter", help="应用滤镜", aliases=["f"]
    )
    filter_parser.add_argument("input", help="输入文件路径")
    filter_parser.add_argument("output", help="输出文件路径")
    filter_parser.add_argument(
        "-t", "--type",
        required=True,
        choices=[
            "grayscale", "invert", "brightness", "contrast",
            "threshold", "sepia", "blur", "sharpen",
            "edge_detect", "emboss", "adjust_hue",
            "saturate", "color_temperature"
        ],
        help="滤镜类型"
    )
    filter_parser.add_argument(
        "--value", type=float, default=None,
        help="滤镜参数值（如brightness的factor、threshold的value等）"
    )

    # === watermark 命令 ===
    watermark_parser = subparsers.add_parser(
        "watermark", help="添加水印", aliases=["w"]
    )
    watermark_parser.add_argument("input", help="输入文件路径")
    watermark_parser.add_argument("output", help="输出文件路径")
    watermark_parser.add_argument(
        "-t", "--text", required=True, help="水印文本"
    )
    watermark_parser.add_argument(
        "-p", "--position",
        default="bottom-right",
        choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
        help="水印位置（默认: bottom-right）"
    )
    watermark_parser.add_argument(
        "-o", "--opacity",
        type=float, default=0.5,
        help="水印透明度 0.0-1.0（默认: 0.5）"
    )
    watermark_parser.add_argument(
        "-s", "--font-size",
        type=int, default=12,
        help="字体大小（默认: 12）"
    )

    # === batch 命令 ===
    batch_parser = subparsers.add_parser(
        "batch", help="批量处理"
    )
    batch_subparsers = batch_parser.add_subparsers(
        dest="batch_command", help="批量操作类型"
    )

    # batch resize
    batch_resize_parser = batch_subparsers.add_parser(
        "resize", help="批量缩放"
    )
    batch_resize_parser.add_argument("input_dir", help="输入目录")
    batch_resize_parser.add_argument(
        "-o", "--output", default=None, help="输出目录（默认: input_dir_resized）"
    )
    batch_resize_parser.add_argument("-W", "--width", type=int, required=True, help="目标宽度")
    batch_resize_parser.add_argument("-H", "--height", type=int, required=True, help="目标高度")
    batch_resize_parser.add_argument(
        "-p", "--pattern", default="*.png", help="文件匹配模式（默认: *.png）"
    )
    batch_resize_parser.add_argument(
        "-m", "--method",
        choices=["nearest", "bilinear"],
        default="nearest",
        help="缩放方法（默认: nearest）"
    )

    # batch convert
    batch_convert_parser = batch_subparsers.add_parser(
        "convert", help="批量格式转换"
    )
    batch_convert_parser.add_argument("input_dir", help="输入目录")
    batch_convert_parser.add_argument(
        "-o", "--output", default=None, help="输出目录（默认: input_dir_converted）"
    )
    batch_convert_parser.add_argument(
        "-f", "--format",
        required=True,
        choices=["png", "bmp", "ppm", "pgm", "pbm"],
        help="目标格式"
    )
    batch_convert_parser.add_argument(
        "-p", "--pattern", default="*.png", help="文件匹配模式（默认: *.png）"
    )

    # batch filter
    batch_filter_parser = batch_subparsers.add_parser(
        "filter", help="批量应用滤镜"
    )
    batch_filter_parser.add_argument("input_dir", help="输入目录")
    batch_filter_parser.add_argument(
        "-o", "--output", default=None, help="输出目录（默认: input_dir_filtered）"
    )
    batch_filter_parser.add_argument(
        "-t", "--type",
        required=True,
        choices=[
            "grayscale", "invert", "brightness", "contrast",
            "threshold", "sepia", "blur", "sharpen",
            "edge_detect", "emboss", "adjust_hue",
            "saturate", "color_temperature"
        ],
        help="滤镜类型"
    )
    batch_filter_parser.add_argument(
        "-p", "--pattern", default="*.png", help="文件匹配模式（默认: *.png）"
    )
    batch_filter_parser.add_argument(
        "--value", type=float, default=None, help="滤镜参数值"
    )

    # batch watermark
    batch_watermark_parser = batch_subparsers.add_parser(
        "watermark", help="批量添加水印"
    )
    batch_watermark_parser.add_argument("input_dir", help="输入目录")
    batch_watermark_parser.add_argument(
        "-o", "--output", default=None, help="输出目录（默认: input_dir_watermarked）"
    )
    batch_watermark_parser.add_argument(
        "-t", "--text", required=True, help="水印文本"
    )
    batch_watermark_parser.add_argument(
        "-p", "--position",
        default="bottom-right",
        choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
        help="水印位置（默认: bottom-right）"
    )
    batch_watermark_parser.add_argument(
        "--pattern", default="*.png", help="文件匹配模式（默认: *.png）"
    )

    # === compare 命令 ===
    compare_parser = subparsers.add_parser(
        "compare", help="比较两张图像"
    )
    compare_parser.add_argument("image1", help="第一张图像路径")
    compare_parser.add_argument("image2", help="第二张图像路径")

    return parser


def main(argv: list = None) -> int:
    """CLI主入口函数。

    Args:
        argv: 命令行参数列表，如果为None则使用sys.argv

    Returns:
        退出码，0表示成功
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # 无命令时显示帮助
    if args.command is None:
        print(_banner())
        parser.print_help()
        return 0

    try:
        if args.command in ("info", "i"):
            return _cmd_info(args)
        elif args.command in ("convert", "c"):
            return _cmd_convert(args)
        elif args.command in ("resize", "r"):
            return _cmd_resize(args)
        elif args.command == "crop":
            return _cmd_crop(args)
        elif args.command == "rotate":
            return _cmd_rotate(args)
        elif args.command == "flip":
            return _cmd_flip(args)
        elif args.command in ("filter", "f"):
            return _cmd_filter(args)
        elif args.command in ("watermark", "w"):
            return _cmd_watermark(args)
        elif args.command == "batch":
            return _cmd_batch(args)
        elif args.command == "compare":
            return _cmd_compare(args)
        else:
            parser.print_help()
            return 1

    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


def _cmd_info(args) -> int:
    """处理info命令。"""
    from pixelforge.core.image import Image
    from pixelforge.processors.metadata import get_info

    img = Image.from_file(args.image)
    info = get_info(img, args.image)

    print(f"\n{'='*40}")
    print(f"  图像信息: {info.get('file_name', args.image)}")
    print(f"{'='*40}")
    print(f"  尺寸:       {info['width']} x {info['height']} 像素")
    print(f"  宽高比:     {info['aspect_ratio']}")
    print(f"  总像素数:   {info['total_pixels']:,}")
    print(f"  格式:       {info['format']}")
    if "file_size_str" in info:
        print(f"  文件大小:   {info['file_size_str']}")
    print(f"  平均颜色:   RGB{info['avg_color']}")
    print(f"  平均亮度:   {info['avg_brightness']:.1f}")
    print(f"  亮度范围:   {info['min_brightness']} - {info['max_brightness']}")
    print(f"  含透明通道: {'是' if info['has_alpha'] else '否'}")
    print(f"{'='*40}\n")

    return 0


def _cmd_convert(args) -> int:
    """处理convert命令。"""
    from pixelforge.core.image import Image

    img = Image.from_file(args.input)
    img.save(args.output)
    print(f"已转换: {args.input} -> {args.output}")
    return 0


def _cmd_resize(args) -> int:
    """处理resize命令。"""
    from pixelforge.core.image import Image

    img = Image.from_file(args.input)
    resized = img.resize(args.width, args.height, args.method)
    resized.save(args.output)
    print(f"已缩放: {args.input} -> {args.output} ({args.width}x{args.height}, {args.method})")
    return 0


def _cmd_crop(args) -> int:
    """处理crop命令。"""
    from pixelforge.core.image import Image

    img = Image.from_file(args.input)
    cropped = img.crop(args.x, args.y, args.w, args.ch)
    cropped.save(args.output)
    print(f"已裁剪: {args.input} -> {args.output} ({args.w}x{args.ch} at {args.x},{args.y})")
    return 0


def _cmd_rotate(args) -> int:
    """处理rotate命令。"""
    from pixelforge.core.image import Image

    img = Image.from_file(args.input)
    rotated = img.rotate(args.degrees)
    rotated.save(args.output)
    print(f"已旋转: {args.input} -> {args.output} ({args.degrees}度)")
    return 0


def _cmd_flip(args) -> int:
    """处理flip命令。"""
    from pixelforge.core.image import Image

    # 处理简写
    direction = args.dir
    if direction == "h":
        direction = "horizontal"
    elif direction == "v":
        direction = "vertical"

    img = Image.from_file(args.input)
    flipped = img.flip(direction)
    flipped.save(args.output)
    print(f"已翻转: {args.input} -> {args.output} ({direction})")
    return 0


def _cmd_filter(args) -> int:
    """处理filter命令。"""
    from pixelforge.core.image import Image
    from pixelforge.processors.batch import _get_filter_function

    img = Image.from_file(args.input)

    # 构建滤镜参数
    kwargs = {}
    if args.value is not None:
        filter_type = args.type
        if filter_type == "brightness":
            kwargs["factor"] = args.value
        elif filter_type == "contrast":
            kwargs["factor"] = args.value
        elif filter_type == "threshold":
            kwargs["value"] = int(args.value)
        elif filter_type == "blur":
            kwargs["radius"] = int(args.value)
        elif filter_type == "adjust_hue":
            kwargs["degrees"] = args.value
        elif filter_type == "saturate":
            kwargs["factor"] = args.value
        elif filter_type == "color_temperature":
            kwargs["value"] = int(args.value)

    filter_func = _get_filter_function(args.type, kwargs)
    result = filter_func(img)
    result.save(args.output)
    print(f"已应用滤镜 [{args.type}]: {args.input} -> {args.output}")
    return 0


def _cmd_watermark(args) -> int:
    """处理watermark命令。"""
    from pixelforge.core.image import Image
    from pixelforge.processors.watermark import add_text_watermark

    img = Image.from_file(args.input)
    result = add_text_watermark(
        img, args.text, args.position, args.opacity, args.font_size
    )
    result.save(args.output)
    print(f"已添加水印: {args.input} -> {args.output}")
    return 0


def _cmd_batch(args) -> int:
    """处理batch命令。"""
    from pixelforge.processors.batch import (
        batch_resize, batch_convert, batch_filter, batch_watermark
    )

    if args.batch_command is None:
        print("错误: 请指定批量操作类型 (resize/convert/filter/watermark)",
              file=sys.stderr)
        return 1

    if args.batch_command == "resize":
        output_dir = args.output or args.input_dir + "_resized"
        count = batch_resize(
            args.input_dir, output_dir,
            (args.width, args.height),
            args.pattern, args.method
        )
        print(f"\n批量缩放完成: {count} 个文件 -> {output_dir}")

    elif args.batch_command == "convert":
        output_dir = args.output or args.input_dir + "_converted"
        count = batch_convert(
            args.input_dir, output_dir,
            args.format, args.pattern
        )
        print(f"\n批量转换完成: {count} 个文件 -> {output_dir}")

    elif args.batch_command == "filter":
        output_dir = args.output or args.input_dir + "_filtered"
        kwargs = {}
        if args.value is not None:
            kwargs["value"] = args.value
        count = batch_filter(
            args.input_dir, output_dir,
            args.type, args.pattern, **kwargs
        )
        print(f"\n批量滤镜完成: {count} 个文件 -> {output_dir}")

    elif args.batch_command == "watermark":
        output_dir = args.output or args.input_dir + "_watermarked"
        count = batch_watermark(
            args.input_dir, output_dir,
            args.text, args.position, args.pattern
        )
        print(f"\n批量水印完成: {count} 个文件 -> {output_dir}")

    return 0


def _cmd_compare(args) -> int:
    """处理compare命令。"""
    from pixelforge.core.image import Image
    from pixelforge.processors.comparison import compare, is_identical

    img1 = Image.from_file(args.image1)
    img2 = Image.from_file(args.image2)

    result = compare(img1, img2)

    print(f"\n{'='*40}")
    print(f"  图像比较结果")
    print(f"{'='*40}")
    print(f"  图像1: {args.image1} ({img1.width}x{img1.height})")
    print(f"  图像2: {args.image2} ({img2.width}x{img2.height})")
    print(f"  尺寸相同: {'是' if result['same_size'] else '否'}")
    print(f"  完全相同: {'是' if result['identical'] else '否'}")
    print(f"  差异像素: {result['total_diff_pixels']:,} / {result['total_pixels']:,}")
    print(f"  差异百分比: {result['diff_percentage']:.2f}%")
    print(f"  最大差异值: {result['max_diff']}")
    print(f"  平均差异值: {result['avg_diff']:.4f}")
    print(f"{'='*40}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

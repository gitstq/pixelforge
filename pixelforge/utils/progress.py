# -*- coding: utf-8 -*-
"""
进度条工具

提供美观的命令行进度条显示，用于批量处理等耗时操作。
"""

from __future__ import annotations

import sys
import time


class ProgressBar:
    """命令行进度条。

    在终端中显示处理进度，支持百分比、计数和速度显示。

    Attributes:
        total: 总任务数
        description: 进度条描述文本
        bar_width: 进度条宽度（字符数）

    Examples:
        >>> progress = ProgressBar(100, "处理中")
        >>> for i in range(100):
        ...     # 执行任务
        ...     progress.update(i + 1)
        >>> progress.finish()
    """

    def __init__(
        self,
        total: int,
        description: str = "进度",
        bar_width: int = 40
    ) -> None:
        """初始化进度条。

        Args:
            total: 总任务数
            description: 进度条前缀描述
            bar_width: 进度条显示宽度（字符数）
        """
        self.total = max(1, total)
        self.description = description
        self.bar_width = bar_width
        self.current = 0
        self.start_time = time.time()

    def update(self, current: int) -> None:
        """更新进度条显示。

        Args:
            current: 当前已完成任务数
        """
        self.current = min(current, self.total)
        self._render()

    def _render(self) -> None:
        """渲染进度条到终端。"""
        # 计算进度百分比
        progress = self.current / self.total
        percent = progress * 100

        # 构建进度条字符串
        filled = int(self.bar_width * progress)
        bar = "█" * filled + "░" * (self.bar_width - filled)

        # 计算已用时间和预估剩余时间
        elapsed = time.time() - self.start_time
        if self.current > 0:
            eta = elapsed / self.current * (self.total - self.current)
            eta_str = _format_time(eta)
        else:
            eta_str = "--:--"

        elapsed_str = _format_time(elapsed)

        # 构建输出行
        line = (
            f"\r{self.description}: |{bar}| "
            f"{self.current}/{self.total} "
            f"({percent:.1f}%) "
            f"[{elapsed_str}<{eta_str}]"
        )

        # 写入终端（使用\\r回到行首覆盖）
        sys.stdout.write(line)
        sys.stdout.flush()

    def finish(self) -> None:
        """完成进度条，换行。"""
        self.update(self.total)
        sys.stdout.write("\n")
        sys.stdout.flush()


def _format_time(seconds: float) -> str:
    """将秒数格式化为 MM:SS 或 HH:MM:SS 格式。

    Args:
        seconds: 秒数

    Returns:
        格式化的时间字符串
    """
    if seconds < 0:
        return "--:--"

    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

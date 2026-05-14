# 贡献指南

感谢你对 PixelForge 的关注！本文档将帮助你了解如何参与项目开发。

## 开发环境设置

### 前置要求

- Python 3.8 或更高版本
- Git

### 安装步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/your-repo/pixelforge.git
   cd pixelforge
   ```

2. 以开发模式安装：
   ```bash
   pip install -e .
   ```

## 项目结构

```
pixelforge/
├── pixelforge/
│   ├── __init__.py          # 包初始化，版本号
│   ├── cli.py               # CLI命令行入口
│   ├── core/
│   │   ├── __init__.py
│   │   ├── image.py         # 核心图像数据结构
│   │   └── formats/
│   │       ├── __init__.py  # 格式注册与自动检测
│   │       ├── png.py       # PNG格式读写
│   │       ├── bmp.py       # BMP格式读写
│   │       └── ppm.py       # PPM/PGM/PBM格式读写
│   ├── filters/
│   │   ├── __init__.py
│   │   ├── basic.py         # 基础滤镜
│   │   ├── convolution.py   # 卷积滤镜
│   │   └── color.py         # 颜色操作
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── batch.py         # 批量处理
│   │   ├── watermark.py     # 水印
│   │   ├── metadata.py      # 元数据
│   │   └── comparison.py    # 图像比较
│   └── utils/
│       ├── __init__.py
│       ├── colors.py        # 颜色工具
│       ├── text.py          # 文本渲染
│       └── progress.py      # 进度条
├── setup.py
├── pyproject.toml
├── LICENSE
└── CONTRIBUTING.md
```

## 代码规范

### 零外部依赖

PixelForge 的核心设计原则是零外部依赖。所有功能必须仅使用 Python 标准库实现。请勿引入任何第三方包。

### 代码质量要求

1. **文档字符串**：所有公开函数和类必须有 docstring
2. **类型注解**：所有函数参数和返回值必须有类型注解
3. **错误处理**：完善的错误处理，使用明确的异常类型
4. **中文注释**：关键逻辑处添加中文注释
5. **代码风格**：遵循 PEP 8 规范

### 提交规范

使用语义化提交消息：

```
feat: 新增XXX功能
fix: 修复XXX问题
docs: 更新文档
refactor: 重构XXX
test: 添加XXX测试
chore: 构建/工具变更
```

## 添加新格式支持

如需添加新的图像格式支持：

1. 在 `pixelforge/core/formats/` 下创建新模块
2. 实现 `read_xxx(path) -> Image` 和 `write_xxx(img, path)` 函数
3. 在 `pixelforge/core/formats/__init__.py` 中注册新格式

## 添加新滤镜

如需添加新的图像滤镜：

1. 在 `pixelforge/filters/` 下选择合适的模块或创建新模块
2. 实现滤镜函数 `filter_name(img: Image, **kwargs) -> Image`
3. 在 `pixelforge/processors/batch.py` 的 `_get_filter_function` 中注册
4. 在 `pixelforge/cli.py` 中添加对应的CLI参数

## 测试

运行测试：

```bash
python -m pytest tests/
```

## 问题反馈

如果发现问题或有功能建议，请提交 Issue。

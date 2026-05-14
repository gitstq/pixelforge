<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/dependencies-zero-red.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <b>[简体中文](#简体中文)</b> &nbsp;|&nbsp;
  <b>[繁體中文](#繁體中文)</b> &nbsp;|&nbsp;
  <b>[English](#english)</b>
</p>

---

<a name="简体中文"></a>

# PixelForge

> 轻量级跨平台图像智能处理CLI引擎 - 零依赖、纯Python实现

<p align="center">
  <img src="https://img.shields.io/badge/格式-PNG%20%7C%20BMP%20%7C%20PPM%20%7C%20PGM%20%7C%20PBM-blueviolet.svg" alt="Formats">
  <img src="https://img.shields.io/badge/滤镜-15+-ff69b4.svg" alt="Filters">
  <img src="https://img.shields.io/badge/批量处理-支持-success.svg" alt="Batch">
</p>

---

## 项目介绍

**PixelForge** 是一个零外部依赖的纯Python图像处理CLI工具。它完全基于Python标准库构建，无需安装任何第三方包即可运行。

### 解决的痛点

现有的主流图像处理工具（如 Pillow、OpenCV）虽然功能强大，但存在以下问题：

- **依赖重**：Pillow 需要编译 C 扩展库，OpenCV 依赖更多系统级库
- **安装复杂**：在某些受限环境（嵌入式设备、CI/CD 容器）中安装困难
- **体积庞大**：动辄数十MB的安装包，对于简单图像处理任务来说过于臃肿

**PixelForge** 仅需 Python 标准库，`pip install` 即可使用，安装包体积极小，非常适合轻量化场景。

### 差异化亮点

- **零依赖**：不依赖任何第三方库，纯 Python 标准库实现
- **纯 Python**：所有图像处理算法均为 Python 原生实现，代码可读性高，便于学习和二次开发
- **多格式支持**：支持 PNG（含 CRC 校验）、BMP（1/4/8/16/24/32 位深）、PPM/PGM/PBM 格式
- **15+ 内置滤镜**：涵盖基础调整、色彩操作、卷积滤镜三大类
- **批量处理**：支持批量缩放、格式转换、滤镜应用、水印添加
- **文本水印**：5 种位置、透明度控制、自定义字号
- **图像比较**：差异百分比、差异像素统计、热力图数据

### 灵感来源

灵感来源于 GitHub Trending 上的计算机视觉工具轻量化理念，旨在提供一个「开箱即用、无需折腾」的图像处理方案。

---

## 核心特性

### 多格式支持

| 格式 | 说明 | 特性 |
|------|------|------|
| **PNG** | 便携式网络图形 | 含 CRC 校验、Alpha 通道支持 |
| **BMP** | 位图文件 | 支持 1/4/8/16/24/32 位色深 |
| **PPM** | 便携式像素图 | P6 二进制格式 |
| **PGM** | 便携式灰度图 | P5 二进制格式 |
| **PBM** | 便携式位图 | P4 二进制格式 |

### 15+ 内置滤镜

| 分类 | 滤镜 | 说明 |
|------|------|------|
| **基础调整** | `grayscale` | 灰度化（ITU-R BT.601 标准） |
| | `invert` | 反色处理 |
| | `brightness` | 亮度调整（可调因子） |
| | `contrast` | 对比度调整（可调因子） |
| | `threshold` | 二值化（可调阈值） |
| | `sepia` | 复古/棕褐色调 |
| **卷积滤镜** | `blur` | 高斯模糊（3x3/5x5 核） |
| | `sharpen` | 锐化（拉普拉斯核） |
| | `edge_detect` | 边缘检测（拉普拉斯算子） |
| | `emboss` | 浮雕效果 |
| **色彩操作** | `adjust_hue` | 色调偏移（HSL 色彩空间） |
| | `saturate` | 饱和度调整 |
| | `color_temperature` | 色温调整（暖色/冷色） |

### 图像操作

- **缩放**：支持最近邻插值（`nearest`）和双线性插值（`bilinear`）两种方法
- **裁剪**：指定区域精确裁剪
- **旋转**：支持 90°、180°、270° 旋转
- **翻转**：支持水平翻转和垂直翻转

### 文本水印

- **5 种位置**：`top-left`、`top-right`、`bottom-left`、`bottom-right`、`center`
- **透明度控制**：0.0（完全透明）到 1.0（完全不透明）
- **自定义字号**：可调节字体大小
- **Alpha 混合**：基于 Alpha 通道的精确混合算法

### 批量处理

- 批量缩放（指定目标尺寸和插值方法）
- 批量格式转换（PNG/BMP/PPM/PGM/PBM 互转）
- 批量滤镜应用
- 批量水印添加
- 支持文件通配符匹配（`*.png`、`*.bmp` 等）

### 图像比较

- 差异百分比计算
- 差异像素统计
- 最大/平均差异值
- 差异热力图数据输出

### 元数据管理

- 图像详细信息（尺寸、格式、文件大小、宽高比）
- 颜色统计（平均颜色、平均亮度、亮度范围）
- Alpha 通道检测
- 哈希计算（MD5/SHA1/SHA256）

### 跨平台支持

- **Windows** / **macOS** / **Linux** 全平台兼容
- 仅需 Python 3.8+ 解释器

---

## 快速开始

### 环境要求

- **Python 3.8+**（推荐 3.9 及以上）

### 安装

```bash
# 通过 pip 安装（推荐）
pip install pixelforge

# 或从源码安装
git clone https://github.com/your-repo/pixelforge.git
cd pixelforge
python setup.py install
```

### 基本使用

```bash
# 查看版本
pixelforge -v

# 显示图像信息
pixelforge info photo.png

# 格式转换：BMP -> PNG
pixelforge convert photo.bmp photo.png

# 缩放图像（800x600，双线性插值）
pixelforge resize photo.png output.png -W 800 -H 600 -m bilinear

# 裁剪图像
pixelforge crop photo.png output.png -x 10 -y 10 -w 200 --ch 200

# 旋转图像（顺时针90度）
pixelforge rotate photo.png output.png -d 90

# 水平翻转
pixelforge flip photo.png output.png --dir h

# 应用滤镜（灰度化）
pixelforge filter photo.png output.png -t grayscale

# 应用滤镜（亮度调整，增加50）
pixelforge filter photo.png output.png -t brightness --value 50

# 添加水印
pixelforge watermark photo.png output.png -t "Copyright 2024" -p bottom-right -o 0.6 -s 16

# 比较两张图像
pixelforge compare original.png edited.png
```

### 批量处理

```bash
# 批量缩放目录中的所有 PNG 文件
pixelforge batch resize ./photos -W 800 -H 600 -p "*.png" -m bilinear

# 批量格式转换（PNG -> BMP）
pixelforge batch convert ./photos -f bmp -p "*.png"

# 批量应用模糊滤镜
pixelforge batch filter ./photos -t blur -p "*.png"

# 批量添加水印
pixelforge batch watermark ./photos -t "Sample" -p bottom-right -p "*.png"
```

---

## 详细使用指南

### CLI 命令完整列表

| 命令 | 别名 | 说明 |
|------|------|------|
| `pixelforge info <image>` | `i` | 显示图像详细信息 |
| `pixelforge convert <input> <output>` | `c` | 格式转换 |
| `pixelforge resize <input> <output>` | `r` | 缩放图像 |
| `pixelforge crop <input> <output>` | - | 裁剪图像 |
| `pixelforge rotate <input> <output>` | - | 旋转图像 |
| `pixelforge flip <input> <output>` | - | 翻转图像 |
| `pixelforge filter <input> <output>` | `f` | 应用滤镜 |
| `pixelforge watermark <input> <output>` | `w` | 添加文本水印 |
| `pixelforge batch <sub-command>` | - | 批量处理 |
| `pixelforge compare <img1> <img2>` | - | 比较两张图像 |

### resize 命令参数

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--width` | `-W` | 是 | - | 目标宽度 |
| `--height` | `-H` | 是 | - | 目标高度 |
| `--method` | `-m` | 否 | `nearest` | 缩放方法：`nearest`（最近邻）/ `bilinear`（双线性） |

### crop 命令参数

| 参数 | 缩写 | 必填 | 说明 |
|------|------|------|------|
| `-x` | - | 是 | 裁剪区域左上角 X 坐标 |
| `-y` | - | 是 | 裁剪区域左上角 Y 坐标 |
| `-w` | - | 是 | 裁剪区域宽度 |
| `--ch` | - | 是 | 裁剪区域高度 |

### rotate 命令参数

| 参数 | 缩写 | 必填 | 说明 |
|------|------|------|------|
| `--degrees` | `-d` | 是 | 旋转角度：`90` / `180` / `270` |

### flip 命令参数

| 参数 | 缩写 | 必填 | 说明 |
|------|------|------|------|
| `--dir` | `-dir` | 是 | 翻转方向：`horizontal`（`h`）/ `vertical`（`v`） |

### filter 命令参数

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--type` | `-t` | 是 | - | 滤镜类型（见滤镜列表） |
| `--value` | - | 否 | 视滤镜而定 | 滤镜参数值 |

### watermark 命令参数

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--text` | `-t` | 是 | - | 水印文本 |
| `--position` | `-p` | 否 | `bottom-right` | 水印位置 |
| `--opacity` | `-o` | 否 | `0.5` | 透明度（0.0-1.0） |
| `--font-size` | `-s` | 否 | `12` | 字体大小（像素） |

### batch 子命令参数

| 子命令 | 必填参数 | 可选参数 |
|--------|----------|----------|
| `resize` | `input_dir`, `-W`, `-H` | `-o`（输出目录）, `-p`（文件匹配）, `-m`（缩放方法） |
| `convert` | `input_dir`, `-f`（目标格式） | `-o`, `-p` |
| `filter` | `input_dir`, `-t`（滤镜类型） | `-o`, `-p`, `--value` |
| `watermark` | `input_dir`, `-t`（水印文本） | `-o`, `-p`, `-p`（位置） |

### Python API 使用示例

```python
from pixelforge import Image
from pixelforge.filters.basic import grayscale, sepia, brightness
from pixelforge.filters.convolution import blur, sharpen, edge_detect
from pixelforge.filters.color import adjust_hue, saturate, color_temperature
from pixelforge.processors.watermark import add_text_watermark
from pixelforge.processors.metadata import get_info, calculate_hash
from pixelforge.processors.comparison import compare

# 加载图像
img = Image.from_file("photo.png")

# 获取图像信息
info = get_info(img, "photo.png")
print(f"尺寸: {info['width']}x{info['height']}")
print(f"格式: {info['format']}")
print(f"平均亮度: {info['avg_brightness']:.1f}")

# 应用滤镜
gray_img = grayscale(img)
sepia_img = sepia(img)
bright_img = brightness(img, factor=50)
blur_img = blur(img, radius=1)

# 图像操作
resized = img.resize(800, 600, method="bilinear")
cropped = img.crop(10, 10, 200, 200)
rotated = img.rotate(90)
flipped = img.flip("horizontal")

# 添加水印
watermarked = add_text_watermark(
    img, "Copyright 2024",
    position="bottom-right",
    opacity=0.6,
    font_size=16
)

# 图像比较
img2 = Image.from_file("edited.png")
result = compare(img, img2)
print(f"差异百分比: {result['diff_percentage']:.2f}%")

# 哈希计算
hash_value = calculate_hash(img, algorithm="sha256")
print(f"SHA256: {hash_value}")

# 保存图像
gray_img.save("output_gray.png")
sepia_img.save("output_sepia.bmp")
```

### 滤镜效果说明

| 滤镜 | 参数 | 效果描述 |
|------|------|----------|
| `grayscale` | 无 | 使用 ITU-R BT.601 标准加权公式转为灰度图 |
| `invert` | 无 | RGB 通道取反，产生底片效果 |
| `brightness` | `factor`（建议 -255~255） | 增减像素亮度值 |
| `contrast` | `factor`（建议 0.0~3.0） | 以 128 为中心拉伸/压缩对比度 |
| `threshold` | `value`（0-255，默认 128） | 灰度值大于阈值为白，否则为黑 |
| `sepia` | 无 | 应用棕褐色复古色调矩阵变换 |
| `blur` | `radius`（1 或 2） | 高斯模糊，radius=1 为 3x3 核，radius=2 为 5x5 核 |
| `sharpen` | 无 | 拉普拉斯锐化核增强边缘 |
| `edge_detect` | 无 | 拉普拉斯算子检测图像边缘 |
| `emboss` | 无 | 浮雕卷积核创建立体效果 |
| `adjust_hue` | `degrees`（度） | HSL 色彩空间色调偏移 |
| `saturate` | `factor`（>1 增强，<1 降低） | HSL 色彩空间饱和度调整 |
| `color_temperature` | `value`（建议 -100~100） | 正值偏暖（增红减蓝），负值偏冷（增蓝减红） |

---

## 设计思路与迭代规划

### 设计理念

**「做减法」** 是 PixelForge 的核心设计哲学：

1. **零依赖原则**：所有功能仅使用 Python 标准库（`struct`、`zlib`、`math`、`hashlib`、`argparse` 等），确保在任何 Python 环境中都能直接运行
2. **纯 Python 实现**：不使用 C 扩展，代码完全可读、可调试、可学习，适合作为图像处理算法的教学参考
3. **CLI 优先**：命令行界面设计简洁直观，参数命名符合直觉，支持别名快捷操作
4. **模块化架构**：核心层（`core`）、滤镜层（`filters`）、处理层（`processors`）、工具层（`utils`）职责清晰，便于扩展

### 技术选型原因

| 选型 | 原因 |
|------|------|
| **纯 Python** | 最大兼容性，无需编译，跨平台零成本 |
| **argparse** | Python 标准库 CLI 框架，无额外依赖 |
| **struct/zlib** | 标准库二进制处理，用于 PNG/BMP 格式解析 |
| **HSL 色彩空间** | 色调/饱和度操作比 RGB 更直观 |
| **卷积核架构** | 统一的卷积操作接口，新增滤镜只需定义核矩阵 |

### 项目架构

```
pixelforge/
├── core/                    # 核心层
│   ├── image.py             # Image 和 Pixel 数据结构
│   └── formats/             # 格式解析器
│       ├── png.py           # PNG 读写（含 CRC 校验）
│       ├── bmp.py           # BMP 读写（多位深支持）
│       └── ppm.py           # PPM/PGM/PBM 读写
├── filters/                 # 滤镜层
│   ├── basic.py             # 基础滤镜（灰度/反色/亮度/对比度/二值化/复古）
│   ├── convolution.py       # 卷积滤镜（模糊/锐化/边缘检测/浮雕）
│   └── color.py             # 色彩滤镜（色调/饱和度/色温）
├── processors/              # 处理层
│   ├── batch.py             # 批量处理器
│   ├── watermark.py         # 文本水印
│   ├── comparison.py        # 图像比较
│   └── metadata.py          # 元数据管理
├── utils/                   # 工具层
│   ├── colors.py            # 颜色工具
│   ├── progress.py          # 进度条
│   └── text.py              # 文本渲染
└── cli.py                   # CLI 入口
```

### 后续计划

- [ ] **WebP 格式支持**：添加 WebP 读写能力
- [ ] **GIF 格式支持**：支持 GIF 动画帧的读取和处理
- [ ] **更多滤镜**：添加噪点、晕影、色彩通道分离等创意滤镜
- [ ] **GUI 界面**：基于 tkinter 的图形界面版本
- [ ] **性能优化**：对大图像处理进行性能优化
- [ ] **插件系统**：支持用户自定义滤镜插件

---

## 打包与部署指南

### pip 安装（推荐）

```bash
pip install pixelforge
```

### 源码安装

```bash
git clone https://github.com/your-repo/pixelforge.git
cd pixelforge
pip install .
```

### 开发模式安装

```bash
git clone https://github.com/your-repo/pixelforge.git
cd pixelforge
pip install -e .
```

开发模式安装后，对源码的修改会立即生效，无需重复安装。

### 构建分发包

```bash
# 安装构建工具
pip install build

# 构建 sdist 和 wheel
python -m build
```

构建产物位于 `dist/` 目录下。

---

## 贡献指南

我们欢迎并感谢所有形式的贡献！

### PR 提交规范

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m "feat: 添加某功能"`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 **Pull Request**

**Commit Message 格式**（参考 Conventional Commits）：

| 前缀 | 说明 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | Bug 修复 |
| `docs:` | 文档更新 |
| `refactor:` | 代码重构 |
| `test:` | 测试相关 |
| `chore:` | 构建/工具链更新 |

### Issue 反馈规则

提交 Issue 时，请包含以下信息：

- **Python 版本**：`python --version`
- **操作系统**：Windows/macOS/Linux 及版本号
- **问题描述**：尽量详细地描述复现步骤
- **期望行为**：描述你期望的正确行为
- **实际行为**：描述实际发生的错误行为
- **错误日志**：如有，请附上完整的错误堆栈信息

---

## 开源协议

本项目基于 [MIT License](LICENSE) 开源。

```
MIT License

Copyright (c) 2024 PixelForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  Made with ❤️ by <b>PixelForge Team</b>
</p>

---

<a name="繁體中文"></a>

# PixelForge

> 輕量級跨平台圖像智慧處理CLI引擎 - 零依賴、純Python實作

<p align="center">
  <img src="https://img.shields.io/badge/版本-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/授權-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/依賴-零-red.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

---

## 專案介紹

**PixelForge** 是一個零外部依賴的純Python圖像處理CLI工具。它完全基於Python標準函式庫構建，無需安裝任何第三方套件即可運行。

### 解決的痛點

現有的主流圖像處理工具（如 Pillow、OpenCV）雖然功能強大，但存在以下問題：

- **依賴重**：Pillow 需要編譯 C 擴充函式庫，OpenCV 依賴更多系統級函式庫
- **安裝複雜**：在某些受限環境（嵌入式裝置、CI/CD 容器）中安裝困難
- **體積龐大**：動輒數十MB的安裝包，對於簡單圖像處理任務來說過於臃腫

**PixelForge** 僅需 Python 標準函式庫，`pip install` 即可使用，安裝包體積極小，非常適合輕量化場景。

### 差異化亮點

- **零依賴**：不依賴任何第三方函式庫，純 Python 標準函式庫實作
- **純 Python**：所有圖像處理演算法均為 Python 原生實作，程式碼可讀性高，便於學習和二次開發
- **多格式支援**：支援 PNG（含 CRC 校驗）、BMP（1/4/8/16/24/32 位元深度）、PPM/PGM/PBM 格式
- **15+ 內建濾鏡**：涵蓋基礎調整、色彩操作、卷積濾鏡三大類
- **批次處理**：支援批次縮放、格式轉換、濾鏡應用、浮水印新增
- **文字浮水印**：5 種位置、透明度控制、自訂字號
- **圖像比較**：差異百分比、差異像素統計、熱力圖資料

### 靈感來源

靈感來源於 GitHub Trending 上的電腦視覺工具輕量化理念，旨在提供一個「開箱即用、無需折騰」的圖像處理方案。

---

## 核心特性

### 多格式支援

| 格式 | 說明 | 特性 |
|------|------|------|
| **PNG** | 可攜式網路圖形 | 含 CRC 校驗、Alpha 通道支援 |
| **BMP** | 點陣圖檔案 | 支援 1/4/8/16/24/32 位元深度 |
| **PPM** | 可攜式像素圖 | P6 二進位格式 |
| **PGM** | 可攜式灰度圖 | P5 二進位格式 |
| **PBM** | 可攜式位元圖 | P4 二進位格式 |

### 15+ 內建濾鏡

| 分類 | 濾鏡 | 說明 |
|------|------|------|
| **基礎調整** | `grayscale` | 灰度化（ITU-R BT.601 標準） |
| | `invert` | 反色處理 |
| | `brightness` | 亮度調整（可調因子） |
| | `contrast` | 對比度調整（可調因子） |
| | `threshold` | 二值化（可調閾值） |
| | `sepia` | 復古/棕褐色調 |
| **卷積濾鏡** | `blur` | 高斯模糊（3x3/5x5 核） |
| | `sharpen` | 銳化（拉普拉斯核） |
| | `edge_detect` | 邊緣檢測（拉普拉斯算子） |
| | `emboss` | 浮雕效果 |
| **色彩操作** | `adjust_hue` | 色調偏移（HSL 色彩空間） |
| | `saturate` | 飽和度調整 |
| | `color_temperature` | 色溫調整（暖色/冷色） |

### 圖像操作

- **縮放**：支援最近鄰插值（`nearest`）和雙線性插值（`bilinear`）兩種方法
- **裁切**：指定區域精確裁切
- **旋轉**：支援 90°、180°、270° 旋轉
- **翻轉**：支援水平翻轉和垂直翻轉

### 文字浮水印

- **5 種位置**：`top-left`、`top-right`、`bottom-left`、`bottom-right`、`center`
- **透明度控制**：0.0（完全透明）到 1.0（完全不透明）
- **自訂字號**：可調節字體大小
- **Alpha 混合**：基於 Alpha 通道的精確混合演算法

### 批次處理

- 批次縮放（指定目標尺寸和插值方法）
- 批次格式轉換（PNG/BMP/PPM/PGM/PBM 互轉）
- 批次濾鏡應用
- 批次浮水印新增
- 支援檔案萬用字元匹配（`*.png`、`*.bmp` 等）

### 圖像比較

- 差異百分比計算
- 差異像素統計
- 最大/平均差異值
- 差異熱力圖資料輸出

### 元資料管理

- 圖像詳細資訊（尺寸、格式、檔案大小、寬高比）
- 顏色統計（平均顏色、平均亮度、亮度範圍）
- Alpha 通道檢測
- 雜湊計算（MD5/SHA1/SHA256）

### 跨平台支援

- **Windows** / **macOS** / **Linux** 全平台相容
- 僅需 Python 3.8+ 直譯器

---

## 快速開始

### 環境需求

- **Python 3.8+**（推薦 3.9 及以上）

### 安裝

```bash
# 透過 pip 安裝（推薦）
pip install pixelforge

# 或從原始碼安裝
git clone https://github.com/your-repo/pixelforge.git
cd pixelforge
python setup.py install
```

### 基本使用

```bash
# 查看版本
pixelforge -v

# 顯示圖像資訊
pixelforge info photo.png

# 格式轉換：BMP -> PNG
pixelforge convert photo.bmp photo.png

# 縮放圖像（800x600，雙線性插值）
pixelforge resize photo.png output.png -W 800 -H 600 -m bilinear

# 裁切圖像
pixelforge crop photo.png output.png -x 10 -y 10 -w 200 --ch 200

# 旋轉圖像（順時針90度）
pixelforge rotate photo.png output.png -d 90

# 水平翻轉
pixelforge flip photo.png output.png --dir h

# 套用濾鏡（灰度化）
pixelforge filter photo.png output.png -t grayscale

# 套用濾鏡（亮度調整，增加50）
pixelforge filter photo.png output.png -t brightness --value 50

# 新增浮水印
pixelforge watermark photo.png output.png -t "Copyright 2024" -p bottom-right -o 0.6 -s 16

# 比較兩張圖像
pixelforge compare original.png edited.png
```

### 批次處理

```bash
# 批次縮放目錄中的所有 PNG 檔案
pixelforge batch resize ./photos -W 800 -H 600 -p "*.png" -m bilinear

# 批次格式轉換（PNG -> BMP）
pixelforge batch convert ./photos -f bmp -p "*.png"

# 批次套用模糊濾鏡
pixelforge batch filter ./photos -t blur -p "*.png"

# 批次新增浮水印
pixelforge batch watermark ./photos -t "Sample" -p bottom-right -p "*.png"
```

---

## 詳細使用指南

### CLI 命令完整列表

| 命令 | 別名 | 說明 |
|------|------|------|
| `pixelforge info <image>` | `i` | 顯示圖像詳細資訊 |
| `pixelforge convert <input> <output>` | `c` | 格式轉換 |
| `pixelforge resize <input> <output>` | `r` | 縮放圖像 |
| `pixelforge crop <input> <output>` | - | 裁切圖像 |
| `pixelforge rotate <input> <output>` | - | 旋轉圖像 |
| `pixelforge flip <input> <output>` | - | 翻轉圖像 |
| `pixelforge filter <input> <output>` | `f` | 套用濾鏡 |
| `pixelforge watermark <input> <output>` | `w` | 新增文字浮水印 |
| `pixelforge batch <sub-command>` | - | 批次處理 |
| `pixelforge compare <img1> <img2>` | - | 比較兩張圖像 |

### resize 命令參數

| 參數 | 縮寫 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `--width` | `-W` | 是 | - | 目標寬度 |
| `--height` | `-H` | 是 | - | 目標高度 |
| `--method` | `-m` | 否 | `nearest` | 縮放方法：`nearest`（最近鄰）/ `bilinear`（雙線性） |

### crop 命令參數

| 參數 | 縮寫 | 必填 | 說明 |
|------|------|------|------|
| `-x` | - | 是 | 裁切區域左上角 X 座標 |
| `-y` | - | 是 | 裁切區域左上角 Y 座標 |
| `-w` | - | 是 | 裁切區域寬度 |
| `--ch` | - | 是 | 裁切區域高度 |

### rotate 命令參數

| 參數 | 縮寫 | 必填 | 說明 |
|------|------|------|------|
| `--degrees` | `-d` | 是 | 旋轉角度：`90` / `180` / `270` |

### flip 命令參數

| 參數 | 縮寫 | 必填 | 說明 |
|------|------|------|------|
| `--dir` | `-dir` | 是 | 翻轉方向：`horizontal`（`h`）/ `vertical`（`v`） |

### filter 命令參數

| 參數 | 縮寫 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `--type` | `-t` | 是 | - | 濾鏡類型（見濾鏡列表） |
| `--value` | - | 否 | 視濾鏡而定 | 濾鏡參數值 |

### watermark 命令參數

| 參數 | 縮寫 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `--text` | `-t` | 是 | - | 浮水印文字 |
| `--position` | `-p` | 否 | `bottom-right` | 浮水印位置 |
| `--opacity` | `-o` | 否 | `0.5` | 透明度（0.0-1.0） |
| `--font-size` | `-s` | 否 | `12` | 字體大小（像素） |

### batch 子命令參數

| 子命令 | 必填參數 | 可選參數 |
|--------|----------|----------|
| `resize` | `input_dir`, `-W`, `-H` | `-o`（輸出目錄）, `-p`（檔案匹配）, `-m`（縮放方法） |
| `convert` | `input_dir`, `-f`（目標格式） | `-o`, `-p` |
| `filter` | `input_dir`, `-t`（濾鏡類型） | `-o`, `-p`, `--value` |
| `watermark` | `input_dir`, `-t`（浮水印文字） | `-o`, `-p`, `-p`（位置） |

### Python API 使用範例

```python
from pixelforge import Image
from pixelforge.filters.basic import grayscale, sepia, brightness
from pixelforge.filters.convolution import blur, sharpen, edge_detect
from pixelforge.filters.color import adjust_hue, saturate, color_temperature
from pixelforge.processors.watermark import add_text_watermark
from pixelforge.processors.metadata import get_info, calculate_hash
from pixelforge.processors.comparison import compare

# 載入圖像
img = Image.from_file("photo.png")

# 取得圖像資訊
info = get_info(img, "photo.png")
print(f"尺寸: {info['width']}x{info['height']}")
print(f"格式: {info['format']}")
print(f"平均亮度: {info['avg_brightness']:.1f}")

# 套用濾鏡
gray_img = grayscale(img)
sepia_img = sepia(img)
bright_img = brightness(img, factor=50)
blur_img = blur(img, radius=1)

# 圖像操作
resized = img.resize(800, 600, method="bilinear")
cropped = img.crop(10, 10, 200, 200)
rotated = img.rotate(90)
flipped = img.flip("horizontal")

# 新增浮水印
watermarked = add_text_watermark(
    img, "Copyright 2024",
    position="bottom-right",
    opacity=0.6,
    font_size=16
)

# 圖像比較
img2 = Image.from_file("edited.png")
result = compare(img, img2)
print(f"差異百分比: {result['diff_percentage']:.2f}%")

# 雜湊計算
hash_value = calculate_hash(img, algorithm="sha256")
print(f"SHA256: {hash_value}")

# 儲存圖像
gray_img.save("output_gray.png")
sepia_img.save("output_sepia.bmp")
```

### 濾鏡效果說明

| 濾鏡 | 參數 | 效果描述 |
|------|------|----------|
| `grayscale` | 無 | 使用 ITU-R BT.601 標準加權公式轉為灰度圖 |
| `invert` | 無 | RGB 通道取反，產生底片效果 |
| `brightness` | `factor`（建議 -255~255） | 增減像素亮度值 |
| `contrast` | `factor`（建議 0.0~3.0） | 以 128 為中心拉伸/壓縮對比度 |
| `threshold` | `value`（0-255，預設 128） | 灰度值大於閾值為白，否則為黑 |
| `sepia` | 無 | 套用棕褐色復古色調矩陣變換 |
| `blur` | `radius`（1 或 2） | 高斯模糊，radius=1 為 3x3 核，radius=2 為 5x5 核 |
| `sharpen` | 無 | 拉普拉斯銳化核增強邊緣 |
| `edge_detect` | 無 | 拉普拉斯算子檢測圖像邊緣 |
| `emboss` | 無 | 浮雕卷積核建立立體效果 |
| `adjust_hue` | `degrees`（度） | HSL 色彩空間色調偏移 |
| `saturate` | `factor`（>1 增強，<1 降低） | HSL 色彩空間飽和度調整 |
| `color_temperature` | `value`（建議 -100~100） | 正值偏暖（增紅減藍），負值偏冷（增藍減紅） |

---

## 設計思路與迭代規劃

### 設計理念

**「做減法」** 是 PixelForge 的核心設計哲學：

1. **零依賴原則**：所有功能僅使用 Python 標準函式庫（`struct`、`zlib`、`math`、`hashlib`、`argparse` 等），確保在任何 Python 環境中都能直接運行
2. **純 Python 實作**：不使用 C 擴充，程式碼完全可讀、可除錯、可學習，適合作為圖像處理演算法的教學參考
3. **CLI 優先**：命令列介面設計簡潔直觀，參數命名符合直覺，支援別名快捷操作
4. **模組化架構**：核心層（`core`）、濾鏡層（`filters`）、處理層（`processors`）、工具層（`utils`）職責清晰，便於擴充

### 技術選型原因

| 選型 | 原因 |
|------|------|
| **純 Python** | 最大相容性，無需編譯，跨平台零成本 |
| **argparse** | Python 標準函式庫 CLI 框架，無額外依賴 |
| **struct/zlib** | 標準函式庫二進位處理，用於 PNG/BMP 格式解析 |
| **HSL 色彩空間** | 色調/飽和度操作比 RGB 更直觀 |
| **卷積核架構** | 統一的卷積操作介面，新增濾鏡只需定義核矩陣 |

### 專案架構

```
pixelforge/
├── core/                    # 核心層
│   ├── image.py             # Image 和 Pixel 資料結構
│   └── formats/             # 格式解析器
│       ├── png.py           # PNG 讀寫（含 CRC 校驗）
│       ├── bmp.py           # BMP 讀寫（多位元深度支援）
│       └── ppm.py           # PPM/PGM/PBM 讀寫
├── filters/                 # 濾鏡層
│   ├── basic.py             # 基礎濾鏡（灰度/反色/亮度/對比度/二值化/復古）
│   ├── convolution.py       # 卷積濾鏡（模糊/銳化/邊緣檢測/浮雕）
│   └── color.py             # 色彩濾鏡（色調/飽和度/色溫）
├── processors/              # 處理層
│   ├── batch.py             # 批次處理器
│   ├── watermark.py         # 文字浮水印
│   ├── comparison.py        # 圖像比較
│   └── metadata.py          # 元資料管理
├── utils/                   # 工具層
│   ├── colors.py            # 顏色工具
│   ├── progress.py          # 進度條
│   └── text.py              # 文字渲染
└── cli.py                   # CLI 入口
```

### 後續計畫

- [ ] **WebP 格式支援**：新增 WebP 讀寫能力
- [ ] **GIF 格式支援**：支援 GIF 動畫幀的讀取和處理
- [ ] **更多濾鏡**：新增雜訊、暈影、色彩通道分離等創意濾鏡
- [ ] **GUI 介面**：基於 tkinter 的圖形介面版本
- [ ] **效能最佳化**：對大圖像處理進行效能最佳化
- [ ] **外掛系統**：支援使用者自訂濾鏡外掛

---

## 打包與部署指南

### pip 安裝（推薦）

```bash
pip install pixelforge
```

### 原始碼安裝

```bash
git clone https://github.com/your-repo/pixelforge.git
cd pixelforge
pip install .
```

### 開發模式安裝

```bash
git clone https://github.com/your-repo/pixelforge.git
cd pixelforge
pip install -e .
```

開發模式安裝後，對原始碼的修改會立即生效，無需重複安裝。

### 建構分發包

```bash
# 安裝建構工具
pip install build

# 建構 sdist 和 wheel
python -m build
```

建構產物位於 `dist/` 目錄下。

---

## 貢獻指南

我們歡迎並感謝所有形式的貢獻！

### PR 提交規範

1. **Fork** 本儲存庫
2. 建立特性分支：`git checkout -b feature/your-feature`
3. 提交變更：`git commit -m "feat: 新增某功能"`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 **Pull Request**

**Commit Message 格式**（參考 Conventional Commits）：

| 前綴 | 說明 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | Bug 修復 |
| `docs:` | 文件更新 |
| `refactor:` | 程式碼重構 |
| `test:` | 測試相關 |
| `chore:` | 建構/工具鏈更新 |

### Issue 回饋規則

提交 Issue 時，請包含以下資訊：

- **Python 版本**：`python --version`
- **作業系統**：Windows/macOS/Linux 及版本號
- **問題描述**：盡量詳細地描述重現步驟
- **期望行為**：描述你期望的正確行為
- **實際行為**：描述實際發生的錯誤行為
- **錯誤日誌**：如有，請附上完整的錯誤堆疊資訊

---

## 開源授權

本專案基於 [MIT License](LICENSE) 開源。

```
MIT License

Copyright (c) 2024 PixelForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  Made with ❤️ by <b>PixelForge Team</b>
</p>

---

<a name="english"></a>

# PixelForge

> Lightweight Cross-Platform Image Processing CLI Engine - Zero Dependencies, Pure Python

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/dependencies-zero-red.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

---

## Introduction

**PixelForge** is a zero-dependency, pure Python image processing CLI tool. It is built entirely on the Python standard library and requires no third-party packages to run.

### Problems We Solve

Existing mainstream image processing tools (such as Pillow and OpenCV) are powerful, but they come with several drawbacks:

- **Heavy dependencies**: Pillow requires compiling C extensions; OpenCV depends on even more system-level libraries
- **Complex installation**: Difficult to install in restricted environments (embedded devices, CI/CD containers)
- **Large footprint**: Tens of MBs of installation packages, which is overkill for simple image processing tasks

**PixelForge** only requires the Python standard library. Just `pip install` and you're ready to go. The installation package is extremely small, making it ideal for lightweight scenarios.

### Key Highlights

- **Zero dependencies**: No third-party libraries required, implemented purely with the Python standard library
- **Pure Python**: All image processing algorithms are implemented natively in Python with high code readability, making it easy to learn and extend
- **Multi-format support**: PNG (with CRC verification), BMP (1/4/8/16/24/32-bit depth), PPM/PGM/PBM formats
- **15+ built-in filters**: Covering basic adjustments, color operations, and convolution filters
- **Batch processing**: Batch resize, format conversion, filter application, and watermarking
- **Text watermarking**: 5 positions, opacity control, custom font size
- **Image comparison**: Difference percentage, difference pixel statistics, heatmap data

### Inspiration

Inspired by the lightweight philosophy of computer vision tools trending on GitHub, PixelForge aims to provide an "out-of-the-box, hassle-free" image processing solution.

---

## Core Features

### Multi-Format Support

| Format | Description | Features |
|--------|-------------|----------|
| **PNG** | Portable Network Graphics | CRC verification, Alpha channel support |
| **BMP** | Bitmap File | Supports 1/4/8/16/24/32-bit depth |
| **PPM** | Portable Pixel Map | P6 binary format |
| **PGM** | Portable Gray Map | P5 binary format |
| **PBM** | Portable Bit Map | P4 binary format |

### 15+ Built-in Filters

| Category | Filter | Description |
|----------|--------|-------------|
| **Basic Adjustments** | `grayscale` | Grayscale conversion (ITU-R BT.601 standard) |
| | `invert` | Color inversion |
| | `brightness` | Brightness adjustment (adjustable factor) |
| | `contrast` | Contrast adjustment (adjustable factor) |
| | `threshold` | Binarization (adjustable threshold) |
| | `sepia` | Vintage / Sepia tone |
| **Convolution Filters** | `blur` | Gaussian blur (3x3/5x5 kernel) |
| | `sharpen` | Sharpening (Laplacian kernel) |
| | `edge_detect` | Edge detection (Laplacian operator) |
| | `emboss` | Emboss effect |
| **Color Operations** | `adjust_hue` | Hue shift (HSL color space) |
| | `saturate` | Saturation adjustment |
| | `color_temperature` | Color temperature adjustment (warm/cool) |

### Image Operations

- **Resize**: Supports nearest-neighbor (`nearest`) and bilinear (`bilinear`) interpolation
- **Crop**: Precise cropping with specified region
- **Rotate**: Supports 90, 180, and 270-degree rotation
- **Flip**: Supports horizontal and vertical flipping

### Text Watermarking

- **5 positions**: `top-left`, `top-right`, `bottom-left`, `bottom-right`, `center`
- **Opacity control**: 0.0 (fully transparent) to 1.0 (fully opaque)
- **Custom font size**: Adjustable font size
- **Alpha blending**: Precise blending algorithm based on Alpha channel

### Batch Processing

- Batch resize (specify target dimensions and interpolation method)
- Batch format conversion (PNG/BMP/PPM/PGM/PBM interconversion)
- Batch filter application
- Batch watermarking
- File glob pattern matching support (`*.png`, `*.bmp`, etc.)

### Image Comparison

- Difference percentage calculation
- Difference pixel statistics
- Maximum/average difference values
- Difference heatmap data output

### Metadata Management

- Detailed image information (dimensions, format, file size, aspect ratio)
- Color statistics (average color, average brightness, brightness range)
- Alpha channel detection
- Hash calculation (MD5/SHA1/SHA256)

### Cross-Platform Support

- **Windows** / **macOS** / **Linux** compatible
- Only requires Python 3.8+ interpreter

---

## Quick Start

### Requirements

- **Python 3.8+** (3.9+ recommended)

### Installation

```bash
# Install via pip (recommended)
pip install pixelforge

# Or install from source
git clone https://github.com/your-repo/pixelforge.git
cd pixelforge
python setup.py install
```

### Basic Usage

```bash
# Check version
pixelforge -v

# Display image information
pixelforge info photo.png

# Format conversion: BMP -> PNG
pixelforge convert photo.bmp photo.png

# Resize image (800x600, bilinear interpolation)
pixelforge resize photo.png output.png -W 800 -H 600 -m bilinear

# Crop image
pixelforge crop photo.png output.png -x 10 -y 10 -w 200 --ch 200

# Rotate image (90 degrees clockwise)
pixelforge rotate photo.png output.png -d 90

# Horizontal flip
pixelforge flip photo.png output.png --dir h

# Apply filter (grayscale)
pixelforge filter photo.png output.png -t grayscale

# Apply filter (brightness adjustment, increase by 50)
pixelforge filter photo.png output.png -t brightness --value 50

# Add watermark
pixelforge watermark photo.png output.png -t "Copyright 2024" -p bottom-right -o 0.6 -s 16

# Compare two images
pixelforge compare original.png edited.png
```

### Batch Processing

```bash
# Batch resize all PNG files in a directory
pixelforge batch resize ./photos -W 800 -H 600 -p "*.png" -m bilinear

# Batch format conversion (PNG -> BMP)
pixelforge batch convert ./photos -f bmp -p "*.png"

# Batch apply blur filter
pixelforge batch filter ./photos -t blur -p "*.png"

# Batch add watermarks
pixelforge batch watermark ./photos -t "Sample" -p bottom-right -p "*.png"
```

---

## Detailed Usage Guide

### Complete CLI Command List

| Command | Alias | Description |
|---------|-------|-------------|
| `pixelforge info <image>` | `i` | Display detailed image information |
| `pixelforge convert <input> <output>` | `c` | Format conversion |
| `pixelforge resize <input> <output>` | `r` | Resize image |
| `pixelforge crop <input> <output>` | - | Crop image |
| `pixelforge rotate <input> <output>` | - | Rotate image |
| `pixelforge flip <input> <output>` | - | Flip image |
| `pixelforge filter <input> <output>` | `f` | Apply filter |
| `pixelforge watermark <input> <output>` | `w` | Add text watermark |
| `pixelforge batch <sub-command>` | - | Batch processing |
| `pixelforge compare <img1> <img2>` | - | Compare two images |

### resize Command Parameters

| Parameter | Short | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `--width` | `-W` | Yes | - | Target width |
| `--height` | `-H` | Yes | - | Target height |
| `--method` | `-m` | No | `nearest` | Interpolation method: `nearest` / `bilinear` |

### crop Command Parameters

| Parameter | Short | Required | Description |
|-----------|-------|----------|-------------|
| `-x` | - | Yes | Top-left X coordinate of crop region |
| `-y` | - | Yes | Top-left Y coordinate of crop region |
| `-w` | - | Yes | Crop region width |
| `--ch` | - | Yes | Crop region height |

### rotate Command Parameters

| Parameter | Short | Required | Description |
|-----------|-------|----------|-------------|
| `--degrees` | `-d` | Yes | Rotation angle: `90` / `180` / `270` |

### flip Command Parameters

| Parameter | Short | Required | Description |
|-----------|-------|----------|-------------|
| `--dir` | `-dir` | Yes | Flip direction: `horizontal` (`h`) / `vertical` (`v`) |

### filter Command Parameters

| Parameter | Short | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `--type` | `-t` | Yes | - | Filter type (see filter list) |
| `--value` | - | No | Varies | Filter parameter value |

### watermark Command Parameters

| Parameter | Short | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `--text` | `-t` | Yes | - | Watermark text |
| `--position` | `-p` | No | `bottom-right` | Watermark position |
| `--opacity` | `-o` | No | `0.5` | Opacity (0.0-1.0) |
| `--font-size` | `-s` | No | `12` | Font size (pixels) |

### batch Sub-command Parameters

| Sub-command | Required Parameters | Optional Parameters |
|-------------|---------------------|---------------------|
| `resize` | `input_dir`, `-W`, `-H` | `-o` (output dir), `-p` (pattern), `-m` (method) |
| `convert` | `input_dir`, `-f` (target format) | `-o`, `-p` |
| `filter` | `input_dir`, `-t` (filter type) | `-o`, `-p`, `--value` |
| `watermark` | `input_dir`, `-t` (watermark text) | `-o`, `-p`, `-p` (position) |

### Python API Examples

```python
from pixelforge import Image
from pixelforge.filters.basic import grayscale, sepia, brightness
from pixelforge.filters.convolution import blur, sharpen, edge_detect
from pixelforge.filters.color import adjust_hue, saturate, color_temperature
from pixelforge.processors.watermark import add_text_watermark
from pixelforge.processors.metadata import get_info, calculate_hash
from pixelforge.processors.comparison import compare

# Load image
img = Image.from_file("photo.png")

# Get image information
info = get_info(img, "photo.png")
print(f"Dimensions: {info['width']}x{info['height']}")
print(f"Format: {info['format']}")
print(f"Average brightness: {info['avg_brightness']:.1f}")

# Apply filters
gray_img = grayscale(img)
sepia_img = sepia(img)
bright_img = brightness(img, factor=50)
blur_img = blur(img, radius=1)

# Image operations
resized = img.resize(800, 600, method="bilinear")
cropped = img.crop(10, 10, 200, 200)
rotated = img.rotate(90)
flipped = img.flip("horizontal")

# Add watermark
watermarked = add_text_watermark(
    img, "Copyright 2024",
    position="bottom-right",
    opacity=0.6,
    font_size=16
)

# Compare images
img2 = Image.from_file("edited.png")
result = compare(img, img2)
print(f"Difference: {result['diff_percentage']:.2f}%")

# Hash calculation
hash_value = calculate_hash(img, algorithm="sha256")
print(f"SHA256: {hash_value}")

# Save image
gray_img.save("output_gray.png")
sepia_img.save("output_sepia.bmp")
```

### Filter Effect Details

| Filter | Parameter | Effect Description |
|--------|-----------|-------------------|
| `grayscale` | None | Converts to grayscale using ITU-R BT.601 weighted formula |
| `invert` | None | Inverts RGB channels, creating a negative effect |
| `brightness` | `factor` (recommended -255~255) | Increases/decreases pixel brightness values |
| `contrast` | `factor` (recommended 0.0~3.0) | Stretches/compresses contrast centered at 128 |
| `threshold` | `value` (0-255, default 128) | Pixels above threshold become white, otherwise black |
| `sepia` | None | Applies sepia tone matrix transformation |
| `blur` | `radius` (1 or 2) | Gaussian blur; radius=1 uses 3x3 kernel, radius=2 uses 5x5 kernel |
| `sharpen` | None | Laplacian sharpening kernel enhances edges |
| `edge_detect` | None | Laplacian operator detects image edges |
| `emboss` | None | Emboss convolution kernel creates 3D relief effect |
| `adjust_hue` | `degrees` | Hue shift in HSL color space |
| `saturate` | `factor` (>1 increases, <1 decreases) | Saturation adjustment in HSL color space |
| `color_temperature` | `value` (recommended -100~100) | Positive = warm (more red, less blue); Negative = cool (more blue, less red) |

---

## Design Philosophy & Roadmap

### Design Philosophy

**"Less is More"** is the core design philosophy of PixelForge:

1. **Zero dependency principle**: All features use only the Python standard library (`struct`, `zlib`, `math`, `hashlib`, `argparse`, etc.), ensuring it runs directly in any Python environment
2. **Pure Python implementation**: No C extensions; code is fully readable, debuggable, and learnable, making it an excellent teaching reference for image processing algorithms
3. **CLI-first design**: Clean and intuitive command-line interface with sensible parameter names and alias shortcuts
4. **Modular architecture**: Clear separation between the core layer (`core`), filter layer (`filters`), processor layer (`processors`), and utility layer (`utils`), making it easy to extend

### Technical Choices

| Choice | Rationale |
|--------|-----------|
| **Pure Python** | Maximum compatibility, no compilation needed, zero-cost cross-platform support |
| **argparse** | Standard library CLI framework, no extra dependencies |
| **struct/zlib** | Standard library binary processing for PNG/BMP format parsing |
| **HSL color space** | Hue/saturation operations are more intuitive than RGB |
| **Convolution kernel architecture** | Unified convolution interface; adding new filters only requires defining a kernel matrix |

### Project Architecture

```
pixelforge/
├── core/                    # Core layer
│   ├── image.py             # Image and Pixel data structures
│   └── formats/             # Format parsers
│       ├── png.py           # PNG read/write (with CRC verification)
│       ├── bmp.py           # BMP read/write (multi-bit-depth support)
│       └── ppm.py           # PPM/PGM/PBM read/write
├── filters/                 # Filter layer
│   ├── basic.py             # Basic filters (grayscale/invert/brightness/contrast/threshold/sepia)
│   ├── convolution.py       # Convolution filters (blur/sharpen/edge_detect/emboss)
│   └── color.py             # Color filters (hue/saturation/color_temperature)
├── processors/              # Processor layer
│   ├── batch.py             # Batch processor
│   ├── watermark.py         # Text watermarking
│   ├── comparison.py        # Image comparison
│   └── metadata.py          # Metadata management
├── utils/                   # Utility layer
│   ├── colors.py            # Color utilities
│   ├── progress.py          # Progress bar
│   └── text.py              # Text rendering
└── cli.py                   # CLI entry point
```

### Roadmap

- [ ] **WebP format support**: Add WebP read/write capabilities
- [ ] **GIF format support**: Support reading and processing GIF animation frames
- [ ] **More filters**: Add noise, vignette, channel splitting, and other creative filters
- [ ] **GUI interface**: A graphical interface version based on tkinter
- [ ] **Performance optimization**: Optimize processing speed for large images
- [ ] **Plugin system**: Support user-defined filter plugins

---

## Packaging & Deployment Guide

### pip Install (Recommended)

```bash
pip install pixelforge
```

### Install from Source

```bash
git clone https://github.com/your-repo/pixelforge.git
cd pixelforge
pip install .
```

### Development Mode Install

```bash
git clone https://github.com/your-repo/pixelforge.git
cd pixelforge
pip install -e .
```

In development mode, changes to the source code take effect immediately without reinstallation.

### Build Distribution Packages

```bash
# Install build tools
pip install build

# Build sdist and wheel
python -m build
```

Build artifacts are located in the `dist/` directory.

---

## Contributing Guide

We welcome and appreciate contributions of all forms!

### PR Submission Guidelines

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add some feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Submit a **Pull Request**

**Commit Message Format** (following Conventional Commits):

| Prefix | Description |
|--------|-------------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation update |
| `refactor:` | Code refactoring |
| `test:` | Test-related |
| `chore:` | Build/toolchain update |

### Issue Reporting Guidelines

When submitting an issue, please include the following information:

- **Python version**: `python --version`
- **Operating system**: Windows/macOS/Linux and version number
- **Problem description**: Describe the reproduction steps in detail
- **Expected behavior**: Describe what you expect to happen
- **Actual behavior**: Describe what actually happens incorrectly
- **Error logs**: If available, attach the complete error stack trace

---

## License

This project is licensed under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024 PixelForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  Made with ❤️ by <b>PixelForge Team</b>
</p>

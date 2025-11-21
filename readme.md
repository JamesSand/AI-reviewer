# Review Attack - 论文审稿系统

这是一个使用多个大语言模型（OpenAI、Claude、Gemini）自动生成学术论文审稿意见的工具。

## 📁 项目结构

```
AI-review/
├── env.yaml.example           # API密钥配置示例文件
├── env.yaml                   # API密钥配置文件（不要提交到Git）
├── reviewer_guidance.txt      # 审稿指导模板
├── generate_all.py           # 一键生成所有模型审稿（推荐）
├── generate_openai.py        # OpenAI单独生成脚本
├── generate_claude.py        # Claude单独生成脚本  
├── generate_gemini.py        # Gemini单独生成脚本
├── analyze_and_vis.py        # 分析和可视化脚本
├── example_pdfs/             # 示例PDF文件
└── output/                   # 输出根目录
    ├── output_openai/        # OpenAI生成的审稿结果
    ├── output_claude/        # Claude生成的审稿结果
    ├── output_gemini/        # Gemini生成的审稿结果
    └── analyze_image/        # 分析结果可视化图表
```

## 🚀 快速开始

### 0. 安装依赖

```bash
pip install openai anthropic google-genai matplotlib numpy
```

### 1. 配置API密钥

首先，复制示例配置文件并填入你的API密钥：

```bash
# 复制示例配置文件
cp env.yaml.example env.yaml

# 编辑 env.yaml，填入你的实际API密钥
nano env.yaml  # 或使用其他编辑器
```

`env.yaml` 文件格式：

```yaml
OPENAI_API_KEY: "sk-proj-xxxx..."
ANTHROPIC_API_KEY: "sk-ant-api03-xxxx..."
GEMINI_API_KEY: "AIzaSyxxxx..."
```

**获取API密钥：**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic (Claude): https://console.anthropic.com/
- Google (Gemini): https://aistudio.google.com/app/apikey

### 2. 生成审稿意见

**推荐方式：使用 `generate_all.py` 一键生成所有模型的审稿**

```bash
# 基本用法：为单篇论文生成所有模型的审稿（每个模型10次）
python generate_all.py --pdf_path example_pdfs/paper.pdf

# 自定义参数
python generate_all.py \
    --pdf_path example_pdfs/paper.pdf \
    --guidance reviewer_guidance.txt \
    --tries 10 \
    --output output
```

这将自动调用以下6个模型，每个模型生成10次审稿（共60个审稿文件）：
- **OpenAI**: gpt-5, gpt-5-mini
- **Claude**: claude-sonnet-4-5, claude-haiku-4-5
- **Gemini**: gemini-2.5-flash, gemini-2.5-flash-lite

**可选：单独运行某个API**

如果只想使用某个特定的API，可以直接运行对应的脚本：

```bash
python generate_openai.py   # 仅OpenAI
python generate_claude.py    # 仅Claude
python generate_gemini.py    # 仅Gemini
```

### 3. 分析结果

编辑 `analyze_and_vis.py` 中的参数，然后运行：

```python
# 分析特定模型和论文的结果
analyze_reviews("output_gemini", 
                model_name="gemini-2.5-flash", 
                pdf_name="a0kq0tJwwn")

# 或分析整个输出目录
analyze_reviews("output_openai")
```

```bash
python analyze_and_vis.py
```

生成的可视化图表会保存在 `analyze_image/` 目录下。

## 📊 功能特性

### 生成审稿意见（generate_all.py）

`generate_all.py` 提供一站式审稿生成：
- **自动化流程**：一次调用生成所有模型的审稿
- **多模型支持**：同时使用OpenAI、Claude、Gemini的6个不同模型
- **批量生成**：每个模型默认生成10次独立审稿
- **断点续传**：自动跳过已存在的文件，支持中断后继续
- **错误处理**：单个调用失败不影响其他模型继续运行
- **命令行参数**：灵活配置PDF路径、生成次数、输出目录等

**输出文件命名格式**：`{model_name}_{pdf_name}_{attempt}.txt`

**支持的评分指标**：
- **Soundness**: 技术正确性 (1-5分)
- **Presentation**: 呈现质量 (1-5分)
- **Contribution**: 贡献度 (1-5分)
- **Rating**: 总体评分 (1-10分)
- **Confidence**: 信心度 (1-5分)

### 分析和可视化

`analyze_and_vis.py` 提供：
- 自动提取所有评分指标
- 统计分析（均值、标准差、方差、分布）
- 生成 2×3 布局的可视化图表
- 支持按模型和论文筛选分析

## 🔧 自定义配置

### generate_all.py 命令行参数

```bash
python generate_all.py --help
```

**可用参数：**
- `--pdf_path`: PDF文件路径（必需）
- `--guidance`: 审稿指导文件路径（默认：`reviewer_guidance.txt`）
- `--tries`: 每个模型生成次数（默认：10）
- `--output`: 输出根目录（默认：`output`）

**示例：**

```bash
# 生成5次审稿而不是默认的10次
python generate_all.py --pdf_path paper.pdf --tries 5

# 使用自定义审稿指导和输出目录
python generate_all.py --pdf_path paper.pdf \
    --guidance custom_guidance.txt \
    --output my_output
```

### 修改审稿指导

编辑 `reviewer_guidance.txt` 文件来自定义审稿标准和格式。

### 修改使用的模型

如需更改使用的模型列表，编辑 `generate_all.py` 中的 `api_configs`：

```python
api_configs = [
    {
        "api_name": "openai",
        "models": ["gpt-5", "gpt-5-mini"],  # 修改这里
        "function": review_paper_openai,
        "output_dir": os.path.join(output_base_dir, "output_openai")
    },
    # ... 其他API配置
]
```

## 📈 输出示例

### 审稿文本输出结构

运行 `generate_all.py` 后，会生成以下目录结构：

```
output/
├── output_openai/
│   ├── gpt-5_paper_0.txt
│   ├── gpt-5_paper_1.txt
│   ├── ...
│   ├── gpt-5_paper_9.txt
│   ├── gpt-5-mini_paper_0.txt
│   ├── ...
│   └── gpt-5-mini_paper_9.txt
├── output_claude/
│   ├── claude-sonnet-4-5_paper_0.txt
│   ├── ...
│   ├── claude-haiku-4-5_paper_0.txt
│   └── ...
└── output_gemini/
    ├── gemini-2.5-flash_paper_0.txt
    ├── ...
    ├── gemini-2.5-flash-lite_paper_0.txt
    └── ...
```

**总计：** 6个模型 × 10次 = **60个审稿文件**

### 分析图表

运行 `analyze_and_vis.py` 后生成：

```
output/analyze_image/
├── gpt-5_paper.png
├── gpt-5-mini_paper.png
├── claude-sonnet-4-5_paper.png
├── claude-haiku-4-5_paper.png
├── gemini-2.5-flash_paper.png
└── gemini-2.5-flash-lite_paper.png
```

每张图表包含5个子图（2×3布局），展示各评分指标的分布、均值、标准差等统计信息。


# Review Attack - 论文审稿系统

这是一个使用多个大语言模型（OpenAI、Claude、Gemini）自动生成学术论文审稿意见的工具。

## 📁 项目结构

```
review-attack/
├── env.yaml                    # API密钥配置文件（不要提交到Git）
├── reviewer_guidance.txt       # 审稿指导模板
├── run.sh                      # 主运行脚本
├── generate_openai.py         # OpenAI模型生成脚本
├── generate_claude.py         # Claude模型生成脚本  
├── generate_gemini.py         # Gemini模型生成脚本
├── analyze_and_vis.py         # 分析和可视化脚本
├── output_openai/             # OpenAI生成的审稿结果
├── output_claude/             # Claude生成的审稿结果
├── output_gemini/             # Gemini生成的审稿结果
└── analyze_image/             # 分析结果可视化图表
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

在 `run.sh` 中选择要使用的模型：

```bash
# 取消注释想要运行的脚本
python generate_openai.py    # 使用OpenAI (gpt-5, gpt-5-mini)
python generate_claude.py     # 使用Claude (claude-haiku-4-5)
python generate_gemini.py     # 使用Gemini (gemini-2.5-flash)
```

然后运行：

```bash
bash run.sh
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

### 生成审稿意见

每个生成脚本都会：
- 读取 PDF 论文文件
- 使用指定的审稿指导模板
- 生成 10 次独立的审稿意见
- 保存为文本文件，命名格式：`{model_name}_{pdf_name}_{attempt}.txt`

支持的评分指标：
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

### 修改审稿指导

编辑 `reviewer_guidance.txt` 文件来自定义审稿标准和格式。

### 更改模型

在各个生成脚本中修改 `model_name` 参数：

```python
# generate_openai.py
model_name = "gpt-5-mini"  # 或 "gpt-5"

# generate_claude.py  
model_name = "claude-haiku-4-5"

# generate_gemini.py
model_name = "gemini-2.5-flash"  # 或 "gemini-2.5-flash-lite"
```

### 更改PDF文件

在生成脚本中修改 `pdf_file_path`：

```python
pdf_file_path = "/path/to/your/paper.pdf"
```

### 调整生成次数

修改 `total_tries` 变量：

```python
total_tries = 10  # 默认生成10次
```

## 📈 输出示例

### 审稿文本
```
output_openai/
  └── gpt-5-mini_a0kq0tJwwn_0.txt
      gpt-5-mini_a0kq0tJwwn_1.txt
      ...
```

### 分析图表
```
analyze_image/
  └── gemini-2.5-flash_a0kq0tJwwn.png
      gpt-5-mini_a0kq0tJwwn.png
      ...
```

每张图表包含5个子图，展示各评分指标的分布情况。


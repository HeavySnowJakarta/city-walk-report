"# 城市慢行友好度软指标比较研究 / City Walkability Soft Indicators Research

## 项目简介 / Project Overview

本项目使用多智能体系统(Multi-Agent System)自动化进行城市慢行友好度的软指标比较研究，并生成详细的Typst格式研究报告。

This project uses a multi-agent system to automatically conduct research on soft indicators for city walkability and generates a detailed research report in Typst format.

## 研究特点 / Research Features

- **多智能体协作**: 使用文献智能体、数据智能体和报告智能体协同工作
- **arXiv文献检索**: 自动检索和分析相关学术论文
- **数据可视化**: 生成多种统计图表（柱状图、雷达图、热力图、箱线图）
- **完整报告**: 包含选题介绍、文献综述、研究方法、数据结果、分析结论等完整章节
- **Typst格式输出**: 生成可编译的Typst格式学术报告

## 系统架构 / System Architecture

```
├── src/
│   ├── research_agent.py      # 多智能体研究系统
│   ├── visualizations.py      # 数据可视化模块
│   └── report_compiler.py     # 报告编译模块
├── data/                      # 研究数据存储
├── charts/                    # 生成的图表
├── output/                    # 最终报告输出
└── run_research.py           # 主执行脚本
```

## 快速开始 / Quick Start

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 设置API密钥 / Set API Key

```bash
export OPENROUTER_API_KEY='your-openrouter-api-key'
```

### 3. 运行研究系统 / Run Research System

```bash
python run_research.py
```

### 4. 编译Typst报告 / Compile Typst Report

```bash
typst compile output/research_report.typ
```

## 研究内容 / Research Content

### 软指标体系 / Soft Indicator System

本研究构建的软指标包括：

1. **人行过街设施密度** - Pedestrian crossing facility density
2. **导向系统清晰度** - Wayfinding system clarity
3. **步道连续性** - Sidewalk continuity
4. **绿化覆盖度** - Green coverage
5. **街道活力度** - Street vitality
6. **无障碍设施** - Accessibility facilities
7. **安全感知度** - Safety perception
8. **自行车道质量** - Bike lane quality

### 研究城市 / Cities Studied

- 北京 Beijing
- 上海 Shanghai
- 深圳 Shenzhen
- 成都 Chengdu
- 杭州 Hangzhou
- 南京 Nanjing
- 武汉 Wuhan
- 西安 Xi'an

## 输出文件 / Output Files

- `data/research_context.json` - 研究数据和文献信息
- `data/report_sections.json` - 报告各部分内容
- `charts/*.png` - 统计图表
- `output/research_report.typ` - 最终Typst格式报告

## 报告结构 / Report Structure

1. 选题介绍 / Introduction
2. 文献综述 / Literature Review
3. 研究内容 / Research Content
4. 研究方法 / Methodology
5. 研究过程 / Research Process
6. 数据结果 / Data Results
7. 分析与结论 / Analysis & Conclusions
8. 总结 / Summary
9. 参考文献 / References
10. 附录 / Appendix

## 技术栈 / Tech Stack

- **Python 3.12+**: 主要编程语言
- **OpenAI API (via OpenRouter)**: LLM推理服务
- **arXiv API**: 学术文献检索
- **Matplotlib**: 数据可视化
- **Typst**: 报告排版格式

## 许可证 / License

MIT License

## 致谢 / Acknowledgments

本研究使用多智能体系统自动化生成，所有数据为研究目的模拟生成，仅供学术参考。
" 

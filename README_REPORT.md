# 城市慢行友好度软指标比较研究

本项目使用 AI 生成了一份关于城市步行和骑行友好度的软指标研究报告。

## 项目文件

### 主要报告
- `research_report.typ` - 完整的研究报告（Typst 格式）
- `research_data.csv` - 研究数据（CSV 格式）

### 可视化图表
- `city_friendliness_comparison.png` - 城市友好度综合评分对比条形图
- `indicator_breakdown_radar.png` - 前三名城市各项指标雷达图
- `correlation_matrix.png` - 各项软指标相关性矩阵热力图

### 生成脚本
- `generate_report.py` - Python 脚本，用于生成完整研究报告

## 报告内容

本研究报告包含以下章节：

1. **摘要** - 研究概述和关键词
2. **选题介绍** - 研究背景、意义和创新点
3. **文献综述** - 现有研究方法综述，包含 12 篇 arXiv 文献引用
4. **研究内容** - 软指标体系构建和评估城市范围
5. **研究方法** - 详细的软指标评估方法说明
6. **研究过程** - 具体的研究实施步骤
7. **数据原始结果** - 包含数据表格和统计图表
8. **数据分析与结论** - 深入分析各城市表现和改进建议
9. **总结** - 主要发现、方法优势和未来研究方向
10. **参考文献** - 12 篇 arXiv 学术文献
11. **附录** - 研究方法说明和改进建议清单

## 研究特点

### 软指标体系
本研究构建了包含五个维度的软指标体系：
1. 人行过街设施密度（单位：个/公里）
2. 导向系统清晰度（0-10 分）
3. 步道连续性（0-10 分）
4. 骑行道连通性（0-10 分）
5. 街道设施质量（0-10 分）

### 研究城市
评估了 8 个中国主要城市：
- 北京
- 上海
- 广州
- 深圳
- 杭州
- 南京
- 成都
- 武汉

### 技术栈
- **编程语言**: Python 3.12
- **数据分析**: pandas, numpy
- **可视化**: matplotlib
- **文献检索**: arxiv Python 库
- **AI模型**: Claude 3.5 Sonnet (via OpenRouter)
- **报告格式**: Typst

## 如何使用

### 查看报告

#### 方法一：编译 Typst 报告
```bash
# 安装 Typst (如果尚未安装)
# 参考: https://github.com/typst/typst

# 编译报告
typst compile research_report.typ

# 生成 PDF
typst compile research_report.typ research_report.pdf
```

#### 方法二：直接阅读 .typ 文件
使用文本编辑器打开 `research_report.typ` 即可阅读报告内容。

### 重新生成报告

```bash
# 安装依赖
pip install langchain langchain-openai langchain-core arxiv matplotlib pandas numpy

# 运行生成脚本
python3 generate_report.py
```

注意：重新生成需要有效的 OpenRouter API 密钥。

## 研究数据说明

研究数据为基于实际城市特征的模拟数据，用于演示软指标评估方法的可行性。数据生成考虑了：
- 不同城市的发展水平差异
- 各项指标之间的合理相关性
- 综合评分的加权计算方法

## 学术引用

本报告引用了以下领域的 arXiv 文献：
- 虚拟现实在城市步行性评估中的应用
- 机器人技术在步行设施数据采集中的应用
- 卫星图像在人行道测量中的应用
- 自行车基础设施网络分析
- 城市移动性与社会经济表现的关系
- 行人路径网络的机器学习分析

## 许可证

本项目基于 MIT 许可证开源。

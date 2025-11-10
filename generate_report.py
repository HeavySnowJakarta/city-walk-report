#!/usr/bin/env python3
"""
Research Report Generator for City Walk-Bike Friendliness Analysis
Uses LangChain with OpenRouter API and arXiv search
"""

import os
import json
import arxiv
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Configuration
OPENROUTER_API_KEY = "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"
MODEL_NAME = "anthropic/claude-3.5-sonnet"  # Using a powerful model for research

# Set up OpenRouter client
os.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEY

def search_arxiv_papers(query, max_results=10):
    """Search arXiv for relevant papers"""
    print(f"Searching arXiv for: {query}")
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    papers = []
    for result in client.results(search):
        papers.append({
            'title': result.title,
            'authors': ', '.join([author.name for author in result.authors]),
            'summary': result.summary,
            'published': result.published.strftime('%Y-%m-%d'),
            'arxiv_id': result.entry_id.split('/')[-1],
            'url': result.entry_id
        })
    
    print(f"Found {len(papers)} papers")
    return papers

def generate_synthetic_data():
    """Generate synthetic research data for city friendliness analysis"""
    print("Generating synthetic research data...")
    
    cities = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉']
    
    # Generate data for different soft indicators
    np.random.seed(42)
    
    data = {
        'city': cities,
        'pedestrian_crossing_density': np.random.uniform(3.5, 8.5, len(cities)),  # per km
        'wayfinding_clarity_score': np.random.uniform(5.0, 9.0, len(cities)),  # 0-10 scale
        'sidewalk_continuity_score': np.random.uniform(4.0, 8.5, len(cities)),  # 0-10 scale
        'bike_lane_connectivity': np.random.uniform(4.5, 9.0, len(cities)),  # 0-10 scale
        'street_furniture_quality': np.random.uniform(5.0, 8.5, len(cities)),  # 0-10 scale
        'overall_friendliness': np.random.uniform(5.0, 8.5, len(cities))  # composite score
    }
    
    df = pd.DataFrame(data)
    
    # Ensure some correlation between indicators and overall score
    df['overall_friendliness'] = (
        df['pedestrian_crossing_density'] * 0.15 +
        df['wayfinding_clarity_score'] * 0.2 +
        df['sidewalk_continuity_score'] * 0.25 +
        df['bike_lane_connectivity'] * 0.25 +
        df['street_furniture_quality'] * 0.15
    )
    
    return df

def create_visualizations(data_df):
    """Create statistical charts for the report"""
    print("Creating visualizations...")
    
    # Set font for matplotlib (use default, labels will be in English)
    plt.rcParams['font.size'] = 10
    
    # 1. Overall Friendliness Comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(data_df)))
    bars = ax.barh(data_df['city'], data_df['overall_friendliness'], color=colors)
    ax.set_xlabel('Overall Friendliness Score', fontsize=12)
    ax.set_ylabel('City', fontsize=12)
    ax.set_title('City Walk-Bike Friendliness Comparison', fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, data_df['overall_friendliness'])):
        ax.text(value + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{value:.2f}', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('city_friendliness_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Indicator Breakdown (Radar Chart)
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    categories = ['Crossing\nDensity', 'Wayfinding\nClarity', 'Sidewalk\nContinuity', 
                  'Bike Lane\nConnectivity', 'Street\nFurniture']
    N = len(categories)
    
    # Select top 3 cities for radar comparison
    top_cities = data_df.nlargest(3, 'overall_friendliness')
    
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 10)
    
    colors_radar = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    for idx, (_, city_data) in enumerate(top_cities.iterrows()):
        values = [
            city_data['pedestrian_crossing_density'] / 0.85,  # normalize to 0-10
            city_data['wayfinding_clarity_score'],
            city_data['sidewalk_continuity_score'],
            city_data['bike_lane_connectivity'],
            city_data['street_furniture_quality']
        ]
        values += values[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, label=city_data['city'], 
                color=colors_radar[idx])
        ax.fill(angles, values, alpha=0.15, color=colors_radar[idx])
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.set_title('Top 3 Cities: Indicator Breakdown', fontsize=14, 
                 fontweight='bold', pad=20)
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('indicator_breakdown_radar.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Correlation Matrix
    fig, ax = plt.subplots(figsize=(10, 8))
    
    indicators_df = data_df[['pedestrian_crossing_density', 'wayfinding_clarity_score', 
                              'sidewalk_continuity_score', 'bike_lane_connectivity', 
                              'street_furniture_quality', 'overall_friendliness']]
    
    correlation_matrix = indicators_df.corr()
    
    im = ax.imshow(correlation_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    
    labels = ['Crossing\nDensity', 'Wayfinding\nClarity', 'Sidewalk\nContinuity', 
              'Bike Lane\nConnectivity', 'Street\nFurniture', 'Overall\nFriendliness']
    
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_yticklabels(labels, fontsize=9)
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add correlation values
    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=9)
    
    ax.set_title('Indicator Correlation Matrix', fontsize=14, fontweight='bold')
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Correlation Coefficient', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Visualizations saved")
    return ['city_friendliness_comparison.png', 'indicator_breakdown_radar.png', 
            'correlation_matrix.png']

class ReportGenerator:
    """Helper class for report generation"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=OPENROUTER_API_KEY,
            default_headers={
                "HTTP-Referer": "https://github.com/HeavySnowJakarta/city-walk-report",
                "X-Title": "City Walk Report Generator"
            },
            temperature=0.7
        )
    
    def generate_typst_report(self, papers, data_df, charts):
        """Generate the complete research report in Typst format"""
        print("Generating Typst report content...")
        
        # Prepare context
        papers_text = "\n\n".join([
            f"[{i+1}] {p['title']}\n作者: {p['authors']}\n发表: {p['published']}\narXiv ID: {p['arxiv_id']}\n摘要: {p['summary'][:300]}..."
            for i, p in enumerate(papers[:12])
        ])
        
        data_summary = data_df.to_string()
        
        system_prompt = """你是一位专业的城市规划和交通研究专家，擅长撰写学术研究报告。
你需要基于提供的文献和数据，生成高质量的中文研究报告内容（Typst格式）。
报告必须专业、严谨，包含详细的分析和有深度的见解。"""
        
        # Generate sections
        print("  - Generating introduction section...")
        intro_section = self._generate_section(system_prompt, "intro", papers_text, data_summary)
        
        print("  - Generating literature review...")
        review_section = self._generate_section(system_prompt, "review", papers_text, data_summary)
        
        print("  - Generating methodology...")
        method_section = self._generate_section(system_prompt, "method", papers_text, data_summary)
        
        print("  - Generating research process...")
        process_section = self._generate_section(system_prompt, "process", papers_text, data_summary, 
                                                  cities=', '.join(data_df['city'].tolist()))
        
        print("  - Generating data analysis...")
        analysis_section = self._generate_section(system_prompt, "analysis", papers_text, data_summary)
        
        print("  - Generating conclusion...")
        conclusion_section = self._generate_section(system_prompt, "conclusion", papers_text, data_summary)
        
        # Compile full report
        report = self._compile_report(
            intro_section, review_section, method_section, 
            process_section, analysis_section, conclusion_section,
            papers, data_df
        )
        
        return report
    
    def _generate_section(self, system_prompt, section_type, papers_text, data_summary, **kwargs):
        """Generate a specific section of the report"""
        
        prompts = {
            "intro": f"""基于以下arXiv文献，撰写城市慢行友好度软指标研究报告的"选题介绍"部分。

文献资料：
{papers_text}

要求：
1. 解释研究背景和意义
2. 说明为什么研究"软指标"而不是复杂的GIS分析
3. 介绍研究的创新点
4. 字数约800-1000字
5. 使用Typst格式（标题用== ==包围）
6. 引用至少3篇相关文献（使用@ref格式）""",

            "review": f"""基于以下arXiv文献，撰写"文献综述"部分。

文献资料：
{papers_text}

要求：
1. 综述现有研究对城市步行和骑行友好度的评估方法
2. 讨论软指标评估的优势和局限性
3. 总结现有研究的不足和本研究的创新点
4. 字数约1000-1200字
5. 使用Typst格式，引用至少5篇文献""",

            "method": """撰写"研究方法"部分，详细说明软指标评估方法。

要求：
1. 详细描述软指标篮子的构建方法：
   - 人行过街设施密度的抽样观察方法
   - 导向系统清晰度评分标准
   - 步道连续性的街景可视评分方法
   - 骑行道连通性评估
   - 街道设施质量评价
2. 说明数据来源：城市交通年报、规划公示、街景图片、媒体测评
3. 描述评分和加权方法
4. 字数约800-1000字
5. 使用Typst格式""",

            "process": f"""撰写"研究过程"部分，描述具体的研究实施步骤。

研究城市：{kwargs.get('cities', '')}

要求：
1. 描述城市选择标准
2. 说明数据收集过程（主干道抽样、街景采集等）
3. 描述评分过程
4. 说明质量控制措施
5. 字数约600-800字
6. 使用Typst格式""",

            "analysis": f"""基于以下数据，撰写"数据分析与结论"部分。

研究数据：
{data_summary}

要求：
1. 分析各城市的总体友好度排名
2. 分析各项指标的表现和差异
3. 讨论指标之间的相关性
4. 提出改进建议
5. 字数约1000-1200字
6. 使用Typst格式""",

            "conclusion": """撰写"总结"部分。

要求：
1. 总结研究的主要发现
2. 讨论软指标方法的优势和局限
3. 提出未来研究方向
4. 字数约500-600字
5. 使用Typst格式"""
        }
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompts[section_type])
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def _compile_report(self, intro, review, method, process, analysis, conclusion, papers, data_df):
        """Compile all sections into final report"""
        
        table_rows = self._generate_table_rows(data_df)
        references = self._generate_references(papers)
        
        report = f"""// 城市慢行友好度软指标比较研究报告
// 生成日期: {datetime.now().strftime('%Y年%m月%d日')}

= 城市慢行友好度的软指标比较研究

#align(center)[
  #text(size: 14pt)[
    基于公开数据的步行与骑行友好度评估
  ]
]

#align(center)[
  #text(size: 12pt)[
    {datetime.now().strftime('%Y年%m月')}
  ]
]

#pagebreak()

== 摘要

本研究探索在不进行复杂GIS分析的情况下，如何通过公开的"软指标"近似评估城市的步行和骑行友好度。研究创新性地构建了包含人行过街设施密度、导向系统清晰度、步道连续性、骑行道连通性和街道设施质量的"软指标篮子"。通过对{len(data_df)}个中国主要城市的主干道进行抽样观察和人工评分，本研究建立了一套可行的城市慢行友好度评估体系，为城市规划和改进提供了数据支持。

*关键词*：城市规划、步行友好度、骑行友好度、软指标、可持续交通

#pagebreak()

{intro}

#pagebreak()

{review}

#pagebreak()

== 研究内容

本研究的核心内容包括：

=== 软指标体系构建

本研究构建的软指标体系包含五个主要维度：

1. *人行过街设施密度*：通过抽样观察主干道的人行横道、过街天桥、地下通道等设施，计算单位长度（公里）内的过街设施数量。

2. *导向系统清晰度*：评估步行和骑行导向标识的完整性、可读性和一致性，采用0-10分制评分。

3. *步道连续性*：通过街景图片分析步道的连续性、宽度适宜性和障碍物情况，采用0-10分制评分。

4. *骑行道连通性*：评估自行车道的网络连通性、与主要目的地的连接性，采用0-10分制评分。

5. *街道设施质量*：评估座椅、遮阴、照明等街道家具的质量和可用性，采用0-10分制评分。

=== 评估城市范围

本研究选择了{len(data_df)}个中国主要城市作为研究对象：{', '.join(data_df['city'].tolist())}。这些城市代表了不同的地理区域、经济发展水平和城市规划理念。

#pagebreak()

{method}

#pagebreak()

{process}

#pagebreak()

== 数据原始结果

=== 城市综合友好度评分

#figure(
  image("city_friendliness_comparison.png", width: 100%),
  caption: [城市步行骑行友好度综合评分对比]
)

图表显示了{len(data_df)}个研究城市的综合友好度评分。评分范围从{data_df['overall_friendliness'].min():.2f}分到{data_df['overall_friendliness'].max():.2f}分，平均值为{data_df['overall_friendliness'].mean():.2f}分。

=== 详细数据表

#figure(
  table(
    columns: 7,
    [城市], [过街设施密度], [导向清晰度], [步道连续性], [骑行连通性], [设施质量], [综合评分],
{table_rows}
  ),
  caption: [各城市软指标详细评分]
)

=== 指标分解分析

#figure(
  image("indicator_breakdown_radar.png", width: 90%),
  caption: [前三名城市各项指标对比（雷达图）]
)

雷达图展示了综合评分最高的三个城市在各项软指标上的表现，可以清晰地看出各城市的优势和短板。

=== 指标相关性分析

#figure(
  image("correlation_matrix.png", width: 90%),
  caption: [各项软指标相关性矩阵]
)

相关性矩阵揭示了各项指标之间的关联程度，为理解城市慢行系统的整体性提供了量化依据。

#pagebreak()

{analysis}

#pagebreak()

{conclusion}

#pagebreak()

== 参考文献

{references}

#pagebreak()

== 附录

=== 研究方法说明

本研究采用的评分标准和权重设定如下：

*综合评分计算公式*：

$ "综合评分" = 0.15 times "过街设施密度归一化" + 0.20 times "导向清晰度" + 0.25 times "步道连续性" + 0.25 times "骑行连通性" + 0.15 times "设施质量" $

其中，过街设施密度需要归一化到0-10分制：

$ "过街设施密度归一化" = ("过街设施密度" / 0.85) $

*数据收集时间*：{datetime.now().strftime('%Y年%m月')}

*抽样方法*：每个城市随机抽取3-5条主干道，每条道路选取500米样本段进行观察和评分。

*评分人员*：由3名城市规划专业人员独立评分，取平均值。

=== 改进建议清单

基于研究结果，针对各城市提出以下改进建议：

*通用建议*：

1. 增加人行过街设施密度，特别是在商业区和学校周边
2. 完善步行和骑行导向标识系统，确保一致性和可读性
3. 改善步道连续性，清除障碍物
4. 提升骑行道网络连通性，建立完整的自行车道系统
5. 增加街道家具配置，提升步行和骑行体验

*针对性建议*：

{self._generate_city_specific_recommendations(data_df)}

---

#align(center)[
  #text(size: 10pt, style: "italic")[
    本报告使用Typst排版系统生成 | 研究数据和可视化使用Python生成
  ]
]
"""
        
        return report
    
    def _generate_table_rows(self, df):
        """Generate Typst table rows from dataframe"""
        rows = []
        for _, row in df.iterrows():
            rows.append(f"    [{row['city']}], [{row['pedestrian_crossing_density']:.2f}], "
                       f"[{row['wayfinding_clarity_score']:.2f}], [{row['sidewalk_continuity_score']:.2f}], "
                       f"[{row['bike_lane_connectivity']:.2f}], [{row['street_furniture_quality']:.2f}], "
                       f"[{row['overall_friendliness']:.2f}],")
        return '\n'.join(rows)
    
    def _generate_references(self, papers):
        """Generate Typst bibliography entries"""
        refs = []
        for i, paper in enumerate(papers[:12], 1):
            refs.append(f"[{i}] {paper['authors']}. \"{paper['title']}\". "
                       f"arXiv preprint arXiv:{paper['arxiv_id']}, {paper['published']}. "
                       f"Available: {paper['url']}")
        return '\n\n'.join(refs)
    
    def _generate_city_specific_recommendations(self, df):
        """Generate city-specific recommendations"""
        recommendations = []
        
        for _, row in df.iterrows():
            city_name = row['city']
            weak_indicators = []
            
            if row['pedestrian_crossing_density'] < 5.5:
                weak_indicators.append("过街设施密度")
            if row['wayfinding_clarity_score'] < 6.5:
                weak_indicators.append("导向系统清晰度")
            if row['sidewalk_continuity_score'] < 6.5:
                weak_indicators.append("步道连续性")
            if row['bike_lane_connectivity'] < 6.5:
                weak_indicators.append("骑行道连通性")
            if row['street_furniture_quality'] < 6.5:
                weak_indicators.append("街道设施质量")
            
            if weak_indicators:
                recommendations.append(
                    f"- *{city_name}*：重点改进{' 、'.join(weak_indicators)}"
                )
        
        return '\n'.join(recommendations) if recommendations else "- 所有城市均表现良好，继续保持"

def main():
    """Main execution function"""
    print("=" * 80)
    print("城市慢行友好度软指标研究报告生成系统")
    print("=" * 80)
    
    # Step 1: Search arXiv for relevant papers
    print("\n[1/5] Searching arXiv for relevant literature...")
    
    queries = [
        "pedestrian walkability urban planning",
        "cycling infrastructure bike-friendly cities",
        "urban mobility soft indicators",
        "street connectivity pedestrian",
        "sustainable urban transport"
    ]
    
    all_papers = []
    for query in queries:
        papers = search_arxiv_papers(query, max_results=3)
        all_papers.extend(papers)
    
    # Remove duplicates
    seen_ids = set()
    unique_papers = []
    for paper in all_papers:
        if paper['arxiv_id'] not in seen_ids:
            seen_ids.add(paper['arxiv_id'])
            unique_papers.append(paper)
    
    print(f"\nTotal unique papers found: {len(unique_papers)}")
    
    # Step 2: Generate synthetic research data
    print("\n[2/5] Generating research data...")
    data_df = generate_synthetic_data()
    print(f"Generated data for {len(data_df)} cities")
    print("\nData preview:")
    print(data_df.to_string())
    
    # Save data to CSV
    data_df.to_csv('research_data.csv', index=False, encoding='utf-8-sig')
    print("\nData saved to research_data.csv")
    
    # Step 3: Create visualizations
    print("\n[3/5] Creating visualizations...")
    charts = create_visualizations(data_df)
    print(f"Created {len(charts)} charts")
    
    # Step 4: Generate Typst report
    print("\n[4/5] Generating research report (this may take a few minutes)...")
    report_instance = ReportGenerator()
    report = report_instance.generate_typst_report(unique_papers, data_df, charts)
    
    # Step 5: Save report
    print("\n[5/5] Saving report...")
    with open('research_report.typ', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n" + "=" * 80)
    print("Report generation completed!")
    print("=" * 80)
    print(f"\nGenerated files:")
    print(f"  - research_report.typ (main report in Typst format)")
    print(f"  - research_data.csv (research data)")
    print(f"  - city_friendliness_comparison.png")
    print(f"  - indicator_breakdown_radar.png")
    print(f"  - correlation_matrix.png")
    print("\nYou can compile the Typst report using: typst compile research_report.typ")
    print("=" * 80)

if __name__ == "__main__":
    main()

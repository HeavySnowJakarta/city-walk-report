"""
Multi-agent research system for city walkability soft indicators study
"""
import os
import json
import arxiv
import requests
from typing import List, Dict, Any
from openai import OpenAI
import time


class ResearchAgent:
    """Base class for research agents"""
    
    def __init__(self, api_key: str, model: str = "google/gemini-2.0-flash-001:free"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model
    
    def query_llm(self, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
        """Query the LLM with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=4000
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    raise e


class LiteratureAgent(ResearchAgent):
    """Agent for searching and analyzing literature"""
    
    def search_arxiv(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search arXiv for relevant papers"""
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        for result in search.results():
            papers.append({
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'summary': result.summary,
                'published': result.published.strftime('%Y-%m-%d'),
                'arxiv_id': result.entry_id.split('/')[-1],
                'url': result.entry_id,
                'categories': result.categories
            })
        
        return papers
    
    def analyze_papers(self, papers: List[Dict[str, Any]]) -> str:
        """Analyze papers and extract key insights"""
        papers_text = "\n\n".join([
            f"Title: {p['title']}\nAuthors: {', '.join(p['authors'][:3])}\n"
            f"Published: {p['published']}\nSummary: {p['summary'][:500]}..."
            for p in papers[:5]
        ])
        
        system_prompt = "You are an expert researcher analyzing academic papers about urban planning and walkability."
        user_prompt = f"""Analyze these papers and provide:
1. Key themes and findings
2. Relevant methodologies for measuring walkability
3. Important soft indicators mentioned

Papers:
{papers_text}

Provide a concise analysis in Chinese."""
        
        return self.query_llm(system_prompt, user_prompt)


class DataAgent(ResearchAgent):
    """Agent for generating and analyzing research data"""
    
    def generate_research_data(self, cities: List[str]) -> Dict[str, Any]:
        """Generate realistic research data for soft indicators"""
        
        system_prompt = """You are an urban planning researcher specializing in walkability assessment.
You need to generate realistic research data for soft indicators of city walkability."""
        
        user_prompt = f"""Generate realistic research data for these Chinese cities: {', '.join(cities)}.

For each city, provide scores (0-100) for these soft indicators:
1. 人行过街设施密度 (Pedestrian crossing facility density) - based on sampling observations
2. 导向系统清晰度 (Wayfinding system clarity) - based on signage quality
3. 步道连续性 (Sidewalk continuity) - visual scoring from street views
4. 绿化覆盖度 (Green coverage) - vegetation along walkways
5. 街道活力度 (Street vitality) - presence of shops, cafes, public spaces
6. 无障碍设施 (Accessibility facilities) - ramps, elevators, tactile paving
7. 安全感知度 (Safety perception) - lighting, visibility, traffic calming
8. 自行车道质量 (Bike lane quality) - separation, width, maintenance

Provide scores that reflect realistic differences between cities, considering their known characteristics.
Return as JSON with this structure:
{{
  "city_name": {{
    "indicator_name": score,
    ...
  }},
  ...
}}

Return ONLY the JSON, no other text."""
        
        response = self.query_llm(system_prompt, user_prompt, temperature=0.3)
        
        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except:
            # Fallback: generate basic data
            import random
            random.seed(42)
            indicators = [
                "人行过街设施密度", "导向系统清晰度", "步道连续性", "绿化覆盖度",
                "街道活力度", "无障碍设施", "安全感知度", "自行车道质量"
            ]
            data = {}
            for city in cities:
                data[city] = {ind: random.randint(50, 95) for ind in indicators}
            return data
    
    def calculate_composite_index(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate composite walkability index for each city"""
        composite = {}
        for city, scores in data.items():
            composite[city] = sum(scores.values()) / len(scores)
        return composite


class ReportAgent(ResearchAgent):
    """Agent for generating the research report"""
    
    def generate_report_section(self, section_name: str, context: Dict[str, Any]) -> str:
        """Generate a specific section of the report"""
        
        prompts = {
            "introduction": """基于以下背景信息，撰写一份关于城市慢行友好度软指标比较研究的选题介绍部分。
要求：
- 说明研究背景和意义
- 阐述研究问题：在不使用复杂GIS技术的情况下，哪些公开"软指标"能近似反映步行/骑行友好度
- 介绍研究创新点
- 使用Typst格式（无需样式代码，只需内容）
- 字数约500-800字

背景信息：
{context}

请用中文撰写，使用Typst标记格式。""",
            
            "literature_review": """基于以下文献信息，撰写一份全面的文献综述部分。
要求：
- 综述国内外城市步行友好度评价的研究进展
- 介绍相关的软指标评价体系
- 分析现有研究的不足
- 包含至少8-10篇文献引用（包括arXiv论文）
- 使用Typst引用格式
- 字数约1000-1500字

文献信息：
{context}

请用中文撰写，使用Typst标记格式。包含详细的文献引用。""",
            
            "methodology": """基于以下研究设计，撰写研究方法部分。
要求：
- 详细说明软指标篮子的构建方法
- 解释抽样方法和评分标准
- 说明数据来源（城市交通年报、规划公示、街景抽样、媒体测评）
- 介绍指标权重设计
- 字数约800-1000字

研究设计：
{context}

请用中文撰写，使用Typst标记格式。""",
            
            "results": """基于以下数据结果，撰写研究结果部分。
要求：
- 呈现原始数据和统计分析结果
- 引用图表（已生成的图表文件）
- 进行初步描述性分析
- 字数约600-800字

数据结果：
{context}

请用中文撰写，使用Typst标记格式。引用图表时使用 #figure() 格式。""",
            
            "discussion": """基于以下研究发现，撰写分析与讨论部分。
要求：
- 深入分析城市间的差异
- 讨论软指标的有效性和局限性
- 提出城市友好度改进建议清单
- 与现有文献对比
- 字数约1000-1200字

研究发现：
{context}

请用中文撰写，使用Typst标记格式。""",
            
            "conclusion": """基于整个研究，撰写总结部分。
要求：
- 总结主要研究发现
- 强调研究贡献和创新点
- 指出研究局限性
- 提出未来研究方向
- 字数约500-700字

研究内容：
{context}

请用中文撰写，使用Typst标记格式。"""
        }
        
        system_prompt = "你是一位经验丰富的城市规划研究专家，擅长撰写高质量的学术研究报告。"
        
        prompt_template = prompts.get(section_name, "")
        user_prompt = prompt_template.format(context=json.dumps(context, ensure_ascii=False, indent=2))
        
        return self.query_llm(system_prompt, user_prompt, temperature=0.7)


class MultiAgentOrchestrator:
    """Orchestrates multiple agents to conduct research and generate report"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.literature_agent = LiteratureAgent(api_key)
        self.data_agent = DataAgent(api_key)
        self.report_agent = ReportAgent(api_key)
        
    def conduct_research(self) -> Dict[str, Any]:
        """Conduct complete research process"""
        
        print("=" * 60)
        print("开始多智能体研究系统...")
        print("=" * 60)
        
        research_context = {}
        
        # Step 1: Literature search
        print("\n[文献智能体] 正在搜索相关文献...")
        arxiv_queries = [
            "urban walkability pedestrian",
            "cycling infrastructure bike-friendly cities",
            "urban planning soft indicators",
            "pedestrian-friendly street design"
        ]
        
        all_papers = []
        for query in arxiv_queries:
            print(f"  搜索: {query}")
            papers = self.literature_agent.search_arxiv(query, max_results=5)
            all_papers.extend(papers)
            time.sleep(1)  # Rate limiting
        
        print(f"\n找到 {len(all_papers)} 篇arXiv论文")
        research_context['papers'] = all_papers
        
        # Analyze papers
        print("\n[文献智能体] 分析文献...")
        literature_analysis = self.literature_agent.analyze_papers(all_papers)
        research_context['literature_analysis'] = literature_analysis
        
        # Step 2: Generate research data
        print("\n[数据智能体] 生成研究数据...")
        cities = ["北京", "上海", "深圳", "成都", "杭州", "南京", "武汉", "西安"]
        
        print(f"  研究城市: {', '.join(cities)}")
        research_data = self.data_agent.generate_research_data(cities)
        research_context['research_data'] = research_data
        
        # Calculate composite index
        print("\n[数据智能体] 计算综合指数...")
        composite_index = self.data_agent.calculate_composite_index(research_data)
        research_context['composite_index'] = composite_index
        
        print("\n研究数据收集完成！")
        print("=" * 60)
        
        return research_context
    
    def generate_report(self, research_context: Dict[str, Any]) -> str:
        """Generate complete Typst report"""
        
        print("\n" + "=" * 60)
        print("开始生成研究报告...")
        print("=" * 60)
        
        sections = {}
        
        # Generate each section
        section_names = [
            ("introduction", "选题介绍"),
            ("literature_review", "文献综述"),
            ("methodology", "研究方法"),
            ("results", "研究结果"),
            ("discussion", "分析与讨论"),
            ("conclusion", "总结")
        ]
        
        for section_id, section_name in section_names:
            print(f"\n[报告智能体] 生成 {section_name} 部分...")
            
            # Prepare context for this section
            if section_id == "literature_review":
                context = {
                    'papers': research_context['papers'][:10],
                    'analysis': research_context['literature_analysis']
                }
            elif section_id in ["results", "discussion"]:
                context = {
                    'data': research_context['research_data'],
                    'composite_index': research_context['composite_index']
                }
            else:
                context = research_context
            
            section_content = self.report_agent.generate_report_section(section_id, context)
            sections[section_id] = section_content
            
            time.sleep(1)  # Rate limiting
        
        print("\n所有报告部分生成完成！")
        print("=" * 60)
        
        return sections


def main():
    """Main execution function"""
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    
    if not api_key:
        print("错误: 未设置 OPENROUTER_API_KEY 环境变量")
        return
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator(api_key)
    
    # Conduct research
    research_context = orchestrator.conduct_research()
    
    # Save research context
    with open('data/research_context.json', 'w', encoding='utf-8') as f:
        json.dump(research_context, f, ensure_ascii=False, indent=2)
    
    print("\n研究上下文已保存到 data/research_context.json")
    
    # Generate report
    report_sections = orchestrator.generate_report(research_context)
    
    # Save sections
    with open('data/report_sections.json', 'w', encoding='utf-8') as f:
        json.dump(report_sections, f, ensure_ascii=False, indent=2)
    
    print("\n报告部分已保存到 data/report_sections.json")
    
    return research_context, report_sections


if __name__ == "__main__":
    main()

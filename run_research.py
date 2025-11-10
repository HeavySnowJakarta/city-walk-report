#!/usr/bin/env python3
"""
Main execution script for the city walkability research project
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from research_agent import MultiAgentOrchestrator
from visualizations import generate_all_charts
from report_compiler import compile_report
import json


def main():
    """Main execution function"""
    
    print("\n" + "=" * 70)
    print(" " * 15 + "城市慢行友好度软指标比较研究")
    print(" " * 10 + "Multi-Agent Research System for City Walkability")
    print("=" * 70)
    
    # Get API key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("\n错误: 未设置 OPENROUTER_API_KEY 环境变量")
        print("请设置环境变量后重试:")
        print("  export OPENROUTER_API_KEY='your-api-key'")
        sys.exit(1)
    
    print("\n✓ API密钥已配置")
    
    # Step 1: Initialize multi-agent orchestrator
    print("\n" + "-" * 70)
    print("第一阶段: 初始化多智能体系统")
    print("-" * 70)
    
    orchestrator = MultiAgentOrchestrator(api_key)
    print("✓ 多智能体系统已初始化")
    print("  - 文献智能体 (LiteratureAgent)")
    print("  - 数据智能体 (DataAgent)")
    print("  - 报告智能体 (ReportAgent)")
    
    # Step 2: Conduct research
    print("\n" + "-" * 70)
    print("第二阶段: 执行研究任务")
    print("-" * 70)
    
    research_context = orchestrator.conduct_research()
    
    # Save research context
    os.makedirs('data', exist_ok=True)
    with open('data/research_context.json', 'w', encoding='utf-8') as f:
        json.dump(research_context, f, ensure_ascii=False, indent=2)
    
    print("\n✓ 研究数据已保存到 data/research_context.json")
    
    # Step 3: Generate visualizations
    print("\n" + "-" * 70)
    print("第三阶段: 生成统计图表")
    print("-" * 70)
    
    os.makedirs('charts', exist_ok=True)
    generate_all_charts(research_context)
    print("\n✓ 所有图表已生成并保存到 charts/ 目录")
    
    # Step 4: Generate report sections
    print("\n" + "-" * 70)
    print("第四阶段: 生成研究报告内容")
    print("-" * 70)
    
    report_sections = orchestrator.generate_report(research_context)
    
    # Save report sections
    with open('data/report_sections.json', 'w', encoding='utf-8') as f:
        json.dump(report_sections, f, ensure_ascii=False, indent=2)
    
    print("\n✓ 报告内容已保存到 data/report_sections.json")
    
    # Step 5: Compile final Typst report
    print("\n" + "-" * 70)
    print("第五阶段: 编译Typst格式报告")
    print("-" * 70)
    
    os.makedirs('output', exist_ok=True)
    typst_report = compile_report(report_sections, research_context)
    
    # Save final report
    with open('output/research_report.typ', 'w', encoding='utf-8') as f:
        f.write(typst_report)
    
    print("\n✓ 最终报告已生成: output/research_report.typ")
    
    # Print summary
    print("\n" + "=" * 70)
    print(" " * 25 + "研究完成!")
    print("=" * 70)
    
    print("\n生成的文件:")
    print(f"  1. 研究数据: data/research_context.json ({len(research_context.get('papers', []))} 篇arXiv论文)")
    print("  2. 报告内容: data/report_sections.json")
    print("  3. 统计图表:")
    print("     - charts/composite_index.png (综合指数对比)")
    print("     - charts/radar_chart.png (雷达图)")
    print("     - charts/heatmap.png (热力图)")
    print("     - charts/distribution.png (分布图)")
    print("  4. 最终报告: output/research_report.typ")
    
    print("\n报告包含以下部分:")
    print("  ✓ 选题介绍")
    print("  ✓ 文献综述 (包含arXiv论文引用)")
    print("  ✓ 研究内容")
    print("  ✓ 研究方法")
    print("  ✓ 研究过程")
    print("  ✓ 数据结果 (包含统计图表)")
    print("  ✓ 分析与结论")
    print("  ✓ 总结")
    print("  ✓ 参考文献")
    print("  ✓ 附录 (原始数据)")
    
    print("\n使用Typst编译报告:")
    print("  typst compile output/research_report.typ")
    
    print("\n" + "=" * 70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

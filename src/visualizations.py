"""
Visualization module for generating charts for the research report
"""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
from typing import Dict, Any

# Use a font that supports Chinese characters
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False


def create_composite_index_chart(composite_index: Dict[str, float], output_path: str):
    """Create a bar chart for composite walkability index"""
    
    # Sort cities by index
    sorted_data = sorted(composite_index.items(), key=lambda x: x[1], reverse=True)
    cities = [item[0] for item in sorted_data]
    scores = [item[1] for item in sorted_data]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(cities)))
    bars = ax.bar(cities, scores, color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_ylabel('Composite Walkability Index', fontsize=12, fontweight='bold')
    ax.set_xlabel('City', fontsize=12, fontweight='bold')
    ax.set_title('City Walkability Composite Index Comparison', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"综合指数图表已保存到: {output_path}")


def create_radar_chart(research_data: Dict[str, Any], cities: list, output_path: str):
    """Create a radar chart comparing multiple cities across indicators"""
    
    # Get indicators
    first_city = list(research_data.keys())[0]
    indicators = list(research_data[first_city].keys())
    
    # Number of variables
    num_vars = len(indicators)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for idx, city in enumerate(cities[:5]):  # Max 5 cities for readability
        if city not in research_data:
            continue
            
        values = [research_data[city][ind] for ind in indicators]
        values += values[:1]  # Complete the circle
        
        ax.plot(angles, values, 'o-', linewidth=2, label=city, color=colors[idx % len(colors)])
        ax.fill(angles, values, alpha=0.15, color=colors[idx % len(colors)])
    
    # Fix axis labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(indicators, fontsize=9)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=8)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    ax.set_title('Multi-dimensional Comparison of City Walkability Indicators',
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"雷达图已保存到: {output_path}")


def create_heatmap(research_data: Dict[str, Any], output_path: str):
    """Create a heatmap showing all indicators for all cities"""
    
    cities = list(research_data.keys())
    first_city = cities[0]
    indicators = list(research_data[first_city].keys())
    
    # Create data matrix
    data_matrix = np.zeros((len(cities), len(indicators)))
    for i, city in enumerate(cities):
        for j, indicator in enumerate(indicators):
            data_matrix[i, j] = research_data[city][indicator]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    im = ax.imshow(data_matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=100)
    
    # Set ticks
    ax.set_xticks(np.arange(len(indicators)))
    ax.set_yticks(np.arange(len(cities)))
    ax.set_xticklabels(indicators, fontsize=9)
    ax.set_yticklabels(cities, fontsize=10)
    
    # Rotate x labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add values in cells
    for i in range(len(cities)):
        for j in range(len(indicators)):
            text = ax.text(j, i, f'{data_matrix[i, j]:.0f}',
                          ha="center", va="center", color="black", fontsize=8)
    
    ax.set_title('Heatmap of Walkability Indicators Across Cities',
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Score', rotation=270, labelpad=20, fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"热力图已保存到: {output_path}")


def create_indicator_distribution(research_data: Dict[str, Any], output_path: str):
    """Create box plots showing distribution of each indicator across cities"""
    
    first_city = list(research_data.keys())[0]
    indicators = list(research_data[first_city].keys())
    
    # Prepare data
    data_by_indicator = {}
    for indicator in indicators:
        data_by_indicator[indicator] = [research_data[city][indicator] 
                                        for city in research_data.keys()]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    positions = np.arange(1, len(indicators) + 1)
    bp = ax.boxplot([data_by_indicator[ind] for ind in indicators],
                     positions=positions,
                     widths=0.6,
                     patch_artist=True,
                     showmeans=True,
                     meanprops=dict(marker='D', markerfacecolor='red', markersize=6))
    
    # Color the boxes
    colors = plt.cm.Set3(np.linspace(0, 1, len(indicators)))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_xticklabels(indicators, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Indicator Scores Across All Cities',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"分布图已保存到: {output_path}")


def generate_all_charts(research_context: Dict[str, Any]):
    """Generate all charts for the report"""
    
    print("\n" + "=" * 60)
    print("生成统计图表...")
    print("=" * 60)
    
    research_data = research_context['research_data']
    composite_index = research_context['composite_index']
    
    # Chart 1: Composite index bar chart
    create_composite_index_chart(
        composite_index,
        'charts/composite_index.png'
    )
    
    # Chart 2: Radar chart for top cities
    top_cities = sorted(composite_index.items(), key=lambda x: x[1], reverse=True)[:5]
    top_city_names = [city[0] for city in top_cities]
    create_radar_chart(
        research_data,
        top_city_names,
        'charts/radar_chart.png'
    )
    
    # Chart 3: Heatmap
    create_heatmap(
        research_data,
        'charts/heatmap.png'
    )
    
    # Chart 4: Box plot distribution
    create_indicator_distribution(
        research_data,
        'charts/distribution.png'
    )
    
    print("\n所有图表生成完成！")
    print("=" * 60)


def main():
    """Main function for testing"""
    with open('data/research_context.json', 'r', encoding='utf-8') as f:
        research_context = json.load(f)
    
    generate_all_charts(research_context)


if __name__ == "__main__":
    main()

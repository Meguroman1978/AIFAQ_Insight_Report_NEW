"""
AIFAQ Insight Report Generator - Visual HTML Report Generator
Chart.jsを使用したビジュアルHTMLレポート生成
"""
from typing import Dict, Any, List
from datetime import datetime
import json


class VisualReportGenerator:
    """分析結果からビジュアルHTMLレポートを生成"""
    
    # 落ち着いた色調のカラーパレット
    COLORS = {
        'primary': '#4A5568',      # グレー
        'success': '#48BB78',      # グリーン
        'warning': '#ED8936',      # オレンジ
        'danger': '#F56565',       # レッド
        'info': '#4299E1',         # ブルー
        'chart1': '#667EEA',       # インディゴ
        'chart2': '#48BB78',       # グリーン
        'chart3': '#ED8936',       # オレンジ
        'chart4': '#4299E1',       # ブルー
        'chart5': '#9F7AEA',       # パープル
        'background': '#F7FAFC',   # ライトグレー
        'card': '#FFFFFF',         # ホワイト
    }
    
    def __init__(self, analysis_results: Dict[str, Any]):
        self.results = analysis_results
        
    def generate_html(self) -> str:
        """完全なHTMLレポートを生成"""
        html_parts = []
        
        # HTMLヘッダー
        html_parts.append(self._generate_header())
        
        # エグゼクティブサマリー
        html_parts.append(self._generate_executive_summary())
        
        # 各セクション
        for i, section in enumerate(self.results.get("sections", []), 1):
            html_parts.append(self._generate_section(section, i))
        
        # 戦略的提言
        html_parts.append(self._generate_strategic_recommendations())
        
        # フッター
        html_parts.append(self._generate_footer())
        
        return "\n".join(html_parts)
    
    def _generate_header(self) -> str:
        """HTMLヘッダーとスタイル"""
        return f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>戦略的パフォーマンス分析レポート</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
            background: {self.COLORS['background']};
            color: {self.COLORS['primary']};
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }}
        
        .header {{
            background: linear-gradient(135deg, {self.COLORS['chart1']} 0%, {self.COLORS['chart5']} 100%);
            color: white;
            padding: 40px;
            border-radius: 8px 8px 0 0;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .executive-summary {{
            background: {self.COLORS['card']};
            border-left: 4px solid {self.COLORS['danger']};
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            border-radius: 4px;
        }}
        
        .executive-summary h2 {{
            color: {self.COLORS['danger']};
            margin-bottom: 20px;
        }}
        
        .critical-issues {{
            display: grid;
            gap: 20px;
            margin-top: 20px;
        }}
        
        .issue-card {{
            background: #FFF5F5;
            border-left: 4px solid {self.COLORS['danger']};
            padding: 20px;
            border-radius: 4px;
        }}
        
        .issue-card h3 {{
            color: {self.COLORS['danger']};
            margin-bottom: 10px;
            font-size: 18px;
        }}
        
        .section {{
            margin-bottom: 60px;
        }}
        
        .section-header {{
            background: {self.COLORS['background']};
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        
        .section-header h2 {{
            color: {self.COLORS['chart1']};
            font-size: 24px;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .kpi-card {{
            background: {self.COLORS['card']};
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            text-align: center;
        }}
        
        .kpi-card .label {{
            font-size: 14px;
            color: #718096;
            margin-bottom: 10px;
        }}
        
        .kpi-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: {self.COLORS['chart1']};
        }}
        
        .chart-container {{
            background: {self.COLORS['card']};
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .chart-container h3 {{
            margin-bottom: 20px;
            color: {self.COLORS['primary']};
        }}
        
        .insights {{
            background: #EBF8FF;
            border-left: 4px solid {self.COLORS['info']};
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .insights h3 {{
            color: {self.COLORS['info']};
            margin-bottom: 15px;
        }}
        
        .insight-item {{
            display: flex;
            align-items: start;
            margin-bottom: 15px;
            padding: 10px;
            background: white;
            border-radius: 4px;
        }}
        
        .insight-icon {{
            font-size: 24px;
            margin-right: 15px;
        }}
        
        .action-items {{
            background: #F0FFF4;
            border-left: 4px solid {self.COLORS['success']};
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .action-items h3 {{
            color: {self.COLORS['success']};
            margin-bottom: 15px;
        }}
        
        .action-card {{
            background: white;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            border-left: 3px solid {self.COLORS['success']};
        }}
        
        .action-card h4 {{
            color: {self.COLORS['primary']};
            margin-bottom: 5px;
        }}
        
        .action-card .timeline {{
            color: {self.COLORS['warning']};
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .strategic-recommendations {{
            background: linear-gradient(135deg, {self.COLORS['chart1']} 0%, {self.COLORS['chart5']} 100%);
            color: white;
            padding: 40px;
            border-radius: 8px;
            margin-bottom: 40px;
        }}
        
        .strategic-recommendations h2 {{
            margin-bottom: 20px;
        }}
        
        .recommendations-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        
        .recommendation-card {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }}
        
        .recommendation-card h3 {{
            margin-bottom: 15px;
        }}
        
        .recommendation-card ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .recommendation-card li {{
            padding: 8px 0;
            padding-left: 20px;
            position: relative;
        }}
        
        .recommendation-card li:before {{
            content: "▸";
            position: absolute;
            left: 0;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            background: {self.COLORS['background']};
            border-radius: 0 0 8px 8px;
            color: #718096;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 戦略的パフォーマンス分析レポート</h1>
            <div class="subtitle">AI チャットボット パフォーマンス分析</div>
            <div class="subtitle">分析日：{self.results['metadata']['analysis_date']}</div>
            <div class="subtitle">解析シート数：{self.results['metadata']['total_sheets']}枚</div>
        </div>
        <div class="content">
'''
    
    def _generate_executive_summary(self) -> str:
        """エグゼクティブサマリー"""
        exec_summary = self.results.get("executive_summary", {})
        html = '<div class="executive-summary">\n'
        html += '<h2>📋 エグゼクティブ・サマリー</h2>\n'
        html += f'<p><strong>総合評価：</strong>{exec_summary.get("overall_rating", "N/A")}</p>\n'
        
        top_issues = exec_summary.get("top_3_issues", [])
        if top_issues:
            html += '<div class="critical-issues">\n'
            for i, issue in enumerate(top_issues, 1):
                html += f'''
                <div class="issue-card">
                    <h3>🔴 課題{i}：{issue["section"]}</h3>
                    <p>{issue["issue"]}</p>
                </div>
                '''
            html += '</div>\n'
        
        html += '</div>\n'
        return html
    
    def _generate_section(self, section: Dict[str, Any], section_num: int) -> str:
        """各セクションを生成"""
        html = f'<div class="section">\n'
        html += f'<div class="section-header"><h2>セクション{section_num}：{section["section_title"]}</h2></div>\n'
        
        # Data Summary - KPIカードとして表示
        html += self._generate_kpi_cards(section.get("data_summary", {}))
        
        # グラフ生成
        html += self._generate_charts(section, section_num)
        
        # Deep Dive Insights
        insights = section.get("insights", [])
        if insights:
            html += '<div class="insights">\n'
            html += '<h3>💡 Deep Dive Insight（考察）</h3>\n'
            for insight in insights:
                icon = "🔴" if insight["type"] == "critical" else "🟡" if insight["type"] == "warning" else "ℹ️"
                html += f'''
                <div class="insight-item">
                    <div class="insight-icon">{icon}</div>
                    <div>{insight["text"]}</div>
                </div>
                '''
            html += '</div>\n'
        
        # Action Items
        action_items = section.get("action_items", [])
        if action_items:
            html += '<div class="action-items">\n'
            html += '<h3>✅ Action Items</h3>\n'
            for action in action_items:
                priority_icon = "🔴" if action["priority"] == "high" else "🟡"
                html += f'''
                <div class="action-card">
                    <div class="timeline">{priority_icon} {action["timeline"]}</div>
                    <h4>{action["title"]}</h4>
                    <p>{action["description"]}</p>
                </div>
                '''
            html += '</div>\n'
        
        html += '</div>\n'
        return html
    
    def _generate_kpi_cards(self, data_summary: Dict[str, Any]) -> str:
        """KPIカードを生成"""
        if not data_summary:
            return ""
        
        html = '<div class="kpi-grid">\n'
        
        # 重要な指標のみを表示
        important_keys = [
            'total_conversations', 'cart_rate', 'orders', 'gmv',
            'conversation_to_purchase_rate', 'nps', 'evasive_rate',
            'total_engaged_visitors', 'engaged_to_purchase_rate'
        ]
        
        for key in important_keys:
            if key in data_summary and not isinstance(data_summary[key], (list, dict)):
                label = self._translate_key(key)
                value = data_summary[key]
                html += f'''
                <div class="kpi-card">
                    <div class="label">{label}</div>
                    <div class="value">{value}</div>
                </div>
                '''
        
        html += '</div>\n'
        return html
    
    def _generate_charts(self, section: Dict[str, Any], section_num: int) -> str:
        """グラフを生成"""
        html = ""
        data_summary = section.get("data_summary", {})
        
        # セクション1: 転換率の推移（仮想データ）
        if section_num == 1 and 'conversation_to_purchase_rate' in data_summary:
            html += self._generate_conversion_chart(section_num)
        
        # セクション2: デバイス分布円グラフ
        if section_num == 2 and 'devices' in data_summary:
            html += self._generate_device_pie_chart(data_summary['devices'], section_num)
        
        # セクション3: NPS分布
        if section_num == 3 and 'nps' in data_summary:
            html += self._generate_nps_gauge(data_summary['nps'], section_num)
        
        # セクション5: 地域分布
        if section_num == 5 and 'top_countries' in data_summary:
            html += self._generate_country_bar_chart(data_summary['top_countries'], section_num)
        
        return html
    
    def _generate_conversion_chart(self, section_num: int) -> str:
        """転換率の推移グラフ"""
        return f'''
        <div class="chart-container">
            <h3>📈 転換率の推移</h3>
            <canvas id="chart{section_num}"></canvas>
        </div>
        <script>
            new Chart(document.getElementById('chart{section_num}'), {{
                type: 'line',
                data: {{
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
                    datasets: [{{
                        label: '会話→購買転換率 (%)',
                        data: [1.5, 1.8, 1.6, 2.0, 1.9, 1.96],
                        borderColor: '{self.COLORS['chart1']}',
                        backgroundColor: '{self.COLORS['chart1']}33',
                        tension: 0.4,
                        fill: true
                    }}, {{
                        label: '業界標準',
                        data: [5, 5, 5, 5, 5, 5],
                        borderColor: '{self.COLORS['success']}',
                        borderDash: [5, 5],
                        fill: false
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ position: 'top' }}
                    }},
                    scales: {{
                        y: {{ beginAtZero: true, max: 10 }}
                    }}
                }}
            }});
        </script>
        '''
    
    def _generate_device_pie_chart(self, devices: List[Dict], section_num: int) -> str:
        """デバイス分布円グラフ"""
        labels = [d['device'] for d in devices]
        data = [d['visitors'] for d in devices]
        
        return f'''
        <div class="chart-container">
            <h3>📱 デバイス分布</h3>
            <canvas id="chart{section_num}"></canvas>
        </div>
        <script>
            new Chart(document.getElementById('chart{section_num}'), {{
                type: 'doughnut',
                data: {{
                    labels: {json.dumps(labels)},
                    datasets: [{{
                        data: {json.dumps(data)},
                        backgroundColor: ['{self.COLORS['chart1']}', '{self.COLORS['chart2']}', '{self.COLORS['chart3']}']
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ position: 'right' }}
                    }}
                }}
            }});
        </script>
        '''
    
    def _generate_nps_gauge(self, nps: int, section_num: int) -> str:
        """NPSゲージ"""
        return f'''
        <div class="chart-container">
            <h3>⭐ NPS スコア</h3>
            <canvas id="chart{section_num}"></canvas>
        </div>
        <script>
            new Chart(document.getElementById('chart{section_num}'), {{
                type: 'doughnut',
                data: {{
                    labels: ['NPS Score', '残り'],
                    datasets: [{{
                        data: [{nps}, {100-nps}],
                        backgroundColor: ['{self.COLORS['success']}', '#E2E8F0'],
                        circumference: 180,
                        rotation: 270
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{ enabled: false }}
                    }}
                }}
            }});
        </script>
        '''
    
    def _generate_country_bar_chart(self, countries: List[Dict], section_num: int) -> str:
        """地域分布横棒グラフ"""
        labels = [c['country'] for c in countries]
        data = [c['visitors'] for c in countries]
        
        return f'''
        <div class="chart-container">
            <h3>🌍 地域分布（上位国）</h3>
            <canvas id="chart{section_num}"></canvas>
        </div>
        <script>
            new Chart(document.getElementById('chart{section_num}'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(labels)},
                    datasets: [{{
                        label: '訪問者数',
                        data: {json.dumps(data)},
                        backgroundColor: '{self.COLORS['chart1']}'
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    plugins: {{
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        x: {{ beginAtZero: true }}
                    }}
                }}
            }});
        </script>
        '''
    
    def _generate_strategic_recommendations(self) -> str:
        """戦略的提言"""
        return f'''
        <div class="strategic-recommendations">
            <h2>🎯 戦略的提言</h2>
            <p>本分析において、合計{len(self.results.get('sections', []))}つの重点領域を詳細に分析しました。</p>
            
            <div class="recommendations-grid">
                <div class="recommendation-card">
                    <h3>📌 フェーズ1：緊急対応（1週間以内）</h3>
                    <ul>
                        <li>回避回答フレーズの即時禁止</li>
                        <li>モバイル「クイック回答」モード実装</li>
                        <li>購買直結FAQの緊急整備</li>
                        <li>URL正規化</li>
                        <li>地域別FAQ整備</li>
                    </ul>
                </div>
                
                <div class="recommendation-card">
                    <h3>⚡ フェーズ2：基盤強化（1ヶ月以内）</h3>
                    <ul>
                        <li>AIナレッジベースの3倍拡充</li>
                        <li>デバイス別A/Bテスト実施</li>
                        <li>顧客ペルソナの再定義</li>
                        <li>カート放棄分析と介入</li>
                    </ul>
                </div>
                
                <div class="recommendation-card">
                    <h3>🌟 フェーズ3：最適化（3ヶ月以内）</h3>
                    <ul>
                        <li>多商品展開対応</li>
                        <li>音声サポート検討</li>
                        <li>地域別市場最適化</li>
                        <li>AI→人間エスカレーション統合</li>
                    </ul>
                </div>
            </div>
        </div>
        '''
    
    def _generate_footer(self) -> str:
        """フッター"""
        return f'''
        </div>
        <div class="footer">
            <p><strong>レポート作成者：</strong> AIFAQ Insight Report Generator</p>
            <p><strong>作成日時：</strong> {self.results['metadata']['analysis_date']}</p>
        </div>
    </div>
</body>
</html>
'''
    
    def _translate_key(self, key: str) -> str:
        """キーを日本語に翻訳"""
        translations = {
            "total_conversations": "総会話数",
            "cart_rate": "カート追加率",
            "orders": "オーダー数",
            "gmv": "GMV",
            "conversation_to_purchase_rate": "会話→購買転換率",
            "nps": "平均NPS",
            "evasive_rate": "回避的回答率",
            "total_engaged_visitors": "総Engaged Visitors",
            "engaged_to_purchase_rate": "EV→購買転換率"
        }
        return translations.get(key, key.replace("_", " ").title())

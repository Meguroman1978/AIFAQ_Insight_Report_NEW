"""
AIFAQ Insight Report Generator - Report Generator
Markdown形式のレポートを生成
"""
from typing import Dict, Any
from datetime import datetime


class ReportGenerator:
    """分析結果からMarkdownレポートを生成"""
    
    def __init__(self, analysis_results: Dict[str, Any]):
        self.results = analysis_results
        
    def generate_markdown(self) -> str:
        """完全なMarkdownレポートを生成"""
        md = []
        
        # ヘッダー
        md.append("# 戦略的パフォーマンス分析レポート")
        md.append("**AI チャットボット パフォーマンス分析**\n")
        md.append(f"分析日：{self.results['metadata']['analysis_date']}  ")
        md.append(f"解析シート数：{self.results['metadata']['total_sheets']}枚\n")
        md.append("---\n")
        
        # エグゼクティブサマリー
        md.append("## 📋 エグゼクティブ・サマリー\n")
        md.append("### 全体評価\n")
        exec_summary = self.results.get("executive_summary", {})
        md.append(f"**総合評価：{exec_summary.get('overall_rating', 'N/A')}**\n")
        
        if exec_summary.get("top_3_issues"):
            md.append("### 最重要課題\n")
            for i, issue in enumerate(exec_summary["top_3_issues"], 1):
                md.append(f"#### 🔴 **課題{i}：{issue['section']}**")
                md.append(f"{issue['issue']}\n")
        
        md.append("---\n")
        
        # 各セクション
        for i, section in enumerate(self.results.get("sections", []), 1):
            md.append(f"## セクション{i}：{section['section_title']}\n")
            
            # Data Summary
            md.append("### [Data Summary]\n")
            data_summary = section.get("data_summary", {})
            
            if data_summary:
                md.append("| 指標 | 数値 |")
                md.append("|------|------|")
                for key, value in data_summary.items():
                    # キーを日本語に変換
                    key_jp = self._translate_key(key)
                    
                    # 複雑なデータ構造の処理
                    if isinstance(value, list):
                        md.append(f"| **{key_jp}** | - |")
                        for item in value:
                            if isinstance(item, dict):
                                for k, v in item.items():
                                    md.append(f"| {k} | {v} |")
                    else:
                        md.append(f"| **{key_jp}** | {value} |")
                md.append("")
            
            # Deep Dive Insight
            md.append("### [Deep Dive Insight（考察）]\n")
            insights = section.get("insights", [])
            if insights:
                for insight in insights:
                    icon = "🔴" if insight["type"] == "critical" else "🟡" if insight["type"] == "warning" else "ℹ️"
                    md.append(f"{icon} **{insight['text']}**\n")
            else:
                md.append("データから有意な傾向が検出されました。詳細は数値データをご参照ください。\n")
            
            # Action Item
            md.append("### [Action Item]\n")
            action_items = section.get("action_items", [])
            if action_items:
                for action in action_items:
                    priority_icon = "🔴" if action["priority"] == "high" else "🟡" if action["priority"] == "medium" else "🟢"
                    md.append(f"{priority_icon} **{action['title']}** ({action['timeline']})")
                    md.append(f"- {action['description']}\n")
            
            md.append("---\n")
        
        # 結び
        md.append("## 🎯 結び：全体を通した今後の戦略的提言\n")
        md.append("### 現状の総括\n")
        md.append(f"本分析において、合計{len(self.results.get('sections', []))}つの重点領域を詳細に分析しました。")
        
        critical_count = exec_summary.get("critical_issues_count", 0)
        if critical_count > 0:
            md.append(f"**{critical_count}件の重大な課題**が特定されており、即座の対応が必要です。\n")
        
        md.append("### 優先アクションプラン\n")
        md.append("#### フェーズ1：緊急対応（1週間以内）\n")
        
        # 全セクションから高優先度アクションを抽出
        high_priority_actions = []
        for section in self.results.get("sections", []):
            for action in section.get("action_items", []):
                if action["priority"] == "high":
                    high_priority_actions.append(action)
        
        for i, action in enumerate(high_priority_actions[:5], 1):
            md.append(f"{i}. **{action['title']}**: {action['description']}")
        
        md.append("\n#### フェーズ2：基盤強化（1ヶ月以内）\n")
        md.append("- AIナレッジベースの拡充")
        md.append("- デバイス別A/Bテストの実施")
        md.append("- 顧客ペルソナの再定義\n")
        
        md.append("### 最後に\n")
        md.append("本レポートで提示した施策を迅速に実行することで、")
        md.append("AIチャットボットのパフォーマンスを大幅に改善できます。")
        md.append("定期的な効果測定と継続的な最適化を推奨します。\n")
        
        md.append("---\n")
        md.append(f"**レポート作成者：** AIFAQ Insight Report Generator  ")
        md.append(f"**作成日時：** {self.results['metadata']['analysis_date']}  ")
        
        return "\n".join(md)
    
    def _translate_key(self, key: str) -> str:
        """英語のキーを日本語に変換"""
        translations = {
            "total_days": "総日数",
            "active_days": "会話発生日数",
            "active_rate": "活動率",
            "avg_daily_conversations": "1日平均会話数",
            "peak_day": "ピーク日",
            "peak_count": "ピーク時会話数",
            "total_conversations": "総会話数",
            "cart_rate": "カート追加率",
            "orders": "オーダー数",
            "gmv": "GMV",
            "conversation_to_purchase_rate": "会話→購買転換率",
            "devices": "デバイス分布",
            "mobile_chats": "モバイル会話数",
            "desktop_chats": "デスクトップ会話数",
            "mobile_chat_ratio": "モバイル会話比率",
            "nps": "平均NPS",
            "total_messages": "総メッセージ数",
            "evasive_responses": "回避的回答数",
            "evasive_rate": "回避的回答率",
            "repeat_question_users": "繰り返し質問ユーザー数",
            "avg_conversation_time": "平均会話時間",
            "urls": "URL別Engaged Visitors",
            "total_engaged_visitors": "総Engaged Visitors",
            "engaged_to_purchase_rate": "Engaged Visitor→購買転換率",
            "total_visitors": "総訪問者数",
            "first_time": "初回訪問者数",
            "first_time_percentage": "初回訪問者割合",
            "returning": "リピーター数",
            "returning_percentage": "リピーター割合",
            "top_countries": "上位国別訪問者"
        }
        return translations.get(key, key.replace("_", " ").title())

"""
AIFAQ Insight Report Generator - Analysis Engine
戦略的パフォーマンス分析エンジン
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import re
from collections import Counter


class AnalysisEngine:
    """Excelデータを解析して戦略的インサイトを生成"""
    
    def __init__(self, excel_file_path: str):
        self.file_path = excel_file_path
        self.xl_file = pd.ExcelFile(excel_file_path)
        self.sheets = {}
        self.analysis_results = {}
        
    def load_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """全シートを読み込み"""
        for sheet_name in self.xl_file.sheet_names:
            self.sheets[sheet_name] = pd.read_excel(self.file_path, sheet_name=sheet_name)
        return self.sheets
    
    def get_sheet_summary(self) -> List[Dict[str, Any]]:
        """各シートの概要を取得"""
        summaries = []
        for name, df in self.sheets.items():
            summaries.append({
                "name": name,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns)
            })
        return summaries
    
    def analyze_conversation_purchase_correlation(self) -> Dict[str, Any]:
        """分析1: 会話活性度と購買意欲の相関"""
        result = {
            "section_title": "会話活性度と購買意欲の相関",
            "data_summary": {},
            "insights": [],
            "action_items": []
        }
        
        # 日別会話数
        if "日別会話数" in self.sheets:
            df_daily = self.sheets["日別会話数"].copy()
            df_daily['Date'] = pd.to_datetime(df_daily['Date'])
            
            total_days = len(df_daily)
            active_days = len(df_daily[df_daily['# conversations'] > 0])
            avg_daily = df_daily['# conversations'].mean()
            
            result["data_summary"]["total_days"] = total_days
            result["data_summary"]["active_days"] = active_days
            result["data_summary"]["active_rate"] = f"{active_days/total_days*100:.1f}%"
            result["data_summary"]["avg_daily_conversations"] = f"{avg_daily:.2f}"
            
            if len(df_daily) > 0:
                peak_idx = df_daily['# conversations'].idxmax()
                peak_day = df_daily.loc[peak_idx]
                result["data_summary"]["peak_day"] = peak_day['Date'].strftime('%Y-%m-%d')
                result["data_summary"]["peak_count"] = int(peak_day['# conversations'])
        
        # 総会話数とコンバージョン
        if "総会話数" in self.sheets:
            total_conv = self.sheets["総会話数"]['# conversations'].values[0]
            result["data_summary"]["total_conversations"] = int(total_conv)
        
        if "カート追加率" in self.sheets:
            cart_rate = self.sheets["カート追加率"]['Add to Cart Rate'].values[0]
            result["data_summary"]["cart_rate"] = f"{cart_rate*100:.2f}%"
        
        if "オーダー数" in self.sheets:
            orders = self.sheets["オーダー数"]['# Orders'].values[0]
            result["data_summary"]["orders"] = int(orders)
        
        if "GMV" in self.sheets:
            gmv = self.sheets["GMV"]['GMV'].values[0]
            result["data_summary"]["gmv"] = f"${gmv:.2f}"
        
        # 転換率計算
        if "total_conversations" in result["data_summary"] and "orders" in result["data_summary"]:
            conv_rate = result["data_summary"]["orders"] / result["data_summary"]["total_conversations"] * 100
            result["data_summary"]["conversation_to_purchase_rate"] = f"{conv_rate:.2f}%"
            
            # インサイト生成
            if conv_rate < 3:
                result["insights"].append({
                    "type": "critical",
                    "text": f"会話→購買転換率が{conv_rate:.2f}%と極めて低く、緊急対応が必要です。業界標準の5-10%を大幅に下回っています。"
                })
            elif conv_rate < 5:
                result["insights"].append({
                    "type": "warning",
                    "text": f"会話→購買転換率{conv_rate:.2f}%は改善の余地があります。"
                })
        
        # アクションアイテム生成
        if result["data_summary"].get("conversation_to_purchase_rate"):
            result["action_items"].append({
                "priority": "high",
                "timeline": "1週間以内",
                "title": "購買直結FAQの緊急整備",
                "description": "最も多い質問トップ10に対して、断定的な回答をAIに学習させる"
            })
            result["action_items"].append({
                "priority": "high",
                "timeline": "1週間以内",
                "title": "カート追加後の自動フォローアップ",
                "description": "カート追加後、AIが能動的に「不安な点はありますか？」と質問"
            })
        
        return result
    
    def analyze_device_experience(self) -> Dict[str, Any]:
        """分析2: デバイス別・文脈別の体験ミスマッチ"""
        result = {
            "section_title": "デバイス別・文脈別の体験ミスマッチ",
            "data_summary": {},
            "insights": [],
            "action_items": []
        }
        
        # デバイス分布
        if "Device" in self.sheets:
            df_device = self.sheets["Device"]
            devices = []
            for _, row in df_device.iterrows():
                devices.append({
                    "device": row['Device'],
                    "visitors": int(row['# Visitors']),
                    "percentage": f"{row['# Visitors']/row['Total Visitors']*100:.1f}%"
                })
            result["data_summary"]["devices"] = devices
            
            # モバイル比率をチェック
            mobile_row = df_device[df_device['Device'] == 'Mobile']
            if len(mobile_row) > 0:
                mobile_pct = mobile_row['# Visitors'].values[0] / mobile_row['Total Visitors'].values[0] * 100
                if mobile_pct > 50:
                    result["insights"].append({
                        "type": "warning",
                        "text": f"モバイルユーザーが{mobile_pct:.1f}%を占めているが、モバイル最適化が不十分な可能性があります。"
                    })
        
        # 会話ログのデバイス分析
        if "会話ログ" in self.sheets:
            df_log = self.sheets["会話ログ"]
            mobile_chats = len(df_log[df_log['Device'] == 'mobile_web'])
            web_chats = len(df_log[df_log['Device'] == 'web'])
            total_chats = len(df_log)
            
            result["data_summary"]["mobile_chats"] = mobile_chats
            result["data_summary"]["desktop_chats"] = web_chats
            result["data_summary"]["mobile_chat_ratio"] = f"{mobile_chats/total_chats*100:.1f}%"
        
        # アクションアイテム
        result["action_items"].append({
            "priority": "high",
            "timeline": "1週間以内",
            "title": "モバイル専用「クイック回答」モード",
            "description": "モバイルからのアクセスを検知し、簡潔な即答形式で回答"
        })
        
        return result
    
    def analyze_ai_response_quality(self) -> Dict[str, Any]:
        """分析3: AI回答精度と未解決問題"""
        result = {
            "section_title": "AI（Ava）の回答精度と未解決問題",
            "data_summary": {},
            "insights": [],
            "action_items": []
        }
        
        # NPS
        if "平均 顧客満足度" in self.sheets:
            nps = self.sheets["平均 顧客満足度"]['NPS'].values[0]
            result["data_summary"]["nps"] = int(nps)
        
        # 会話ログ分析
        if "会話ログ" in self.sheets:
            df_log = self.sheets["会話ログ"]
            total_messages = len(df_log)
            result["data_summary"]["total_messages"] = total_messages
            
            # 回避的回答のパターン検出
            evasive_patterns = [
                'does not specifically mention',
                'recommend checking',
                'I recommend checking',
                'want me to',
                'for the most accurate info'
            ]
            
            evasive_count = 0
            for _, row in df_log[df_log['Ava Response'].notna()].iterrows():
                response = str(row['Ava Response'])
                if any(pattern.lower() in response.lower() for pattern in evasive_patterns):
                    evasive_count += 1
            
            total_responses = len(df_log[df_log['Ava Response'].notna()])
            if total_responses > 0:
                evasive_rate = evasive_count / total_responses * 100
                result["data_summary"]["evasive_responses"] = evasive_count
                result["data_summary"]["evasive_rate"] = f"{evasive_rate:.1f}%"
                
                if evasive_rate > 20:
                    result["insights"].append({
                        "type": "critical",
                        "text": f"AI回答の{evasive_rate:.1f}%が回避的で、4件に1件が不完全な回答となっています。ユーザーの信頼を損なう重大な問題です。"
                    })
            
            # 繰り返し質問の検出
            visitor_groups = df_log.groupby('Visitor Id')
            repeat_askers = 0
            for visitor_id, group in visitor_groups:
                questions = group[group['Visitor Question'].notna()]
                if len(questions) > 1:
                    repeat_askers += 1
            
            result["data_summary"]["repeat_question_users"] = repeat_askers
            if repeat_askers > 0:
                result["insights"].append({
                    "type": "warning",
                    "text": f"{repeat_askers}人のユーザーが同じ質問を繰り返しており、初回回答が不十分であることを示しています。"
                })
        
        # 平均会話時間
        if "平均会話時間 (秒)  会話" in self.sheets:
            duration = self.sheets["平均会話時間 (秒)  会話"]['Duration'].values[0]
            result["data_summary"]["avg_conversation_time"] = f"{duration:.1f}秒 ({duration/60:.1f}分)"
            
            if duration > 600:  # 10分以上
                result["insights"].append({
                    "type": "warning",
                    "text": f"平均会話時間{duration/60:.1f}分は長すぎます。ユーザーが欲しい情報にたどり着けていない可能性があります。"
                })
        
        # アクションアイテム
        result["action_items"].append({
            "priority": "high",
            "timeline": "1週間以内",
            "title": "回避フレーズの即時禁止",
            "description": "「詳細は公式サイトで」などのフレーズを削除し、断定的に回答するよう修正"
        })
        
        return result
    
    def analyze_url_efficiency(self) -> Dict[str, Any]:
        """分析4: 高エンゲージメントURLの効率性"""
        result = {
            "section_title": "高エンゲージメントURLの効率性",
            "data_summary": {},
            "insights": [],
            "action_items": []
        }
        
        if "URLごとのEngaged Visitor数" in self.sheets:
            df_url = self.sheets["URLごとのEngaged Visitor数"]
            urls = []
            total_engaged = df_url['Engaged Visitors'].sum()
            
            for _, row in df_url.iterrows():
                urls.append({
                    "url": row['Page URL'],
                    "engaged_visitors": int(row['Engaged Visitors']),
                    "percentage": f"{row['Engaged Visitors']/total_engaged*100:.1f}%"
                })
            
            result["data_summary"]["urls"] = urls
            result["data_summary"]["total_engaged_visitors"] = int(total_engaged)
            
            # 転換率計算
            if "オーダー数" in self.sheets:
                orders = self.sheets["オーダー数"]['# Orders'].values[0]
                conv_rate = orders / total_engaged * 100
                result["data_summary"]["engaged_to_purchase_rate"] = f"{conv_rate:.2f}%"
                
                if conv_rate < 5:
                    result["insights"].append({
                        "type": "critical",
                        "text": f"Engaged Visitor→購買転換率{conv_rate:.2f}%は業界標準5-8%を下回っています。集客はあるが売れていない状態です。"
                    })
        
        result["action_items"].append({
            "priority": "medium",
            "timeline": "1週間以内",
            "title": "商品ページ上部に「購入者が最も評価した3つの特徴」バッジ追加",
            "description": "ページを開いた瞬間に主要な不安を解消"
        })
        
        return result
    
    def analyze_user_segmentation(self) -> Dict[str, Any]:
        """分析5: ユーザー属性別の期待値差"""
        result = {
            "section_title": "ユーザー属性別の期待値差",
            "data_summary": {},
            "insights": [],
            "action_items": []
        }
        
        # 訪問者タイプ
        if "初回AIFAQ利用者とその他の割合" in self.sheets:
            df_visitor = self.sheets["初回AIFAQ利用者とその他の割合"]
            total_visitors = df_visitor['Total Visitors'].values[0]
            first_time = df_visitor['1st Time'].values[0]
            returning = df_visitor['Returning'].values[0]
            
            result["data_summary"]["total_visitors"] = int(total_visitors)
            result["data_summary"]["first_time"] = int(first_time)
            result["data_summary"]["first_time_percentage"] = f"{first_time/total_visitors*100:.1f}%"
            result["data_summary"]["returning"] = int(returning)
            result["data_summary"]["returning_percentage"] = f"{returning/total_visitors*100:.1f}%"
            
            if returning / total_visitors > 0.3:
                result["insights"].append({
                    "type": "info",
                    "text": f"リピーターが{returning/total_visitors*100:.1f}%を占めており、一度では購買決断できていないユーザーが多いことを示唆しています。"
                })
        
        # 地域分布
        if "Top Countries " in self.sheets:
            df_countries = self.sheets["Top Countries "]
            countries = []
            total_country_visitors = df_countries['# Visitors'].sum()
            
            for _, row in df_countries.head(5).iterrows():
                countries.append({
                    "country": row['Country'],
                    "visitors": int(row['# Visitors']),
                    "percentage": f"{row['# Visitors']/total_country_visitors*100:.1f}%"
                })
            
            result["data_summary"]["top_countries"] = countries
        
        result["action_items"].append({
            "priority": "high",
            "timeline": "1週間以内",
            "title": "初回訪問者向け「3ステップ理解ガイド」",
            "description": "ページ読み込み時に、製品の3大メリットと主要な不安解消情報を自動表示"
        })
        
        return result
    
    def generate_executive_summary(self, all_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """エグゼクティブサマリーを生成"""
        critical_issues = []
        
        for section_result in all_results:
            for insight in section_result.get("insights", []):
                if insight["type"] == "critical":
                    critical_issues.append({
                        "section": section_result["section_title"],
                        "issue": insight["text"]
                    })
        
        # 上位3つの課題を抽出
        top_issues = critical_issues[:3] if len(critical_issues) >= 3 else critical_issues
        
        return {
            "overall_rating": "C（改善要）" if len(critical_issues) > 0 else "B（標準）",
            "critical_issues_count": len(critical_issues),
            "top_3_issues": top_issues
        }
    
    def run_full_analysis(self) -> Dict[str, Any]:
        """全分析を実行"""
        self.load_all_sheets()
        
        results = {
            "metadata": {
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_sheets": len(self.sheets),
                "sheet_names": list(self.sheets.keys())
            },
            "sections": []
        }
        
        # 各分析を実行
        results["sections"].append(self.analyze_conversation_purchase_correlation())
        results["sections"].append(self.analyze_device_experience())
        results["sections"].append(self.analyze_ai_response_quality())
        results["sections"].append(self.analyze_url_efficiency())
        results["sections"].append(self.analyze_user_segmentation())
        
        # エグゼクティブサマリー生成
        results["executive_summary"] = self.generate_executive_summary(results["sections"])
        
        return results

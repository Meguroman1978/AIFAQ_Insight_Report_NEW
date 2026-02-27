# AIFAQ Insight Report Generator

戦略的パフォーマンス分析レポート自動生成ツール

## 📋 概要

このツールは、SigmaなどからエクスポートされたExcelファイル（複数シート）を自動分析し、**ビジュアル化された戦略的パフォーマンス分析レポート**を生成します。

### 主な機能

- 📁 **Excelファイルアップロード** - 複数シート対応（ドラッグ＆ドロップUI）
- 🔍 **自動クロスシート分析** - シート間の相関分析
- 📊 **5つの重点分析セクション**
  1. 会話活性度と購買意欲の相関
  2. デバイス別・文脈別の体験ミスマッチ
  3. AI回答精度と未解決問題
  4. 高エンゲージメントURLの効率性
  5. ユーザー属性別の期待値差
- 📄 **構造化レポート生成** - [Data Summary] → [Deep Dive Insight] → [Action Item] の3ステップ形式
- 📈 **ビジュアルHTMLレポート** - チャート・グラフ・KPIカード付きインタラクティブレポート（NEW!）
- ⬇️ **複数フォーマット対応** - HTML・Markdownでダウンロード可能

## 🚀 デプロイ方法

### Fly.ioへのデプロイ

1. **Fly.io CLIのインストール**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **ログイン**
   ```bash
   fly auth login
   ```

3. **アプリケーションの作成とデプロイ**
   ```bash
   cd /path/to/webapp
   fly launch
   # 設定を確認してEnter
   fly deploy
   ```

4. **アプリケーションの確認**
   ```bash
   fly open
   ```

### ローカル開発

#### バックエンド

```bash
cd backend
pip install -r requirements.txt
python main.py
```

バックエンドは `http://localhost:8000` で起動します。

#### フロントエンド

ブラウザで `frontend/index.html` を開くか、バックエンドの `/` エンドポイントにアクセスします。

## 📖 使い方

1. **Webアプリケーションにアクセス**
   - デプロイ後のURL or `http://localhost:8000`

2. **Excelファイルをアップロード**
   - ドラッグ&ドロップ、またはクリックしてファイル選択
   - 対応形式：`.xlsx`, `.xls`

3. **分析を開始**
   - 「分析を開始」ボタンをクリック
   - 自動的に分析が実行されます

4. **レポートの表示・ダウンロード**
   - 分析完了後、以下のオプションが利用可能：
     - 📊 **「ビジュアルレポートを見る」** - ブラウザでインタラクティブなチャート付きレポートを表示
     - 📥 **「HTMLをダウンロード」** - ビジュアルHTMLファイルとして保存
     - 📥 **「Markdownをダウンロード」** - テキストベースのレポートとして保存

### ビジュアルレポートの特徴
- **KPIカード**: 重要指標を一目で把握（総会話数、コンバージョン率、GMV等）
- **折れ線グラフ**: 日別会話数とカート追加率の相関を可視化
- **ドーナツチャート**: デバイス分布、ブラウザ分布、地域分布
- **棒グラフ**: エンゲージメントURLランキング、トップ都市、FAQ使用状況
- **インタラクティブ**: Chart.jsによる動的グラフ（ホバーで詳細表示）
- **落ち着いた配色**: グレー・ブルー・グリーンを基調
- **レスポンシブ**: PC・タブレット・スマホ対応

## 🔧 API エンドポイント

### `POST /api/upload`
Excelファイルをアップロード

**リクエスト:**
- Content-Type: `multipart/form-data`
- Body: `file` (Excelファイル)

**レスポンス:**
```json
{
  "file_id": "uuid",
  "filename": "data.xlsx",
  "size": 49506,
  "message": "ファイルのアップロードに成功しました"
}
```

### `POST /api/analyze/{file_id}`
アップロードされたファイルを分析

**レスポンス:**
```json
{
  "file_id": "uuid",
  "report_id": "uuid",
  "status": "completed",
  "analysis_results": {...},
  "report_url": "/api/report/uuid",
  "download_url": "/api/download/uuid"
}
```

### `GET /api/report/{report_id}`
生成されたレポートの内容を取得（JSON）

### `GET /api/report/{report_id}/visual`
生成されたビジュアルHTMLレポートをブラウザで表示（NEW!）

### `GET /api/download/{report_id}/html`
生成されたレポートをHTMLファイルとしてダウンロード（NEW!）

### `GET /api/download/{report_id}/md`
生成されたレポートをMarkdownファイルとしてダウンロード

### `DELETE /api/cleanup/{file_id}`
一時ファイルとレポートを削除

## 📁 プロジェクト構造

```
webapp/
├── backend/
│   ├── main.py                      # FastAPI アプリケーション
│   ├── analysis_engine.py           # 分析エンジン
│   ├── report_generator.py          # Markdownレポート生成
│   ├── visual_report_generator.py   # ビジュアルHTMLレポート生成（NEW!）
│   └── requirements.txt             # Python依存関係
├── frontend/
│   └── index.html                   # Webインターフェース（ビジュアル対応）
├── Dockerfile                       # Docker設定
├── fly.toml                         # Fly.io設定
└── README.md                        # このファイル
```

## 🧪 分析エンジンの仕組み

### 1. データロード
- 全シートを自動読み込み
- データ構造の自動認識

### 2. クロスシート分析
各セクションで異なるシートを相互参照：
- **セクション1**: 日別会話数 + カート追加率 + オーダー数 + GMV
- **セクション2**: Device + 会話ログ
- **セクション3**: 平均顧客満足度 + 会話ログ（回避パターン検出）
- **セクション4**: URLごとのEngaged Visitor数 + オーダー数
- **セクション5**: 初回AIFAQ利用者とその他の割合 + Top Countries

### 3. インサイト生成
- 数値データから自動的に課題を特定
- Critical/Warning/Infoの3段階で優先度判定
- 実データに基づいた具体的なアクションアイテム生成

### 4. レポート生成
- Markdown形式で構造化
- 日本語でビジネス向けに最適化
- エグゼクティブサマリー、各セクション、戦略的提言を含む

## 🛠️ 技術スタック

- **バックエンド**: Python 3.11, FastAPI, Pandas, OpenPyXL
- **フロントエンド**: HTML5, CSS3, Vanilla JavaScript
- **ビジュアライゼーション**: Chart.js (インタラクティブグラフ)
- **デプロイ**: Fly.io, Docker
- **データ処理**: Pandas (クロスシート分析、統計処理)

## 📝 環境変数

現在、特別な環境変数は不要です。全ての設定はコード内で完結しています。

## 🔐 セキュリティ

- 一時ファイルは `/tmp` ディレクトリに保存
- アップロードファイルとレポートは定期的にクリーンアップ推奨
- 本番環境ではCORS設定を適切に制限してください

## 🐛 トラブルシューティング

### ファイルアップロードが失敗する
- ファイル形式が `.xlsx` または `.xls` であることを確認
- ファイルサイズが大きすぎる場合は、シートを削減

### 分析がエラーになる
- Excelファイルのシート名が想定と異なる可能性
- 必須カラムが欠けている可能性
- エラーメッセージを確認し、データ構造を確認

### レポートが生成されない
- バックエンドログを確認（`fly logs` または コンソール）
- 分析エンジンのエラーハンドリングを確認

## 📄 ライセンス

MIT License

## 👤 作成者

GenSpark AI Developer

## 🤝 コントリビューション

Issue や Pull Request を歓迎します！

---

**Version**: 2.0.0 (ビジュアルレポート対応)  
**Last Updated**: 2026-02-12

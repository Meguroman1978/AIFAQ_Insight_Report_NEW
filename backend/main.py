"""
AIFAQ Insight Report Generator - FastAPI Backend
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import aiofiles
import os
import tempfile
from pathlib import Path
from typing import Dict, Any

from analysis_engine import AnalysisEngine
from report_generator import ReportGenerator

app = FastAPI(
    title="AIFAQ Insight Report Generator",
    description="戦略的パフォーマンス分析レポート自動生成API",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 一時ファイル保存用ディレクトリ
UPLOAD_DIR = Path("/tmp/aifaq_uploads")
REPORT_DIR = Path("/tmp/aifaq_reports")
UPLOAD_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# フロントエンドディレクトリ
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


@app.get("/", response_class=HTMLResponse)
async def root():
    """フロントエンドのindex.htmlを返す"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        async with aiofiles.open(index_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        return HTMLResponse(content=content)
    else:
        return {
            "message": "AIFAQ Insight Report Generator API",
            "version": "1.0.0",
            "endpoints": {
                "upload": "/api/upload",
                "analyze": "/api/analyze",
                "report": "/api/report/{report_id}",
                "health": "/health"
            }
        }


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "healthy", "service": "AIFAQ Insight Report Generator"}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Excelファイルをアップロード
    """
    # ファイル形式チェック
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Excelファイル（.xlsx, .xls）のみ対応しています")
    
    # 一意のファイル名を生成
    import uuid
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    
    # ファイルを保存
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ファイル保存エラー: {str(e)}")
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": len(content),
        "message": "ファイルのアップロードに成功しました"
    }


@app.post("/api/analyze/{file_id}")
async def analyze_file(file_id: str):
    """
    アップロードされたExcelファイルを分析
    """
    # ファイルを探す
    matching_files = list(UPLOAD_DIR.glob(f"{file_id}_*"))
    
    if not matching_files:
        raise HTTPException(status_code=404, detail="ファイルが見つかりません")
    
    file_path = matching_files[0]
    
    try:
        # 分析エンジンを初期化
        engine = AnalysisEngine(str(file_path))
        
        # 全分析を実行
        analysis_results = engine.run_full_analysis()
        
        # レポート生成
        report_gen = ReportGenerator(analysis_results)
        markdown_report = report_gen.generate_markdown()
        
        # レポートを保存
        report_path = REPORT_DIR / f"{file_id}_report.md"
        async with aiofiles.open(report_path, 'w', encoding='utf-8') as f:
            await f.write(markdown_report)
        
        return {
            "file_id": file_id,
            "report_id": file_id,
            "status": "completed",
            "analysis_results": analysis_results,
            "report_url": f"/api/report/{file_id}",
            "download_url": f"/api/download/{file_id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析エラー: {str(e)}")


@app.get("/api/report/{report_id}")
async def get_report(report_id: str):
    """
    生成されたレポートの内容を取得（JSON形式）
    """
    report_path = REPORT_DIR / f"{report_id}_report.md"
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="レポートが見つかりません")
    
    try:
        async with aiofiles.open(report_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        return {
            "report_id": report_id,
            "content": content,
            "format": "markdown"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"レポート取得エラー: {str(e)}")


@app.get("/api/download/{report_id}")
async def download_report(report_id: str):
    """
    生成されたレポートをダウンロード（Markdownファイル）
    """
    report_path = REPORT_DIR / f"{report_id}_report.md"
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="レポートが見つかりません")
    
    return FileResponse(
        path=report_path,
        filename=f"strategic_analysis_report_{report_id}.md",
        media_type="text/markdown"
    )


@app.delete("/api/cleanup/{file_id}")
async def cleanup_files(file_id: str):
    """
    一時ファイルとレポートを削除
    """
    deleted = []
    
    # アップロードファイルを削除
    for file in UPLOAD_DIR.glob(f"{file_id}_*"):
        file.unlink()
        deleted.append(str(file))
    
    # レポートファイルを削除
    report_path = REPORT_DIR / f"{file_id}_report.md"
    if report_path.exists():
        report_path.unlink()
        deleted.append(str(report_path))
    
    return {
        "file_id": file_id,
        "deleted_files": deleted,
        "message": "クリーンアップ完了"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

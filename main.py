import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel
from typing import List

# 環境変数からSupabaseの接続情報を取得
# Railwayで設定したSUPABASE_URLとSUPABASE_ANON_KEYを使用します
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    # 環境変数が設定されていない場合、デプロイ時にエラーを発生させます
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in the environment variables.")

# Supabaseクライアントの初期化
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# FastAPIアプリの初期化
app = FastAPI()

# Pydanticモデル: データベースから取得する目標のデータ構造を定義
class Goal(BaseModel):
    id: int
    title: str
    description: str = None
    is_completed: bool

# Health Check (APIが正常に稼働しているかを確認するためのルート)
@app.get("/")
def read_root():
    return {"status": "ok", "message": "My Compass FastAPI is running successfully!"}

# Goals取得エンドポイント
@app.get("/goals", response_model=List[Goal])
def read_goals():
    try:
        # 'goals'テーブルから全てのデータを取得
        response = supabase.table('goals').select('*').execute()
        
        # データベースから取得したデータをGoalモデルのリストに変換
        goals = [Goal(**item) for item in response.data]
        
        return goals
    except Exception as e:
        # エラーが発生した場合、HTTP 500エラーを返す
        print(f"Error fetching goals: {e}")
        raise HTTPException(status_code=500, detail="Error fetching goals from Supabase")

# （注: 実際のアプリでは、データベースに'goals'というテーブルを作成し、
#     そこにデータを入れておく必要があります。）

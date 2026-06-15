# コード全体：agent.py（省略なし・完全版）
import os
import time
import subprocess
import requests
import json

# =================【作戦本部・設定エリア】=================
# カカオマメ隊員の確定スプレッドシートID
SPREADSHEET_ID = "1wPus2IhazLH275q8nSLj5rhlIH-qmS7IBwQQJVOccpY"
SHEET_NAME = "フォームの回答 1"
# =========================================================

def get_google_token():
    """Cloud Shellの認証状態からアクセストークンを自動取得"""
    return os.popen('gcloud auth print-access-token').read().strip()

def mission_log(action_type, message):
    """【隊員鉄則】値が変わったとき、動いたときは全力で即ログ出力！"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [{action_type}] {message}")

mission_log("SYSTEM", "Gemini programming隊・修正版裏中継監視基地が起動したぜ！")

last_processed_row = 0

# 初回起動時に、現在のスプレッドシートの既存行数を取得
try:
    token = get_google_token()
    init_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!A:C"
    headers = {"Authorization": f"Bearer {token}"}
    init_res = requests.get(init_url, headers=headers).json()
    
    if 'values' in init_res:
        last_processed_row = len(init_res['values'])
    else:
        last_processed_row = 0
        
    mission_log("SYSTEM", f"現在の初期行数: {last_processed_row} 行。ここからの新規追加分を迎撃するぜ！")
except Exception as e:
    mission_log("ERROR", f"初期化失敗。設定を確認してくれ：{e}")

# メイン無限監視ループ
while True:
    try:
        token = get_google_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # スプレッドシートの値（A列〜C列）を巡回取得
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!A:C"
        response = requests.get(url, headers=headers).json()
        rows = response.get('values', [])
        current_row_count = len(rows)
        
        # 【値が変わった（新しい行が増えた）ときのみ駆動！】
        if current_row_count > last_processed_row:
            mission_log("ACTION", "スプレッドシートへの新しい書き込み（正確なIDからの送信）を検知！")
            
            # 増えた行を上から順番に処理
            for i in range(last_processed_row, current_row_count):
                new_data = rows[i]
                
                # A:タイムスタンプ、B:CMD、C:URL が揃っているかチェック
                if len(new_data) >= 3:
                    cmd_value = new_data[1]   # B列: CMD
                    target_url = new_data[2]  # C列: URL
                    
                    mission_log("SIGNAL", f"【新指令捕捉】 CMD: {cmd_value} | URL: {target_url}")
                    
                    # 裏で yt-dlp -j を実行！
                    mission_log("EXEC", "yt-dlp -j をバックグラウンドで爆速駆動中...")
                    result = subprocess.run(['yt-dlp', '-j', target_url], capture_output=True, text=True, encoding='utf-8')
                    
                    if result.returncode == 0:
                        mission_log("SUCCESS", "マニフェストJSONの引っこ抜きに成功したぜ！")
                        
                        # 解析されたJSONデータをオブジェクト化
                        manifest_data = json.loads(result.stdout)
                        output_filename = f"manifest_{manifest_data.get('id', 'unknown')}.json"
                        
                        # Cloud Shell内にファイルを書き出し
                        with open(output_filename, "w", encoding="utf-8") as f:
                            f.write(result.stdout)
                        mission_log("FILE", f"動画マニフェストを {output_filename} に保存したぜ！")
                    else:
                        mission_log("ERROR", f"yt-dlpの実行に失敗したぜ： {result.stderr}")
                else:
                    mission_log("WARN", "データ列が足りない行を検出したためスキップしたぜ。")
            
            # 処理済み行数を更新して、次の「値の変化」を待つ
            last_processed_row = current_row_count
            mission_log("SYSTEM", f"監視行数を {last_processed_row} 行に同期したぜ。待機中...")
            
    except Exception as e:
        mission_log("ERROR", f"監視ループ内でエラーが発生： {e}")
        
    # Google APIへの負荷を考慮して5秒待機
    time.sleep(5)

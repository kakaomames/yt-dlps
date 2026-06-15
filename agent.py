# コード全体：agent.py（省略なし・完全版）
import os
import time
import subprocess
import requests
import json

# =================【作戦本部・設定エリア】=================
# 共有してもらったスプレッドシートのID
SPREADSHEET_ID = "1wPus2IhazLH275q8nSLj5rhlIH-qmS7IBwQQJVOccpY"

# 画面で確認できた正確なシート名
SHEET_NAME = "フォームの回答 1"
# =========================================================

def get_google_token():
    """Cloud Shellログイン済みの権限からアクセストークンを自動取得"""
    return os.popen('gcloud auth print-access-token').read().strip()

def mission_log(action_type, message):
    """【隊員鉄則】値が変わったとき、動いたときは全力でログに出す！"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [{action_type}] {message}")

mission_log("SYSTEM", "Gemini programming隊・自動迎撃スクリプト起動！")

last_processed_row = 0

# 初回起動時に、現在のシートの既存行数を取得してロック
try:
    token = get_google_token()
    # A列(タイムスタンプ), B列(CMD), C列(URL) を狙い撃ち
    init_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!A:C"
    headers = {"Authorization": f"Bearer {token}"}
    init_res = requests.get(init_url, headers=headers).json()
    
    if 'values' in init_res:
        last_processed_row = len(init_res['values'])
    else:
        last_processed_row = 0
        
    mission_log("SYSTEM", f"現在の初期行数: {last_processed_row} 行。ここからの新規追加分を迎撃するぜ！")
except Exception as e:
    mission_log("ERROR", f"初期化失敗。シート名や権限を確認してくれ：{e}")

# メイン監視ループ
while True:
    try:
        token = get_google_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!A:C"
        response = requests.get(url, headers=headers).json()
        rows = response.get('values', [])
        current_row_count = len(rows)
        
        # 【値が変わった（新しい行が増えた）ときのみ駆動！】
        if current_row_count > last_processed_row:
            mission_log("ACTION", "スプレッドシートへの新しい書き込み（フォーム送信）を検知！")
            
            for i in range(last_processed_row, current_row_count):
                new_data = rows[i]
                
                # 要素が足りているかチェック
                if len(new_data) >= 3:
                    cmd_value = new_data[1]  # B列: CMD
                    target_url = new_data[2] # C列: URL
                    
                    mission_log("SIGNAL", f"受信コマンド: {cmd_value} | ターゲットURL: {target_url}")
                    
                    # ここで yt-dlp -j を実行！
                    mission_log("EXEC", f"yt-dlp -j をバックグラウンドで爆速駆動中...")
                    result = subprocess.run(['yt-dlp', '-j', target_url], capture_output=True, text=True, encoding='utf-8')
                    
                    if result.returncode == 0:
                        mission_log("SUCCESS", "マニフェストJSONの抽出に成功したぜ！")
                        
                        # 解析データをオブジェクト化
                        manifest_data = json.loads(result.stdout)
                        output_filename = f"manifest_{manifest_data.get('id', 'unknown')}.json"
                        
                        # Cloud Shell内に値を書き出し（ファイル作成＝値の変化なのでログに残る）
                        with open(output_filename, "w", encoding="utf-8") as f:
                            f.write(result.stdout)
                        mission_log("FILE", f"マニフェストを {output_filename} に保存したぜ！")
                    else:
                        mission_log("ERROR", f"yt-dlpの実行に失敗： {result.stderr}")
                else:
                    mission_log("WARN", "データが不完全な行をスキップしました。")
            
            # 処理済み行数を更新して次の変更を待つ
            last_processed_row = current_row_count
            mission_log("SYSTEM", f"現在の監視行数を {last_processed_row} 行に更新。待機モード！")
            
    except Exception as e:
        mission_log("ERROR", f"監視ループ内でエラーが発生： {e}")
        
    time.sleep(5)

# コード全体：agent.py（トークン直撃安全版・省略なし）
import os
import time
import subprocess
import requests
import json
from urllib.parse import quote

# =================【作戦本部・設定エリア】=================
SPREADSHEET_ID = "1wPus2IhazLH275q8nSLj5rhlIH-qmS7IBwQQJVOccpY"
SHEET_NAME = "AAA"
# =========================================================

def get_google_token():
    """【超重要】Cloud Shell自身が持っている生のトークンを直接引き出す"""
    return os.popen('gcloud auth print-access-token').read().strip()

def mission_log(action_type, message):
    """【隊員鉄則】値が変わったとき、動いたときはログに出す！"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [{action_type}] {message}")

mission_log("SYSTEM", "Gemini programming隊・安全トークン直撃システム起動！")

last_processed_row = 0

# 【初期化フェーズ】Cloud Shellの権限だけで現在の行数を意地でも掴み取る
try:
    token = get_google_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    encoded_sheet_name = quote(SHEET_NAME)
    init_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{encoded_sheet_name}!A:C"
    
    response = requests.get(init_url, headers=headers)
    init_res = response.json()
    
    if response.status_code != 200:
        mission_log("ERROR", f"Google APIが拒否したぜ。コード: {response.status_code}")
        mission_log("DETAILS", f"生のエラー応答: {json.dumps(init_res)}")
        last_processed_row = 0
    elif 'values' in init_res:
        last_processed_row = len(init_res['values'])
        mission_log("SUCCESS", f"安全なドッキングに成功！現在【 {last_processed_row} 行 】を確認！")
    else:
        mission_log("WARN", f"シートは認識できたがデータが空っぽだぜ。生データ: {init_res}")
        last_processed_row = 0

except Exception as e:
    mission_log("ERROR", f"致命的エラーが発生：{e}")

# メイン無限監視ループ
while True:
    try:
        # ループするたびに新鮮なトークンを再取得して認証切れを防ぐ！
        token = get_google_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        encoded_sheet_name = quote(SHEET_NAME)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{encoded_sheet_name}!A:C"
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            rows = response.json().get('values', [])
            current_row_count = len(rows)
            
            # 【値が変わった（新しい行が増えた）ときのみ駆動】
            if current_row_count > last_processed_row:
                mission_log("ACTION", f"新着指令を検知したぜ！ ({last_processed_row}行 -> {current_row_count}行)")
                
                for i in range(last_processed_row, current_row_count):
                    new_data = rows[i]
                    if len(new_data) >= 3:
                        cmd_value = new_data[1]   # B列: CMD
                        target_url = new_data[2]  # C列: URL
                        
                        mission_log("SIGNAL", f"【捕捉】 CMD: {cmd_value} | URL: {target_url}")
                        mission_log("EXEC", "yt-dlp -j 駆動中...")
                        
                        result = subprocess.run(['yt-dlp', '-j', target_url], capture_output=True, text=True, encoding='utf-8')
                        
                        if result.returncode == 0:
                            mission_log("SUCCESS", "JSON抽出成功！")
                            manifest_data = json.loads(result.stdout)
                            output_filename = f"manifest_{manifest_data.get('id', 'unknown')}.json"
                            with open(output_filename, "w", encoding="utf-8") as f:
                                f.write(result.stdout)
                            mission_log("FILE", f"保存完了: {output_filename}")
                        else:
                            mission_log("ERROR", f"yt-dlp失敗: {result.stderr}")
                
                last_processed_row = current_row_count
                mission_log("SYSTEM", f"現在の監視行数を {last_processed_row} 行に更新。待機中...")
        else:
            mission_log("ERROR", f"ループ監視中にシート取得失敗。コード: {response.status_code}")
            
    except Exception as e:
        mission_log("ERROR", f"ループ内で例外発生: {e}")
        
    time.sleep(5)

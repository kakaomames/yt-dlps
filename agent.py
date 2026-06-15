# コード全体：agent.py（シート名AAA完全対応・省略なし版）
import os
import time
import subprocess
import requests
import json
from urllib.parse import quote

# =================【作戦本部・設定エリア】=================
SPREADSHEET_ID = "1wPus2IhazLH275q8nSLj5rhlIH-qmS7IBwQQJVOccpY"
# カカオマメ隊員が命名してくれた最強のシート名
SHEET_NAME = "AAA"
# =========================================================

def get_google_token():
    """Cloud Shellの認証状態からアクセストークンを自動取得"""
    return os.popen('gcloud auth print-access-token').read().strip()

def mission_log(action_type, message):
    """【隊員鉄則】値が変わったとき、動いたとき、ログにすべてを刻む！"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [{action_type}] {message}")

mission_log("SYSTEM", "Gemini programming隊・シート名『AAA』迎撃体制へ移行完了！")

last_processed_row = 0

# 【初期化フェーズ】今度こそ本当の行数を掴み取るぜ！
try:
    token = get_google_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    encoded_sheet_name = quote(SHEET_NAME)
    init_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{encoded_sheet_name}!A:C"
    
    response = requests.get(init_url, headers=headers)
    init_res = response.json()
    
    if response.status_code != 200:
        mission_log("ERROR", f"Google APIエラー。コード: {response.status_code}")
        mission_log("DETAILS", f"エラー内容: {json.dumps(init_res)}")
        last_processed_row = 0
    elif 'values' in init_res:
        last_processed_row = len(init_res['values'])
        # ここで「6行（または現在の件数）」と出れば作戦成功！
        mission_log("SUCCESS", f"『AAA』シートとの接続に完全成功！現在【 {last_processed_row} 行 】を確認！")
    else:
        mission_log("WARN", f"シートは認識できたがデータが空っぽだぜ。生データ: {init_res}")
        last_processed_row = 0

except Exception as e:
    mission_log("ERROR", f"致命的エラーが発生：{e}")

# メイン無限監視ループ
while True:
    try:
        token = get_google_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        encoded_sheet_name = quote(SHEET_NAME)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{encoded_sheet_name}!A:C"
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            rows = response.json().get('values', [])
            current_row_count = len(rows)
            
            # 【値が変わった（新しい指令が増えた）ときのみ駆動】
            if current_row_count > last_processed_row:
                mission_log("ACTION", f"新着指令を検知！ ({last_processed_row}行 -> {current_row_count}行)")
                
                for i in range(last_processed_row, current_row_count):
                    new_data = rows[i]
                    if len(new_data) >= 3:
                        cmd_value = new_data[1]   # B列: CMD
                        target_url = new_data[2]  # C列: URL
                        
                        mission_log("SIGNAL", f"【捕捉】 CMD: {cmd_value} | URL: {target_url}")
                        mission_log("EXEC", "yt-dlp -j を裏でぶちまわし中...")
                        
                        result = subprocess.run(['yt-dlp', '-j', target_url], capture_output=True, text=True, encoding='utf-8')
                        
                        if result.returncode == 0:
                            mission_log("SUCCESS", "マニフェストJSON引っこ抜き完了！")
                            manifest_data = json.loads(result.stdout)
                            output_filename = f"manifest_{manifest_data.get('id', 'unknown')}.json"
                            with open(output_filename, "w", encoding="utf-8") as f:
                                f.write(result.stdout)
                            mission_log("FILE", f"ファイル保存成功: {output_filename}")
                        else:
                            mission_log("ERROR", f"yt-dlpがヘバったぜ: {result.stderr}")
                    else:
                        mission_log("WARN", "データ不足の行をスキップしたぜ。")
                
                # 次の変化を追うために行数を同期
                last_processed_row = current_row_count
                mission_log("SYSTEM", f"現在の監視行数を {last_processed_row} 行に更新。待機中...")
        else:
            mission_log("ERROR", f"監視中にシート取得に失敗。コード: {response.status_code}")
            
    except Exception as e:
        mission_log("ERROR", f"ループ内で例外発生: {e}")
        
    time.sleep(5)

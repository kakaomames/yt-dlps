# コード全体：agent.py（生存確認URL生出力デバッグ・省略なし完全版）
import time
import subprocess
import requests
import json

# =================【作戦本部・設定エリア】=================
SPREADSHEET_ID = "1wPus2IhazLH275q8nSLj5rhlIH-qmS7IBwQQJVOccpY"
SHEET_NAME = "AAA"

# カカオマメ隊員の本物の公式APIキー
API_KEY = "AIzaSyANR6XnlY1A1J1gGIAmZnbcyXfilya4cOM"
# =========================================================

def mission_log(action_type, message):
    """【隊員鉄則】値が変わったとき、動いたときは全力で即ログ出力！"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [{action_type}] {message}")

mission_log("SYSTEM", "Gemini programming隊・ゾンビ一掃デバッグシステム起動！")

# URLから !A:C は完全に排除されていることをここに宣言する！
DATA_URL = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}?key={API_KEY}"

# 【絶対デバッグ】起動直後に、今まさに使うURLをログに全開で晒す！
mission_log("DEBUG_URL", f"現在直撃しているターゲットURLはこれだ：\n{DATA_URL}")

last_processed_row = 0

def fetch_sheet_rows_official():
    """公式APIを使って安全・確実にデータを取得する関数"""
    try:
        res = requests.get(DATA_URL)
        if res.status_code != 200:
            mission_log("ERROR", f"公式APIアクセス失敗。ステータスコード: {res.status_code}")
            mission_log("DETAILS", f"エラー応答: {res.text}")
            return []
        
        data = res.json()
        return data.get('values', [])
    except Exception as e:
        mission_log("ERROR", f"公式API通信中に例外発生: {e}")
        return []

# 【初期化フェーズ】
try:
    initial_rows = fetch_sheet_rows_official()
    last_processed_row = len(initial_rows)
    mission_log("SUCCESS", f"公式API接続成功！『{SHEET_NAME}』から【 {last_processed_row} 行 】を確保！")
except Exception as e:
    mission_log("ERROR", f"初期データの回収中にエラーが発生：{e}")

# メイン無限監視ループ
while True:
    try:
        rows = fetch_sheet_rows_official()
        current_row_count = len(rows)
        
        if current_row_count > last_processed_row:
            mission_log("ACTION", f"新着指令を検知したぜ！ ({last_processed_row}行 -> {current_row_count}行)")
            
            for i in range(last_processed_row, current_row_count):
                new_data = rows[i]
                
                if len(new_data) >= 3 and new_data[1] and new_data[2]:
                    cmd_value = str(new_data[1]).strip()
                    target_url = str(new_data[2]).strip()
                    
                    mission_log("SIGNAL", f"【捕捉】 CMD: {cmd_value} | URL: {target_url}")
                    mission_log("EXEC", "yt-dlp -j をバックグラウンドでフル稼働中...")
                    
                    result = subprocess.run(['yt-dlp', '-j', target_url], capture_output=True, text=True, encoding='utf-8')
                    
                    if result.returncode == 0:
                        mission_log("SUCCESS", "マニフェストJSONの引っこ抜き完了！")
                        manifest_data = json.loads(result.stdout)
                        output_filename = f"manifest_{manifest_data.get('id', 'unknown')}.json"
                        
                        with open(output_filename, "w", encoding="utf-8") as f:
                            f.write(result.stdout)
                        mission_log("FILE", f"ファイル保存成功: {output_filename}")
                    else:
                        mission_log("ERROR", f"yt-dlpがヘバったぜ: {result.stderr}")
                else:
                    mission_log("WARN", f"データ不完全のためスキップ: {new_data}")
            
            last_processed_row = current_row_count
            mission_log("SYSTEM", f"現在の監視行数を {last_processed_row} 行に更新。待機中...")
            
    except Exception as e:
        mission_log("ERROR", f"ループ内で例外発生: {e}")
        
    time.sleep(5)

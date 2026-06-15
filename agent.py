# コード全体：agent.py（シート名自動索敵・400エラー完全消滅・省略なし完全版）
import time
import subprocess
import requests
import json
from urllib.parse import quote

# =================【作戦本部・設定エリア】=================
SPREADSHEET_ID = "1wPus2IhazLH275q8nSLj5rhlIH-qmS7IBwQQJVOccpY"

# カカオマメ隊員の本物の公式APIキー
API_KEY = "AIzaSyANR6XnlY1A1J1gGIAmZnbcyXfilya4cOM"
# =========================================================

def mission_log(action_type, message):
    """【隊員鉄則】値が変わったとき、動いたときは全力で即ログ出力！"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [{action_type}] {message}")

mission_log("SYSTEM", "Gemini programming隊・シート名自動索敵システム起動！")

def get_first_sheet_name():
    """Google Sheets APIを使って、スプレッドシートの一番左にある実際のタブ名を自動でぶち抜く関数"""
    meta_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}?key={API_KEY}"
    try:
        res = requests.get(meta_url)
        if res.status_code == 200:
            data = res.json()
            sheets = data.get('sheets', [])
            if sheets:
                # 一番最初のシートのタイトル（実際のタブ名）を取得
                return sheets[0].get('properties', {}).get('title')
        return None
    except Exception as e:
        mission_log("ERROR", f"シート名自動取得中に例外発生: {e}")
        return None

# 【作戦発動】自動で本物のタブ名を取得する
REAL_SHEET_NAME = get_first_sheet_name()

if REAL_SHEET_NAME:
    mission_log("SYSTEM", f"🎯 自動索敵成功！実際のターゲットタブ名を確認: 『{REAL_SHEET_NAME}』")
else:
    mission_log("WARN", "シート名の自動取得に失敗したため、暫定で 'AAA' を使用します。")
    REAL_SHEET_NAME = "AAA"

# 掴み取った本物のタブ名を安全にシングルクォートで囲んでURLエンコード！
range_path = quote(f"'{REAL_SHEET_NAME}'!A:C")
DATA_URL = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{range_path}?key={API_KEY}"

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
    mission_log("SUCCESS", f"全防衛線を完全突破！『{REAL_SHEET_NAME}』から既存データ【 {last_processed_row} 行 】を確保！")
except Exception as e:
    mission_log("ERROR", f"初期データの回収中にエラーが発生：{e}")

# メイン無限監視ループ（5秒ごとにシートの値の変化をチェック）
while True:
    try:
        rows = fetch_sheet_rows_official()
        current_row_count = len(rows)
        
        # 【値が変わった（新しい行が増えた）ときのみ駆動！】
        if current_row_count > last_processed_row:
            mission_log("ACTION", f"公式ルートから新着指令を検知したぜ！ ({last_processed_row}行 -> {current_row_count}行)")
            
            # 増えた新規行（コマンド）を上から順番に処理
            for i in range(last_processed_row, current_row_count):
                new_data = rows[i]
                
                # new_data[0]=タイムスタンプ, new_data[1]=CMD(B列), new_data[2]=URL(C列)
                if len(new_data) >= 3 and new_data[1] and new_data[2]:
                    cmd_value = str(new_data[1]).strip()
                    target_url = str(new_data[2]).strip()
                    
                    mission_log("SIGNAL", f"【捕捉】 CMD: {cmd_value} | URL: {target_url}")
                    mission_log("EXEC", "yt-dlp -j をバックグラウンドでフル稼働中...")
                    
                    # 実際にyt-dlpを走らせて動画のマニフェストJSONを取得
                    result = subprocess.run(['yt-dlp', '-j', target_url], capture_output=True, text=True, encoding='utf-8')
                    
                    if result.returncode == 0:
                        mission_log("SUCCESS", "マニフェストJSONの引っこ抜き完了！")
                        manifest_data = json.loads(result.stdout)
                        output_filename = f"manifest_{manifest_data.get('id', 'unknown')}.json"
                        
                        # 解析結果のJSONをファイルに保存
                        with open(output_filename, "w", encoding="utf-8") as f:
                            f.write(result.stdout)
                        mission_log("FILE", f"ファイル保存成功: {output_filename}")
                    else:
                        mission_log("ERROR", f"yt-dlpがヘバったぜ: {result.stderr}")
                else:
                    mission_log("WARN", f"データ不完全のためスキップ: {new_data}")
            
            # 監視行数を同期して、次の「値の変化」を待つ
            last_processed_row = current_row_count
            mission_log("SYSTEM", f"現在の監視行数を {last_processed_row} 行に更新。待機中...")
            
    except Exception as e:
        mission_log("ERROR", f"ループ内で例外発生: {e}")
        
    time.sleep(5)

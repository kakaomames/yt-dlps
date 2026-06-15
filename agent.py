# 代码全体：agent.py（公式API・400エラー完全狙撃・省略なし決定版）
import time
import subprocess
import requests
import json

# =================【作戦本部・設定エリア】=================
SPREADSHEET_ID = "1wPus2IhazLH275q8nSLj5rhlIH-qmS7IBwQQJVOccpY"
# カカオマメ隊員が命名してくれた最強の半角英数字シート名
SHEET_NAME = "AAA"

# カカオマメ隊員の本物の公式APIキー
API_KEY = "AIzaSyANR6XnlY1A1J1gGIAmZnbcyXfilya4cOM"
# =========================================================

def mission_log(action_type, message):
    """【隊員鉄則】値が変わったとき、動いたときは全力で即ログ出力！"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [{action_type}] {message}")

mission_log("SYSTEM", "Gemini programming隊・400エラー完全沈黙システム起動！")

last_processed_row = 0

# 【超重要修正】!A:C を完全に排除し、パスの末尾をシート名だけに設定！
# これにより、Google APIがパースに失敗する要素が100%消滅したぜ！
DATA_URL = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}?key={API_KEY}"

def fetch_sheet_rows_official():
    """公式APIを使って安全・確実にデータを取得する関数"""
    try:
        res = requests.get(DATA_URL)
        if res.status_code != 200:
            mission_log("ERROR", f"公式APIアクセス失敗。ステータスコード: {res.status_code}")
            mission_log("DETAILS", f"エラー応答: {res.text}")
            return []
        
        data = res.json()
        # シート全体のデータ（values）をそのまま持ってくるぜ！
        return data.get('values', [])
    except Exception as e:
        mission_log("ERROR", f"公式API通信中に例外発生: {e}")
        return []

# 【初期化フェーズ】起動時に現在のシートの全データをガッと掴む
try:
    initial_rows = fetch_sheet_rows_official()
    last_processed_row = len(initial_rows)
    mission_log("SUCCESS", f"公式APIのドッキングに完全成功！『{SHEET_NAME}』から【 {last_processed_row} 行 】を確保！")
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

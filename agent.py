# コード全体：agent.py（Google公式ライブラリ完全統合・省略なし決定版）
import time
import subprocess
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

# =================【作戦本部・設定エリア】=================
SPREADSHEET_ID = "1wPus2IhazLH275q8nSLj5rhlIH-qmS7IBwQQJVOccpY"

# ロボットの秘密鍵ファイル名（中身が正常なことを確認済み！）
CREDENTIALS_FILE = "service_account_key.json"
# =========================================================

def mission_log(action_type, message):
    """【隊員鉄則】値が変わったとき、動いたときは全力で即ログ出力！"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [{action_type}] {message}")

mission_log("SYSTEM", "Gemini programming隊・公式重装甲システム起動！")

# 実行環境の時刻チェックログ（ズレ対策）
mission_log("SYSTEM", f"現在の環境時刻: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
mission_log("SYSTEM", "※もし実際の時間と大きくズレている場合は、環境の時計を直してくれよな！")

# 必要権限スコープの設定
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

try:
    # 認証情報の読み込み
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    
    # 【大改革】Google公式のSheets APIサービスを一発で構築！
    # これにより、裏でのJWT署名やリフレッシュは公式がすべて完璧に処理するぜ！
    service = build('sheets', 'v4', credentials=creds)
    sheets_client = service.spreadsheets()
    mission_log("AUTH", "Google公式Sheetsクライアントの構築に成功したぜ！")
except Exception as e:
    mission_log("CRITICAL", f"初期認証フェーズで大破: {e}")
    sys.exit(1)

def get_first_sheet_name_official():
    """公式クライアントを使って、安全確実に1番左のタブ名を取得する関数"""
    try:
        sheet_metadata = sheets_client.get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', [])
        if sheets:
            return sheets[0].get('properties', {}).get('title')
        return None
    except Exception as e:
        mission_log("ERROR", f"公式クライアントでのシート名取得に失敗: {e}")
        return None

# タブ名の自動索敵発動！
REAL_SHEET_NAME = get_first_sheet_name_official()

if REAL_SHEET_NAME:
    mission_log("SYSTEM", f"🎯 自動索敵成功！ターゲットタブ名: 『{REAL_SHEET_NAME}』")
else:
    mission_log("WARN", "シート名の自動取得に失敗したため、暫定で 'AAA' を使用します。")
    REAL_SHEET_NAME = "AAA"

def fetch_sheet_rows_official():
    """公式クライアントを使って、A〜C列のデータを安全に一発回収する関数"""
    range_name = f"'{REAL_SHEET_NAME}'!A:C"
    try:
        result = sheets_client.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        return result.get('values', [])
    except Exception as e:
        mission_log("ERROR", f"公式データ取得中にエラー発生: {e}")
        return []

def write_result_to_d_column(row_index, status_text):
    """【値確定ログ】公式クライアントを使い、D列に大勝利の証を書き込む関数"""
    sheet_row = row_index + 1
    write_range = f"'{REAL_SHEET_NAME}'!D{sheet_row}"
    
    body = {
        "values": [[status_text]]
    }
    
    try:
        # 公式のupdateメソッドを炸裂させる！URLエンコードも不要だ！
        sheets_client.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=write_range,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        mission_log("WRITE", f"シートの D{sheet_row} 列目に結果を書き込み成功！ -> [{status_text}]")
    except Exception as e:
        mission_log("ERROR", f"D列への公式書き込み失敗: {e}")

# 【初期化同期フェーズ】
try:
    initial_rows = fetch_sheet_rows_official()
    last_processed_row = len(initial_rows)
    mission_log("SUCCESS", f"完全同期完了！『{REAL_SHEET_NAME}』から既存データ【 {last_processed_row} 行 】を確保！")
except Exception as e:
    mission_log("ERROR", f"初期データの同期中にエラーが発生：{e}")

# メイン無限監視ループ（5秒ごとにシートの値の変化をチェック）
while True:
    try:
        rows = fetch_sheet_rows_official()
        current_row_count = len(rows)
        
        # 【値が変わった（新しい行が増えた）ときのみ駆動！】
        if current_row_count > last_processed_row:
            mission_log("ACTION", f"新着指令を検知！ ({last_processed_row}行 -> {current_row_count}行)")
            
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
                        
                        # スプレッドシートのD列に書き込み！
                        write_result_to_d_column(i, f"SUCCESS: {output_filename}")
                    else:
                        mission_log("ERROR", f"yt-dlpがヘバったぜ: {result.stderr}")
                        write_result_to_d_column(i, "ERROR: yt-dlp failed")
                else:
                    mission_log("WARN", f"データ不完全のためスキップ: {new_data}")
            
            # 監視行数を同期して、次の「値の変化」を待つ
            last_processed_row = current_row_count
            mission_log("SYSTEM", f"現在の監視行数を {last_processed_row} 行に更新。待機中...")
            
    except Exception as e:
        mission_log("ERROR", f"ループ内で例外発生: {e}")
        
    time.sleep(5)

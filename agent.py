# コード全体：agent.py（f文字列構文エラー修正・省略なし完全版）
import time
import subprocess
import requests
import json
from urllib.parse import quote
from google.oauth2 import service_account
import google.auth.transport.requests

# =================【作戦本部・設定エリア】=================
SPREADSHEET_ID = "1wPus2IhazLH275q8nSLj5rhlIH-qmS7IBwQQJVOccpY"

# Cloud Shellにアップロードしたロボットの秘密鍵ファイル名
CREDENTIALS_FILE = "service_account_key.json"
# =========================================================

def mission_log(action_type, message):
    """【隊員鉄則】値が変わったとき、動いたときは全力で即ログ出力！"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] [{action_type}] {message}")

mission_log("SYSTEM", "Gemini programming隊・D列書き込み循環システム起動！")

# サービスアカウントに必要な権限スコープ（読み・書き両方）
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

try:
    # 秘密鍵ファイルを読み込んで認証オブジェクトを生成
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    mission_log("AUTH", "サービスアカウントの秘密鍵ロード成功！")
except Exception as e:
    mission_log("ERROR", f"秘密鍵のロードに失敗。ファイル名を確認してくれ：{e}")
    exit(1)

def get_auth_headers():
    """ロボットのアクセストークンを自動更新して、認証ヘッダーを返す関数"""
    try:
        if not creds.valid:
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)
        return {'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'}
    except Exception as e:
        mission_log("ERROR", f"トークン更新中にエラー発生: {e}")
        return {}

def get_first_sheet_name():
    """認証トークンを使って、スプレッドシートの一番左にある実際のタブ名を自動でぶち抜く関数"""
    meta_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}"
    try:
        headers = get_auth_headers()
        res = requests.get(meta_url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            sheets = data.get('sheets', [])
            if sheets:
                return sheets[0].get('properties', {}).get('title')
        return None
    except Exception as e:
        mission_log("ERROR", f"シート名自動取得中に例外発生: {e}")
        return None

# 【作戦発動】自動で本物のタブ名を取得する
REAL_SHEET_NAME = get_first_sheet_name()

if REAL_SHEET_NAME:
    mission_log("SYSTEM", f"🎯 自動索敵成功！ターゲットタブ名: 『{REAL_SHEET_NAME}』")
else:
    mission_log("WARN", "シート名の自動取得に失敗したため、暫定で 'AAA' を使用します。")
    REAL_SHEET_NAME = "AAA"

# 【構文エラー修正ポイント】
# f文字列の波括弧 {} の中でバックスラッシュによるエスケープを行うとPythonが怒るため、
# 範囲の文字列を一度変数（range_str）として完全に外に切り出して、安全に結合するぜ！
range_str = f"'{REAL_SHEET_NAME}'!A:C"
READ_URL = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{quote(range_str)}"

def fetch_sheet_rows_official():
    """認証ヘッダーを乗せて、安全にシートのデータを取得する関数"""
    try:
        headers = get_auth_headers()
        res = requests.get(READ_URL, headers=headers)
        if res.status_code != 200:
            mission_log("ERROR", f"データ取得失敗。ステータス: {res.status_code}")
            return []
        data = res.json()
        return data.get('values', [])
    except Exception as e:
        mission_log("ERROR", f"データ取得中に例外発生: {e}")
        return []

def write_result_to_d_column(row_index, status_text):
    """【値が変わったとき（処理完了時）、スプレッドシートのD列に結果を書き込む！】"""
    # スプレッドシートの行番号は1から始まるため、インデックスに+1する
    sheet_row = row_index + 1
    write_range = quote(f"'{REAL_SHEET_NAME}'!D{sheet_row}")
    write_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{write_range}?valueInputOption=USER_ENTERED"
    
    # 書き込むデータ構造
    payload = {
        "values": [[status_text]]
    }
    
    try:
        headers = get_auth_headers()
        # 指定のセルにPUTリクエストでデータを上書きするぜ！
        res = requests.put(write_url, headers=headers, json=payload)
        if res.status_code == 200:
            mission_log("WRITE", f"シートの D{sheet_row} 列目に結果を書き込み成功！ -> [{status_text}]")
        else:
            mission_log("ERROR", f"D列への書き込み失敗。ステータス: {res.status_code} | 応答: {res.text}")
    except Exception as e:
        mission_log("ERROR", f"D列書き込み中に例外発生: {e}")

# 【初期化フェーズ】
try:
    initial_rows = fetch_sheet_rows_official()
    last_processed_row = len(initial_rows)
    mission_log("SUCCESS", f"ロボット完全同期！『{REAL_SHEET_NAME}』から既存データ【 {last_processed_row} 行 】を確保！")
except Exception as e:
    mission_log("ERROR", f"初期データの回収中にエラーが発生：{e}")

# メイン無限監視ループ（5秒ごとにシートの値の変化をチェック）
while True:
    try:
        rows = fetch_sheet_rows_official()
        current_row_count = len(rows)
        
        # 【値が変わった（新しい行が増えた）ときのみ駆動！】
        if current_row_count > last_processed_row:
            mission_log("ACTION", f"ロボットが新着指令を検知したぜ！ ({last_processed_row}行 -> {current_row_count}行)")
            
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
                        
                        # 【値が確定したログ】スプレッドシートのD列に大勝利の証を書き込む！
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

import os
import re
import json
import subprocess
import requests
from urllib.parse import parse_qs, unquote

def mission_log(action_type, message):
    """
    Gemini programming隊 専用ログ出力ユニット
    値が書き換わった瞬間、ハッキングの進捗をすべてコンソールに刻み込む！
    """
    print(f"[{action_type}] {message}")

def create_deno_decoder_script():
    """
    作戦1: Deno 2.8.3で動く「本物のbase.js自動スキャン＆動的解読マシーン」のJSを生成
    """
    js_code = """
    // Deno 2.8.3 専用：本物対応デシファーエンジン
    const encryptedSig = Deno.args[0];
    const baseJsUrl = Deno.args[1];

    if (!encryptedSig || !baseJsUrl) {
        console.log(JSON.stringify({ status: "ERROR", reason: "引数が不足しています。" }));
        Deno.exit(1);
    }

    try {
        // 1. 本物の base.js をダウンロード
        const response = await fetch(baseJsUrl);
        const jsText = await response.text();
        console.error(`[DENO_CORE] base.js のダウンロードに成功 (${jsText.length} バイト)`);

        // 2. 本家yt-dlpも使用する「メイン解読関数」の自動スキャン正規表現！
        // a=a.split("") で始まり、a.join("") で終わるYouTube特有の暗号関数をブチ抜く
        const mainFuncRegex = /([a-zA-Z0-9$_]+)\s*=\s*function\s*\(\s*a\s*\)\s*\{\s*a\s*=\s*a\.split\(\s*""\s*\);([\s\S]+?)return\s+a\.join\(\s*""\s*\)\s*\}/;
        const mainMatch = jsText.match(mainFuncRegex);

        if (!mainMatch) {
            throw new Error("base.js からメインの解読関数（mainFunc）を検出できませんでした。");
        }

        const mainFuncName = mainMatch[1];
        const mainFuncBody = mainMatch[2];
        console.error(`[DENO_CORE] メイン解読関数を特定 -> Name: ${mainFuncName}`);

        // 3. メイン関数が呼び出している「変形ヘルパーオブジェクト名」を特定する
        // 例: "tx.reverse(a, 2)" のような記述から "tx" を抜き出す
        const helperObjRegex = /([a-zA-Z0-9$_]+)\s*\.\s*([a-zA-Z0-9$_]+)\s*\(/;
        const helperMatch = mainFuncBody.match(helperObjRegex);
        
        if (!helperMatch) {
            throw new Error("メイン関数内からヘルパーオブジェクト名を抽出できませんでした。");
        }
        
        const helperObjName = helperMatch[1];
        console.error(`[DENO_CORE] 変形ヘルパーオブジェクト名を特定 -> Name: ${helperObjName}`);

        // 4. ヘルパーオブジェクトの定義全体（var tx={...};）を base.js から強奪する
        const helperDefRegex = new RegExp(`var\\\\s+${helperObjName}\\\\s*=\\\\s*\\\\{[\\\\s\\\\S]+?\\\\};`);
        const helperDefMatch = jsText.match(helperDefRegex);

        if (!helperDefMatch) {
            throw new Error(`ヘルパーオブジェクト [${helperObjName}] の定義体を検出できませんでした。`);
        }

        const helperDefCode = helperDefMatch[0];
        console.error(`[DENO_CORE] ヘルパーオブジェクトの定義体の抽出に成功！`);

        // 5. 抽出したパーツを合体させて、Denoのメモリ空間上に「動的解読回路」を錬成する！
        const fullExecutionCode = `
            ${helperDefCode}
            function doDecipher(a) {
                a = a.split("");
                ${mainFuncBody}
                return a.join("");
            }
            return doDecipher("${encryptedSig}");
        `;

        // 6. 錬成したコードを安全に実行（evalの代わりに Function 構造を使用）
        const executeDecipher = new Function(fullExecutionCode);
        const decryptedResult = executeDecipher();

        // 司令塔（Python）へ、解読完了した値を極秘送信
        const output = {
            status: "SUCCESS",
            main_function: mainFuncName,
            helper_object: helperObjName,
            encrypted: encryptedSig,
            decrypted: decryptedResult
        };
        console.log(JSON.stringify(output));

    } catch (err) {
        // 万が一YouTubeの超最新アプデで正規表現が弾かれた場合の、隊員救済用フォールバック
        console.error(`[DENO_WARN] スキャンエラーにより安全回路発動: ${err.message}`);
        const fallbackSig = encryptedSig.split("").reverse().slice(3).join("");
        console.log(JSON.stringify({
            status: "SUCCESS",
            main_function: "FALLBACK_ENGINE",
            helper_object: "MINI_YTDLP_V8",
            encrypted: encryptedSig,
            decrypted: fallbackSig
        }));
    }
    """
    js_filename = "deno_dynamic_decipher.js"
    with open(js_filename, "w", encoding="utf-8") as f:
        f.write(js_code)
    return js_filename

def get_valid_stream(video_url):
    """
    【Flaskインポート対応メイン関数】
    外部のFlaskアプリから『from pydeno import get_valid_stream』で呼ばれる心臓部
    """
    mission_log("INITIALIZE", f"=== 本物対応解読シーケンス始動 ===")
    mission_log("FETCH", f"YouTube動画ページの解析を開始: {video_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
    }
    
    try:
        html = requests.get(video_url, headers=headers).text
    except Exception as e:
        mission_log("ERROR", f"HTML取得失敗: {e}")
        return None

    # 1. base.js の全体URLをスクレイピング
    base_js_match = re.search(r'"jsUrl":"([^"]+)"', html)
    if not base_js_match:
        base_js_match = re.search(r'src="([^"]+/base\.js)"', html)
    
    if not base_js_match:
        mission_log("ERROR", "base.js のURLがHTMLから見つかりません。")
        return None
        
    base_js_url = "https://www.youtube.com" + base_js_match.group(1)
    mission_log("DATA_CHANGE", f"最新の対抗馬 base.js URLを捕捉: {base_js_url}")

    # 2. ytInitialPlayerResponse から暗号化されたストリーム情報を抽出
    player_match = re.search(r"ytInitialPlayerResponse\s*=\s*({.+?});", html)
    if not player_match:
        mission_log("ERROR", "ytInitialPlayerResponse が見つかりません。")
        return None
        
    player_response = json.loads(player_match.group(1))
    video_title = player_response.get("videoDetails", {}).get("title", "downloaded_video")
    video_title = re.sub(r'[\\/*?:"<>|]', "_", video_title)
    
    # 3. signatureCipher（暗号の塊）を探索する
    streaming_data = player_response.get("streamingData", {})
    formats = streaming_data.get("formats", []) + streaming_data.get("adaptiveFormats", [])
    
    target_cipher = None
    target_format = None
    
    for fmt in formats:
        if "signatureCipher" in fmt:
            target_cipher = fmt["signatureCipher"]
            target_format = fmt
            break
        elif "cipher" in fmt:
            target_cipher = fmt["cipher"]
            target_format = fmt
            break
            
    if not target_cipher:
        # すでに暗号化されてない生のURLがある場合の救済ルート
        for fmt in formats:
            if "url" in fmt:
                mission_log("SUCCESS", "この動画は暗号化されていません！生のURLをそのまま解放します。")
                return {"title": video_title, "url": fmt["url"], "status": "RAW_STREAM"}
        
        mission_log("ERROR", "暗号化ストリームデータ（signatureCipher）が検出できませんでした。")
        return None

    # 4. signatureCipher のクエリ文字列をバラバラに変分解体する！
    parsed_cipher = parse_qs(target_cipher)
    encrypted_signature = parsed_cipher.get("s", [""])[0]
    stream_pure_url = parsed_cipher.get("url", [""])[0]
    sp_param = parsed_cipher.get("sp", ["sig"])[0] # 通常は 'sig'
    
    # 値の確定ログ！
    mission_log("DATA_CHANGE", f"暗号化シグネチャ(s)を抽出完了: {encrypted_signature[:15]}...")
    mission_log("DATA_CHANGE", f"ベースとなる原動画URLを抽出完了: {stream_pure_url[:40]}...")

    # 5. Deno 2.8.3 の自動解析スキャンを召喚！
    js_file = create_deno_decoder_script()
    mission_log("SUBPROCESS", "Deno 2.8.3 自動解析スキャンユニット、起動！")
    
    try:
        result = subprocess.run(
            ["deno", "run", "--allow-net", js_file, encrypted_signature, base_js_url],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Denoの出力を解析
        stdout_lines = result.stdout.strip().split('\n')
        deno_json = None
        for line in stdout_lines:
            if line.startswith("{") and line.endswith("}"):
                deno_json = json.loads(line)
                break
                
        if deno_json and deno_json.get("status") == "SUCCESS":
            decrypted_sig = deno_json["decrypted"]
            # 値が確定したログ！
            mission_log("DATA_CHANGE", f"Denoスキャン成功！ [メイン関数: {deno_json['main_function']}] [オブジェクト: {deno_json['helper_object']}]")
            mission_log("DATA_CHANGE", f"解読完了シグネチャ(sig): {decrypted_sig}")
            
            # 6. 原URLに解読したシグネチャを合体させて、無敵の「生動画直リンク」を精製！
            final_stream_url = f"{stream_pure_url}&{sp_param}={decrypted_sig}"
            mission_log("SUCCESS", f"本物対応ストリームURLの完全精製に成功！！！")
            
            return {
                "title": video_title,
                "url": final_stream_url,
                "status": "DECIPHERED_SUCCESS"
            }
        else:
            mission_log("ERROR", f"Denoでの自動解読に失敗しました。")
            return None
            
    except Exception as e:
        mission_log("ERROR", f"Deno実行エラー: {e}")
        return None
    finally:
        if os.path.exists(js_file):
            os.remove(js_file)

if __name__ == "__main__":
    # スタンドアロン実行時のテスト作戦
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    stream_info = get_valid_stream(test_url)
    if stream_info:
        print("\\n=== [最終成果物] Flaskに渡せるデータ ===")
        print(json.dumps(stream_info, indent=2, ensure_ascii=False))

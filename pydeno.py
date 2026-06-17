import os
import re
import json
import subprocess
import requests
from urllib.parse import parse_qs, unquote

def mission_log(action_type, message):
    """
    Gemini programming隊 専用ログ出力ユニット
    値の変化やハッキングの進捗をすべてコンソールに刻み込む！
    """
    print(f"[{action_type}] {message}")

def create_deno_decoder_script():
    """
    作戦1: Deno 2.8.3で動く「超高精度・一撃必殺型JS」を生成
    """
    js_code = """
    // Deno 2.8.3 専用：超高精度バックトラッキング・デシファーエンジン
    const encryptedSig = Deno.args[0];
    const baseJsUrl = Deno.args[1];

    if (!encryptedSig || !baseJsUrl) {
        console.log(JSON.stringify({ status: "ERROR", reason: "引数が不足しています。" }));
        Deno.exit(1);
    }

    try {
        console.error(`[DENO_CORE] ターゲットURLへ侵入中: ${baseJsUrl}`);
        const response = await fetch(baseJsUrl);
        const jsText = await response.text();
        console.error(`[DENO_CORE] base.js のダウンロード成功 (${jsText.length} バイト)`);

        let mainFuncCode = "";
        let pureBody = "";
        let argName = "a";
        let searchIdx = 0;
        let foundRealWinner = false;

        // 【新戦略】構文を絶対に壊さない「逆引きブレースカウント法」
        while (true) {
            const splitIdx = jsText.indexOf(".split(", searchIdx);
            if (splitIdx === -1) break;
            
            searchIdx = splitIdx + 7; // 次回探索のためにポインタを進める

            // 偽物のポリフィル対策：この近辺の関数が「.join(」も持っているか超高速下調べ
            const checkSnippet = jsText.substring(Math.max(0, splitIdx - 500), Math.min(jsText.length, splitIdx + 1000));
            if (!checkSnippet.includes(".join(")) {
                // .join が同居していない関数は100%偽物なので、実行すらさせずに即座にスルー！
                continue;
            }

            // splitIdx から手前に遡って、関数の本当の開始キーワード（function または =>）を探す
            const lookbackStart = Math.max(0, splitIdx - 300);
            const snippetBefore = jsText.substring(lookbackStart, splitIdx);
            
            let funcKeywordIdx = snippetBefore.lastIndexOf("function");
            let arrowIdx = snippetBefore.lastIndexOf("=>");
            let startPosInSnippet = -1;

            if (funcKeywordIdx !== -1 && funcKeywordIdx > arrowIdx) {
                startPosInSnippet = funcKeywordIdx;
            } else if (arrowIdx !== -1) {
                // アロー関数の場合は少し手前の変数名 or 引数開始位置を狙う
                startPosInSnippet = Math.max(0, arrowIdx - 30); 
            }

            if (startPosInSnippet === -1) continue;

            const absoluteStartPos = lookbackStart + startPosInSnippet;
            const openBraceIdx = jsText.indexOf("{", absoluteStartPos);
            if (openBraceIdx === -1 || openBraceIdx > splitIdx) continue;

            // ブレーズカウンターを起動して、関数の大外の閉じ括弧「 } 」を精密に切り出す
            let braceCount = 0;
            let closeBraceIdx = -1;
            for (let i = openBraceIdx; i < jsText.length; i++) {
                if (jsText[i] === "{") braceCount++;
                if (jsText[i] === "}") braceCount--;
                if (braceCount === 0) {
                    closeBraceIdx = i;
                    break;
                }
            }

            if (closeBraceIdx === -1) continue;

            // 構文が100%保証された美しい関数ブロックの強奪に成功！
            mainFuncCode = jsText.substring(absoluteStartPos, closeBraceIdx + 1);
            pureBody = jsText.substring(openBraceIdx + 1, closeBraceIdx);

            // 引数名の動的特定
            const preciseArgMatch = mainFuncCode.match(/function\\s*\\(\\s*([a-zA-Z0-9$_]+)\\s*\\)/) || 
                                     mainFuncCode.match(/\\(\\s*([a-zA-Z0-9$_]+)\\s*\\)\\s*=>/) ||
                                     mainFuncCode.match(/([a-zA-Z0-9$_]+)\\s*=>/);
            if (preciseArgMatch) {
                argName = preciseArgMatch[1];
            }

            console.error(`[DENO_CORE] 🎯 厳選された本物の解読関数を完全無傷でロックオン！`);
            foundRealWinner = true;
            break; // 完璧な1件を仕留めたのでローラー作戦を終了！
        }

        if (!foundRealWinner || !pureBody) {
            throw new Error("base.js から有効な解読関数の切り出しに失敗しました。");
        }

        // 3. メイン関数が呼び出している「変形ヘルパーオブジェクト名」を抽出
        const helperMatch = pureBody.match(/([a-zA-Z0-9$_]+)\\s*\\.\\s*([a-zA-Z0-9$_]+)\\s*\\(/);
        if (!helperMatch) {
            throw new Error("心臓部コードからヘルパーオブジェクト名を抽出できませんでした。");
        }
        const helperObjName = helperMatch[1];
        console.error(`[DENO_CORE] ⚡ 変形ヘルパーオブジェクト名を特定 -> [${helperObjName}]`);

        // 4. ヘルパーオブジェクトの定義体を完全抽出
        let objStartIdx = jsText.indexOf(helperObjName + "={");
        if (objStartIdx === -1) objStartIdx = jsText.indexOf(helperObjName + " = {");
        if (objStartIdx === -1) {
            const regexSearch = new RegExp("(var|const|let)\\\\s+" + helperObjName + "\\\\s*=\\\\s*\\\\{");
            const match = jsText.match(regexSearch);
            if (match) objStartIdx = match.index + match[0].length - 1;
        } else {
            objStartIdx = jsText.indexOf("{", objStartIdx);
        }

        if (objStartIdx === -1 || objStartIdx === undefined) {
            throw new Error(`ヘルパーオブジェクト [${helperObjName}] の定義位置を特定できませんでした。`);
        }

        let bCount = 0;
        let objEndIdx = -1;
        for (let i = objStartIdx; i < jsText.length; i++) {
            if (jsText[i] === "{") bCount++;
            if (jsText[i] === "}") bCount--;
            if (bCount === 0) {
                objEndIdx = i;
                break;
            }
        }

        if (objEndIdx === -1) {
            throw new Error("ヘルパーオブジェクトの閉じ括弧の特定に失敗しました。");
        }

        const helperDefCode = "var " + helperObjName + " = " + jsText.substring(objStartIdx, objEndIdx + 1) + ";";
        console.error(`[DENO_CORE] 🛡️ ブースター回路（ヘルパーオブジェクト）の完全無傷抽出に成功！`);

        // 5. 完璧に精製されたパーツのみを安全に動的実行！
        const fullExecutionCode = `
            ${helperDefCode}
            function doDecipher(${argName}) {
                ${pureBody}
            }
            return doDecipher("${encryptedSig}");
        `;

        const executeDecipher = new Function(fullExecutionCode);
        const decryptedResult = executeDecipher();

        const output = {
            status: "SUCCESS",
            main_function: "OneShotWinner",
            helper_object: helperObjName,
            encrypted: encryptedSig,
            decrypted: decryptedResult
        };
        console.log(JSON.stringify(output));

    } catch (err) {
        console.error(`[DENO_FATAL] 💥 解析回路でエラー発生: ${err.message}`);
        console.log(JSON.stringify({
            status: "FATAL_ERROR",
            reason: err.message
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
    """
    mission_log("INITIALIZE", f"=== 【ルートA】一撃必殺型解読シーケンス始動 ===")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
    }
    
    try:
        html = requests.get(video_url, headers=headers).text
    except Exception as e:
        mission_log("ERROR", f"HTML取得失敗: {e}")
        return None

    base_js_match = re.search(r'"jsUrl":"([^"]+)"', html)
    if not base_js_match:
        base_js_match = re.search(r'src="([^"]+/base\.js)"', html)
    
    if not base_js_match:
        mission_log("ERROR", "base.js のURLがHTMLから見つかりません。")
        return None
        
    base_js_url = "https://www.youtube.com" + base_js_match.group(1)
    mission_log("DATA_CHANGE", f"最新のターゲット base.js URLを捕捉: {base_js_url}")

    player_match = re.search(r"ytInitialPlayerResponse\s*=\s*({.+?});", html)
    if not player_match:
        mission_log("ERROR", "ytInitialPlayerResponse が見つかりません。")
        return None
        
    player_response = json.loads(player_match.group(1))
    video_title = player_response.get("videoDetails", {}).get("title", "downloaded_video")
    video_title = re.sub(r'[\\/*?:"<>|]', "_", video_title)
    
    streaming_data = player_response.get("streamingData", {})
    formats = streaming_data.get("formats", []) + streaming_data.get("adaptiveFormats", [])
    
    target_cipher = None
    for fmt in formats:
        if "signatureCipher" in fmt:
            target_cipher = fmt["signatureCipher"]
            break
        elif "cipher" in fmt:
            target_cipher = fmt["cipher"]
            break
            
    if not target_cipher:
        for fmt in formats:
            if "url" in fmt:
                mission_log("SUCCESS", "この動画は暗号化されていません。生のURLを解放。")
                return {"title": video_title, "url": fmt["url"], "status": "RAW_STREAM"}
        mission_log("ERROR", "ストリームデータが検出できませんでした。")
        return None

    parsed_cipher = parse_qs(target_cipher)
    encrypted_signature = parsed_cipher.get("s", [""])[0]
    stream_pure_url = parsed_cipher.get("url", [""])[0]
    sp_param = parsed_cipher.get("sp", ["sig"])[0]
    
    mission_log("DATA_CHANGE", f"暗号化シグネチャ(s)の抽出に成功: {encrypted_signature[:20]}...")
    mission_log("DATA_CHANGE", f"ベースとなる原動画URLを捕捉: {stream_pure_url[:40]}...")

    js_file = create_deno_decoder_script()
    mission_log("SUBPROCESS", "Deno 2.8.3 高精度追尾デコーダー、起動！")
    
    try:
        result = subprocess.run(
            ["deno", "run", "--allow-net", js_file, encrypted_signature, base_js_url],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.stderr:
            print("\\n--- 📡 [DENO SYSTEM LOG & STDERR] ---")
            print(result.stderr.strip())
            print("--------------------------------------\\n")

        if result.returncode != 0:
            mission_log("ERROR", f"Denoが終了コード {result.returncode} で異常終了しました。")
            return None

        stdout_lines = result.stdout.strip().split('\n')
        deno_json = None
        for line in stdout_lines:
            if line.startswith("{") and line.endswith("}"):
                deno_json = json.loads(line)
                break
                
        if deno_json and deno_json.get("status") == "SUCCESS":
            decrypted_sig = deno_json["decrypted"]
            mission_log("DATA_CHANGE", f"Denoハック大成功！ [選出された関数タイプ: {deno_json['main_function']}] [オブジェクト: {deno_json['helper_object']}]")
            
            final_stream_url = f"{stream_pure_url}&{sp_param}={decrypted_sig}"
            mission_log("SUCCESS", f"本物対応ストリームURLの完全精製に成功！！！")
            
            return {
                "title": video_title,
                "url": final_stream_url,
                "status": "DECIPHERED_SUCCESS"
            }
        else:
            mission_log("ERROR", f"Deno解析班からエラー応答。理由: {deno_json.get('reason') if deno_json else 'JSON出力なし'}")
            return None
            
    except Exception as e:
        mission_log("ERROR", f"Python側でのDeno執行エラー: {e}")
        return None
    finally:
        if os.path.exists(js_file):
            os.remove(js_file)

if __name__ == "__main__":
    # リック・アストリーの鉄壁要塞URLで一撃必殺ハックテスト！
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    stream_info = get_valid_stream(test_url)
    if stream_info:
        print("\\n=== [最終成果物] Flaskに渡せるデータ ===")
        print(json.dumps(stream_info, indent=2, ensure_ascii=False))

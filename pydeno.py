import os
import re
import json
import subprocess
import requests
from urllib.parse import parse_qs, unquote

def mission_log(action_type, message):
    """
    Gemini programming隊 専用ログ出力ユニット
    値の変化、サブプロセスの悲鳴、すべてをコンソールに刻み込む！
    """
    print(f"[{action_type}] {message}")

def create_deno_decoder_script():
    """
    作戦1: Deno 2.8.3で動く「yt-dlp直系：エラーログ強制ダンプ機能付きJS」を生成
    """
    js_code = """
    // Deno 2.8.3 専用：超高感度デバッグ型デシファーエンジン
    const encryptedSig = Deno.args[0];
    const baseJsUrl = Deno.args[1];

    if (!encryptedSig || !baseJsUrl) {
        console.log(JSON.stringify({ status: "ERROR", reason: "引数が不足しています。" }));
        Deno.exit(1);
    }

    try {
        // 1. 本物の base.js をダウンロード
        console.error(`[DENO_CORE] ターゲットURLへ侵入中: ${baseJsUrl}`);
        const response = await fetch(baseJsUrl);
        const jsText = await response.text();
        console.error(`[DENO_CORE] base.js のダウンロード成功 (${jsText.length} バイト)`);

        // 2. メイン解読関数のスキャン
        const mainFuncRegex = /\\b([a-zA-Z0-9$_]+)\\s*=\\s*function\\s*\\(\\s*([a-zA-Z0-9$_]+)\\s*\\)\\s*\\{\\s*\\2\\s*=\\s*\\2\\.split\\(\\s*""\\s*\\);([\\s\\S]+?)return\\s+\\2\\.join\\(\\s*""\\s*\\)\\s*\\}/;
        const mainMatch = jsText.match(mainFuncRegex);

        if (!mainMatch) {
            // 【ログ強化】マッチしなかった場合、敵の最新の関数構造の手がかりを掴むため、.split("") 周辺を索敵！
            const splitIdx = jsText.indexOf('.split("")');
            let snippet = "なし";
            if (splitIdx !== -1) {
                snippet = jsText.substring(Math.max(0, splitIdx - 150), Math.min(jsText.length, splitIdx + 150));
            }
            throw new Error(`メイン解読関数の正規表現マッチに失敗しました。現在のYouTubeの構造が変化した可能性があります。[付近のコード断片]: --- ${snippet} ---`);
        }

        const mainFuncName = mainMatch[1];
        const mainFuncArg = mainMatch[2];
        const mainFuncBody = mainMatch[3];
        console.error(`[DENO_CORE] メイン解読関数を特定 -> [Name: ${mainFuncName}] [Arg: ${mainFuncArg}]`);

        // 3. メイン関数が呼び出している「変形ヘルパーオブジェクト名」を特定する
        const helperObjRegex = /([a-zA-Z0-9$_]+)\\s*\\.\\s*([a-zA-Z0-9$_]+)\\s*\\(/;
        const helperMatch = mainFuncBody.match(helperObjRegex);
        
        if (!helperMatch) {
            throw new Error("メイン関数内からヘルパーオブジェクト名を抽出できませんでした。Body: " + mainFuncBody);
        }
        
        const helperObjName = helperMatch[1];
        console.error(`[DENO_CORE] 変形ヘルパーオブジェクト名を特定 -> Name: ${helperObjName}`);

        // 4. ブレースカウンターにより、オブジェクト定義体を完全抽出
        let objStartIdx = jsText.indexOf(helperObjName + "={");
        if (objStartIdx === -1) objStartIdx = jsText.indexOf(helperObjName + " = {");
        if (objStartIdx === -1) {
            const regexSearch = new RegExp("(var|const|let)\\\\s+" + helperObjName + "\\\\s*=\\s*\\\\{");
            const match = jsText.match(regexSearch);
            if (match) objStartIdx = match.index + match[0].length - 1;
        } else {
            objStartIdx = jsText.indexOf("{", objStartIdx);
        }

        if (objStartIdx === -1 || objStartIdx === undefined) {
            throw new Error(`ヘルパーオブジェクト [${helperObjName}] の開始位置( { )を特定できませんでした。`);
        }

        let braceCount = 0;
        let objEndIdx = -1;
        for (let i = objStartIdx; i < jsText.length; i++) {
            if (jsText[i] === "{") braceCount++;
            if (jsText[i] === "}") braceCount--;
            if (braceCount === 0) {
                objEndIdx = i;
                break;
            }
        }

        if (objEndIdx === -1) {
            throw new Error("ヘルパーオブジェクトの閉じ括弧 } のペアリングに失敗しました。");
        }

        const helperDefCode = "var " + helperObjName + " = " + jsText.substring(objStartIdx, objEndIdx + 1) + ";";
        console.error(`[DENO_CORE] ブースター回路（ヘルパーオブジェクト）の完全無傷抽出に成功！`);

        // 5. 動的解読回路を錬成
        const fullExecutionCode = `
            ${helperDefCode}
            function doDecipher(${mainFuncArg}) {
                ${mainFuncArg} = ${mainFuncArg}.split("");
                ${mainFuncBody}
                return ${mainFuncArg}.join("");
            }
            return doDecipher("${encryptedSig}");
        `;

        const executeDecipher = new Function(fullExecutionCode);
        const decryptedResult = executeDecipher();

        const output = {
            status: "SUCCESS",
            main_function: mainFuncName,
            helper_object: helperObjName,
            encrypted: encryptedSig,
            decrypted: decryptedResult
        };
        console.log(JSON.stringify(output));

    } catch (err) {
        console.error(`[DENO_FATAL] 💥 Deno内部回路でエラー発生: ${err.message}`);
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
    mission_log("INITIALIZE", f"=== 【ルートA】ログ強化型解読シーケンス始動 ===")
    
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
    mission_log("SUBPROCESS", "Deno 2.8.3 監視モニター付き解析ユニット、起動！")
    
    try:
        # 【重要】check=False にして、DenoがコケてもPython側でパニックを起こさず、stderrを全回収する！
        result = subprocess.run(
            ["deno", "run", "--allow-net", js_file, encrypted_signature, base_js_url],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Denoの標準エラー出力（内部ログやエラーの悲鳴）をすべてPythonのログに吐き出す！
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
            mission_log("DATA_CHANGE", f"Denoハック成功！ [関数: {deno_json['main_function']}] [オブジェクト: {deno_json['helper_object']}]")
            
            final_stream_url = f"{stream_pure_url}&{sp_param}={decrypted_sig}"
            mission_log("SUCCESS", f"本物対応ストリームURLの完全精製に成功！！！")
            
            return {
                "title": video_title,
                "url": final_stream_url,
                "status": "DECIPHERED_SUCCESS"
            }
        else:
            mission_log("ERROR", f"Denoの自動解読回路がエラーを応答。理由: {deno_json.get('reason') if deno_json else 'JSON出力なし'}")
            return None
            
    except Exception as e:
        mission_log("ERROR", f"Python側でのDeno執行エラー: {e}")
        return None
    finally:
        if os.path.exists(js_file):
            os.remove(js_file)

if __name__ == "__main__":
    # テスト対象動画：お好きなURLでテスト突撃！
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    stream_info = get_valid_stream(test_url)
    if stream_info:
        print("\\n=== [最終成果物] Flaskに渡せるデータ ===")
        print(json.dumps(stream_info, indent=2, ensure_ascii=False))

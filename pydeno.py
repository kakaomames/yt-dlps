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
    作戦1: Deno 2.8.3で動く「全関数シミュレーション・総当たりJS」を生成
    """
    js_code = """
    // Deno 2.8.3 専用：全関数実射シミュレーション・総当たりエンジン
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

        const candidates = [];
        let searchIdx = 0;

        // 【カカオマメ作戦】まずは .split( のある関数ブロックを全件ローラー収集！
        while (true) {
            const splitIdx = jsText.indexOf(".split(", searchIdx);
            if (splitIdx === -1) break;
            
            searchIdx = splitIdx + 7; // 次の探索へポインタを進める

            let funcStartIdx = -1;
            const lookbackStart = Math.max(0, splitIdx - 300);
            const snippetBefore = jsText.substring(lookbackStart, splitIdx);
            
            const lastFuncKeyword = snippetBefore.lastIndexOf("function");
            if (lastFuncKeyword !== -1) {
                funcStartIdx = lookbackStart + lastFuncKeyword;
            } else {
                const lastOpenBrace = snippetBefore.lastIndexOf("{");
                if (lastOpenBrace !== -1) {
                    funcStartIdx = lookbackStart + lastOpenBrace;
                }
            }

            if (funcStartIdx === -1) continue;

            const openBraceIdx = jsText.indexOf("{", funcStartIdx);
            if (openBraceIdx === -1 || openBraceIdx > splitIdx) continue;

            let braceCount = 0;
            let funcEndIdx = -1;
            for (let i = openBraceIdx; i < jsText.length; i++) {
                if (jsText[i] === "{") braceCount++;
                if (jsText[i] === "}") braceCount--;
                if (braceCount === 0) {
                    funcEndIdx = i;
                    break;
                }
            }

            if (funcEndIdx === -1) continue;

            const potentialFunc = jsText.substring(funcStartIdx, funcEndIdx + 1);
            
            // 重複を排除して容疑者リストに登録
            if (!candidates.includes(potentialFunc)) {
                candidates.push(potentialFunc);
            }
        }

        console.error(`[DENO_CORE] 🕵️‍♂️ 索敵完了：容疑者となる関数を ${candidates.length} 個捕捉！これより総当たり実射シミュレーションを開始する！`);

        let validResult = null;
        let winnerHelperName = "";
        let winnerIndex = -1;

        // 【実射ループ】すべての候補関数に、実際に暗号化シグネチャを流し込んでみる！
        for (let i = 0; i < candidates.length; i++) {
            try {
                const mainFuncCode = candidates[i];
                const firstBrace = mainFuncCode.indexOf("{");
                const lastBrace = mainFuncCode.lastIndexOf("}");
                const pureBody = mainFuncCode.substring(firstBrace + 1, lastBrace);

                // 引数名を動的に特定
                let argName = "a";
                const argMatch = mainFuncCode.match(/function\\s*\\(\\s*([a-zA-Z0-9$_]+)\\s*\\)/) || 
                                 mainFuncCode.match(/\\(\\s*([a-zA-Z0-9$_]+)\\s*\\)\\s*=>/) ||
                                 mainFuncCode.match(/([a-zA-Z0-9$_]+)\\s*=>/);
                if (argMatch && argMatch[1]) argName = argMatch[1];

                // ヘルパーオブジェクト名を特定
                const helperMatch = pureBody.match(/([a-zA-Z0-9$_]+)\\s*\\.\\s*([a-zA-Z0-9$_]+)\\s*\\(/);
                if (!helperMatch) {
                    console.error(`[DENO_SIM] ⏩ 候補 [${i + 1}/${candidates.length}]: ヘルパーオブジェクトを内部に持たないためスキップ。`);
                    continue;
                }
                const helperObjName = helperMatch[1];

                // ヘルパーオブジェクトの定義コードを base.js から抽出
                let objStartIdx = jsText.indexOf(helperObjName + "={");
                if (objStartIdx === -1) objStartIdx = jsText.indexOf(helperObjName + " = {");
                if (objStartIdx === -1) {
                    const regexSearch = new RegExp("(var|const|let)\\\\s+" + helperObjName + "\\\\s*=\\\\s*\\\\{");
                    const m = jsText.match(regexSearch);
                    if (m) objStartIdx = m.index + m[0].length - 1;
                } else {
                    objStartIdx = jsText.indexOf("{", objStartIdx);
                }

                if (objStartIdx === -1 || objStartIdx === undefined) {
                    console.error(`[DENO_SIM] ⏩ 候補 [${i + 1}/${candidates.length}]: オブジェクト [${helperObjName}] の定義体が見つからずスキップ。`);
                    continue;
                }

                let bCount = 0;
                let objEndIdx = -1;
                for (let j = objStartIdx; j < jsText.length; j++) {
                    if (jsText[j] === "{") bCount++;
                    if (jsText[j] === "}") bCount--;
                    if (bCount === 0) {
                        objEndIdx = j;
                        break;
                    }
                }
                if (objEndIdx === -1) continue;

                const helperDefCode = "var " + helperObjName + " = " + jsText.substring(objStartIdx, objEndIdx + 1) + ";";

                // テスト環境をダイナミック構築！
                const fullExecutionCode = `
                    ${helperDefCode}
                    function testDecipher(${argName}) {
                        ${pureBody}
                    }
                    return testDecipher("${encryptedSig}");
                `;

                // 実際にシグネチャをブチ込んで実行！！
                const executeDecipher = new Function(fullExecutionCode);
                const res = executeDecipher();

                // 【判定アルゴリズム】
                // 実行に成功し、かつ返り値が「元のシグネチャの長さに近く(通常100文字前後)」、かつ空でないこと！
                if (res && typeof res === "string" && res.length > 20 && res !== encryptedSig) {
                    console.error(`[DENO_SIM] 🟢 🟢 🟢 候補 [${i + 1}/${candidates.length}] が完全な復号出力を検知！！！ 長さ: ${res.length}`);
                    validResult = res;
                    winnerHelperName = helperObjName;
                    winnerIndex = i + 1;
                    break; // 本物が見つかったので総当たりループを突破！
                } else {
                    console.error(`[DENO_SIM] ⚠️ 候補 [${i + 1}/${candidates.length}]: 実行はできたが出力が不正のため除外。`);
                }

            } catch (e) {
                // ダミー関数などでエラーが出ても、システムはパニックを起こさず次の候補を試す！
                console.error(`[DENO_SIM] ❌ 候補 [${i + 1}/${candidates.length}]: 実行エラーのため除外 (${e.message})`);
            }
        }

        if (!validResult) {
            throw new Error("すべての候補関数にシグネチャを実射テストしましたが、有効な出力を返す本物の関数が存在しませんでした。");
        }

        const output = {
            status: "SUCCESS",
            main_function: `Simulated_Winner_No_${winnerIndex}`,
            helper_object: winnerHelperName,
            encrypted: encryptedSig,
            decrypted: validResult
        };
        console.log(JSON.stringify(output));

    } catch (err) {
        console.error(`[DENO_FATAL] 💥 総当たりシミュレーション中に致命的エラー: ${err.message}`);
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
    mission_log("INITIALIZE", f"=== 【ルートA】全関数実射シミュレーション・シーケンス始動 ===")
    
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
    mission_log("SUBPROCESS", "Deno 2.8.3 総当たりテスト実射モニター、起動！")
    
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
            mission_log("DATA_CHANGE", f"Denoハック大成功！ [選出された関数番号: {deno_json['main_function']}] [オブジェクト: {deno_json['helper_object']}]")
            
            final_stream_url = f"{stream_pure_url}&{sp_param}={decrypted_sig}"
            mission_log("SUCCESS", f"本物対応ストリームURLの完全精製に成功！！！")
            
            return {
                "title": video_title,
                "url": final_stream_url,
                "status": "DECIPHERED_SUCCESS"
            }
        else:
            mission_log("ERROR", f"Denoの総当たりスキャンがエラーを応答。理由: {deno_json.get('reason') if deno_json else 'JSON出力なし'}")
            return None
            
    except Exception as e:
        mission_log("ERROR", f"Python側でのDeno執行エラー: {e}")
        return None
    finally:
        if os.path.exists(js_file):
            os.remove(js_file)

if __name__ == "__main__":
    # リック・アストリーの鉄壁要塞URLで総当たり実射テスト！
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    stream_info = get_valid_stream(test_url)
    if stream_info:
        print("\\n=== [最終成果物] Flaskに渡せるデータ ===")
        print(json.dumps(stream_info, indent=2, ensure_ascii=False))

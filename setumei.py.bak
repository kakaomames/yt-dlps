import os
import re
import shutil

def inject_to_file(file_path):
    print(f"setumei.pyの関数inject_to_fileを実行しました。")
    print(f"setumei.pyの関数inject_to_fileを実行しました。")
    print(f"setumei.pyの関数inject_to_fileを実行しました。")
    print(f"setumei.pyの関数inject_to_fileを実行しました。")
    print(f"setumei.pyの関数inject_to_fileを実行しました。")
    print(f"setumei.pyの関数inject_to_fileを実行しました。")
    # バックアップ作成
    shutil.copy(file_path, file_path + ".bak")
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    modified = False
    new_lines = []
    
    # 正規表現: 行頭の空白と関数名を取得
    pattern = re.compile(r"^(\s*)def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\)\s*:")
    
    prev_line = ""
    for line in lines:
        match = pattern.match(line)
        
        # 挿入条件: 
        # 1. def行であること
        # 2. 直前の行がデコレータ(@)ではないこと
        if match and not prev_line.strip().startswith("@"):
            indent_str = match.group(1)
            func_name = match.group(2)
            file_name = os.path.basename(file_path).replace(".py", "")
            
            # インデント計算 (defのインデント + 4スペース)
            next_indent = indent_str + "    "
            # ログ用コード
            log_code = f'{next_indent}print(f"{file_name}.pyの関数{func_name}を実行しました。")\n'
            
            new_lines.append(line)
            # 二重挿入防止
            if log_code not in new_lines:
                new_lines.append(log_code)
                modified = True
        else:
            new_lines.append(line)
        
        # 直前の行を更新
        prev_line = line
                
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        return True
    return False

# カレントディレクトリ以下の全 .py を対象に実行
target_dir = "."
for root, dirs, files in os.walk(target_dir):
    for file in files:
        # バックアップファイルは除外
        if file.endswith(".py") and not file.endswith(".bak"):
            path = os.path.join(root, file)
            try:
                if inject_to_file(path):
                    print(f"✅ 注入完了: {path}")
            except Exception as e:
                print(f"❌ エラー発生: {path} - {e}")

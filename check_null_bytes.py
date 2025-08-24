import os
import sys


def scan_and_clean(root_dir=".", fix=False):
    found = False
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):  # 只处理 Python 文件
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, "rb") as f:
                        content = f.read()
                    if b"\x00" in content:
                        found = True
                        positions = [i for i, b in enumerate(content) if b == 0]
                        print(f"[!] Null byte found in {filepath}")
                        print(f"    Positions: {positions[:10]}{'...' if len(positions) > 10 else ''}")

                        if fix:
                            new_content = content.replace(b"\x00", b"")
                            backup_path = filepath + ".bak"

                            # 先备份原文件
                            with open(backup_path, "wb") as f:
                                f.write(content)

                            # 写入清理后的文件
                            with open(filepath, "wb") as f:
                                f.write(new_content)

                            print(f"[FIXED] Cleaned null bytes in {filepath}")
                            print(f"        Backup saved as {backup_path}")
                except Exception as e:
                    print(f"[ERROR] Could not process {filepath}: {e}")
    if not found:
        print("✅ No null bytes found in any .py file.")


if __name__ == "__main__":
    project_path = r"D:\workspace\python\stock-analysis-backend"
    fix_mode = "--fix" in sys.argv
    scan_and_clean(project_path, fix=fix_mode)

# 默认模式：只检查，不改动文件。
# 加上 --fix 参数：会清理 \x00 并生成 .bak 备份。
# 用法：
# 只检查（不会改动文件）：
# python check_null_bytes.py
# 检查并清理（会生成 .bak 备份并移除 \x00）：
# python check_null_bytes.py --fix

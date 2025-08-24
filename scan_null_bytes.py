import os

def scan_for_null_bytes(root_dir="."):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):  # 只扫描 Python 文件
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, "rb") as f:
                        content = f.read()
                        if b"\x00" in content:
                            positions = [i for i, b in enumerate(content) if b == 0]
                            print(f"[!] Null byte found in {filepath}")
                            print(f"    Positions: {positions[:10]}{'...' if len(positions) > 10 else ''}")
                except Exception as e:
                    print(f"[ERROR] Could not read {filepath}: {e}")

if __name__ == "__main__":
    scan_for_null_bytes("D:\\workspace\\python\\stock-analysis-backend")
# python scan_null_bytes.py

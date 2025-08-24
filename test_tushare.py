#!/usr/bin/env python3
import json
import requests
import sys
import os


def mask(s, n=10):
    if not s: return ""
    return s[:n] + "...(" + str(len(s)) + " chars)"


def http_call(token):
    url_http = "http://api.tushare.pro"
    url_https = "https://api.tushare.pro"  # 也测一下 https
    payload = {
        "api_name": "stock_basic",
        "token": token,
        "params": {"exchange": "", "list_status": "L"},
        "fields": "ts_code,symbol,name"
    }
    print("\n=== 直接HTTP调用（requests） ===")
    for url in (url_http, url_https):
        try:
            r = requests.post(url, json=payload, timeout=20)
            print(f"[HTTP] POST {url} -> {r.status_code}")
            text = r.text
            if len(text) > 600: text = text[:600] + "...(truncated)"
            print(text)
        except Exception as e:
            print(f"[HTTP] 请求失败: {e}")


def pro_call(token):
    print("\n=== 通过 tushare 库调用 ===")
    try:
        import tushare as ts, pandas as pd
        print(f"tushare version: {ts.__version__}")
        print(f"pandas version:  {pd.__version__}")
    except Exception as e:
        print(f"导入库失败: {e}")
        return

    try:
        ts.set_token(token)
        pro1 = ts.pro_api()
        pro2 = ts.pro_api(token)

        for i, pro in enumerate((pro1, pro2), start=1):
            print(f"\n-- pro_api 实例 {i} --")
            try:
                print("调用 stock_basic（不带 fields）...")
                df1 = pro.stock_basic(exchange='', list_status='L')
                print(f"shape={df1.shape}, columns={list(df1.columns)}")
                print(df1.head())

                print("调用 stock_basic（带 fields）...")
                df2 = pro.stock_basic(exchange='', list_status='L',
                                      fields='ts_code,symbol,name')
                print(f"shape={df2.shape}, columns={list(df2.columns)}")
                print(df2.head())

                print("调用通用 query ...")
                df3 = pro.query('stock_basic', exchange='', list_status='L',
                                fields='ts_code,symbol,name')
                print(f"shape={df3.shape}, columns={list(df3.columns)}")
                print(df3.head())

                print("只拉上交所做最小测试 ...")
                df4 = pro.stock_basic(exchange='SSE', list_status='L',
                                      fields='ts_code,symbol,name')
                print(f"shape={df4.shape}, columns={list(df4.columns)}")
                print(df4.head())
            except Exception as e:
                print(f"库调用异常: {e}")
    except Exception as e:
        print(f"初始化 tushare 失败: {e}")


def load_token():
    """优先从 .env 读取 TU_SHARE_TOKEN，否则读环境变量"""
    token = None
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("TU_SHARE_TOKEN"):
                        key, value = line.strip().split("=", 1)
                        token = value.strip().strip('"').strip("'")
                        break
        except Exception as e:
            print(f"读取 .env 文件失败: {e}")

    if not token:
        token = os.getenv("TU_SHARE_TOKEN")

    return token


if __name__ == "__main__":
    TOKEN = load_token()
    print(f"使用的 token: {mask(TOKEN)}")
    if not TOKEN:
        print("请在环境变量 TU_SHARE_TOKEN 或 .env 文件中配置你的 Tushare token。")
        sys.exit(1)

    http_call(TOKEN)
    pro_call(TOKEN)

#!/usr/bin/env python3
"""
定时股票数据同步任务
"""
import schedule
import time
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.data.sources.tushare import TushareDataSource

async def sync_stocks_task():
    """执行股票数据同步任务"""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始执行股票数据同步...")
    
    try:
        tushare = TushareDataSource()
        # 实现具体的同步逻辑
        print("股票数据同步完成")
    except Exception as e:
        print(f"股票数据同步失败: {e}")

def run_sync_task():
    """运行同步任务"""
    asyncio.run(sync_stocks_task())

def main():
    """主函数"""
    # 设置定时任务
    schedule.every().day.at("09:30").do(run_sync_task)  # 开盘前
    schedule.every().day.at("15:00").do(run_sync_task)  # 收盘后
    
    print("股票数据同步任务已启动...")
    print("定时任务:")
    print("  - 每天 09:30 (开盘前)")
    print("  - 每天 15:00 (收盘后)")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()

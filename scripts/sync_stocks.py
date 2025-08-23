#!/usr/bin/env python3
"""
股票数据同步脚本
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.data.sources.tushare import TushareDataSource

async def sync_stocks():
    """同步股票数据"""
    print("开始同步股票数据...")
    
    tushare = TushareDataSource()
    
    # 这里实现数据同步逻辑
    print("股票数据同步完成")

if __name__ == "__main__":
    asyncio.run(sync_stocks())

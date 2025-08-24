#!/usr/bin/env python3
"""
Tushare数据源使用示例（带 daily fallback）
"""

import asyncio
from pathlib import Path
from app.infrastructure.data.sources import TushareDataSource


async def example_tushare_usage():
    print("=" * 60)
    print("Tushare数据源使用示例（带 daily fallback）")
    print("=" * 60)

    # 创建 TushareDataSource 实例（token 从 .env 文件读取）
    ts_source = TushareDataSource()
    print("成功创建 TushareDataSource 实例")

    print("测试连接中...")
    result = await ts_source.test_connection()

    if result["success"]:
        print("✅ Tushare连接成功")
        if result.get("error_msg"):
            print("⚠️ 说明:", result["error_msg"])
        if result.get("sample_stock"):
            print("示例股票数据:")
            sample = result["sample_stock"]
            if "daily_records" in sample:
                print(
                    f"股票代码: {sample['ts_code']}, name: {sample['name']}, daily记录数: {len(sample['daily_records'])}")
                print("前5条 daily 数据:", sample['daily_records'][:5])
            else:
                print(sample)
    else:
        print("❌ Tushare连接失败")
        print("原因:", result.get("error_msg"))

    print("=" * 60)
    print("使用说明:")
    print("1. 确保在项目根目录下有 .env 文件，包含 TU_SHARE_TOKEN")
    print("2. 运行此脚本测试连接")
    print("3. 在代码中使用: ts_source = TushareDataSource()")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(example_tushare_usage())

#!/usr/bin/env python3
"""
测试数据源功能
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.infrastructure.data.sources import TushareDataSource, EastMoneyDataSource
from app.core.config import settings


async def test_eastmoney_source():
    """测试东方财富网数据源"""
    print("=" * 50)
    print("测试东方财富网数据源")
    print("=" * 50)

    try:
        # 创建数据源实例
        em_source = EastMoneyDataSource()

        # 测试连接
        print("1. 测试连接...")
        is_connected = await em_source.test_connection()
        print(f"   连接状态: {'成功' if is_connected else '失败'}")

        if is_connected:
            # 测试获取股票基本信息
            print("2. 测试获取股票基本信息...")
            stock_basic = await em_source.get_stock_basic('000001')
            if stock_basic:
                print(f"   获取到 {len(stock_basic)} 条股票基本信息")
                print(f"   示例: {stock_basic[0]}")
            else:
                print("   获取股票基本信息失败")

            # 测试获取实时行情
            print("3. 测试获取实时行情...")
            realtime_quote = await em_source.get_stock_realtime_quote('000001')
            if realtime_quote:
                print(f"   获取到 {len(realtime_quote)} 条实时行情")
                print(f"   示例: {realtime_quote[0]}")
            else:
                print("   获取实时行情失败")

    except Exception as e:
        print(f"   测试失败: {e}")


async def test_tushare_source():
    """测试Tushare数据源"""
    print("\n" + "=" * 50)
    print("测试Tushare数据源")
    print("=" * 50)

    try:
        # 检查是否有Tushare token
        token = getattr(settings, 'TU_SHARE_TOKEN', None)
        if not token:
            print("   未配置Tushare token，跳过测试")
            print("   请在.env文件中设置TU_SHARE_TOKEN")
            return

        # 创建数据源实例
        ts_source = TushareDataSource(token)

        # 测试连接
        print("1. 测试连接...")
        is_connected = await ts_source.test_connection()
        print(f"   连接状态: {'成功' if is_connected else '失败'}")

        if is_connected:
            # 测试获取股票基本信息
            print("2. 测试获取股票基本信息...")
            stock_basic = await ts_source.get_stock_basic(exchange='SSE', list_status='L')
            if stock_basic:
                print(f"   获取到 {len(stock_basic)} 条股票基本信息")
                print(f"   示例: {stock_basic[0]}")
            else:
                print("   获取股票基本信息失败")

            # 测试获取K线数据
            print("3. 测试获取K线数据...")
            kline_data = await ts_source.get_stock_kline('000001.SZ', period='daily')
            if kline_data:
                print(f"   获取到 {len(kline_data)} 条K线数据")
                print(f"   示例: {kline_data[0]}")
            else:
                print("   获取K线数据失败")

    except Exception as e:
        print(f"   测试失败: {e}")


async def main():
    """主测试函数"""
    print("开始测试数据源...")

    # 测试东方财富网数据源
    await test_eastmoney_source()

    # 测试Tushare数据源
    await test_tushare_source()

    print("\n测试完成!")


if __name__ == "__main__":
    asyncio.run(main())

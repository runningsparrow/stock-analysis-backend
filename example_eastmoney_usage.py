#!/usr/bin/env python3
"""
EastMoney 数据源使用示例（支持指定股票、K线周期和返回数量 limit）
"""

import asyncio
import pandas as pd
import argparse
from app.infrastructure.data.sources import EastMoneyDataSource

async def example_eastmoney_usage(
    symbol: str = None,
    kline_freq: str = 'daily',
    kline_limit: int = 30,
    list_limit: int = 10
):
    print("=" * 60)
    print("EastMoney数据源使用示例")
    print("=" * 60)

    try:
        em_source = EastMoneyDataSource()
        print("✅ 成功创建 EastMoneyDataSource 实例\n")

        # 测试连接
        conn_result = await em_source.test_connection()
        if conn_result.get("success"):
            print("✅ EastMoney连接成功！")
        else:
            print(f"❌ EastMoney连接失败: {conn_result.get('error_msg')}")

        # 获取单只股票信息
        target_symbol = symbol or '000001'
        print(f"\n获取单只股票信息（示例: {target_symbol}）:")
        single_stock = await em_source.get_stock_basic(target_symbol)
        if single_stock:
            print(pd.DataFrame(single_stock))
        else:
            print(f"⚠️ {target_symbol} 无股票基本信息")

        # 获取股票列表前 list_limit 条
        print(f"\n获取股票列表前 {list_limit} 条:")
        stock_list = await em_source.get_stock_basic()
        if stock_list:
            df_list = pd.DataFrame(stock_list[:list_limit])
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print(df_list)
        else:
            print("⚠️ 无股票列表数据")

        # 获取K线数据（带 limit）
        print(f"\n获取单只股票最近 {kline_limit} 条 {kline_freq} K线数据（{target_symbol}）:")
        kline_df = await em_source.get_stock_kline(target_symbol, freq=kline_freq, limit=kline_limit)
        if kline_df.empty:
            print(f"⚠️ {target_symbol} 无 {kline_freq} K 线数据")
        else:
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print(kline_df)

        # 获取财务数据
        print(f"\n获取单只股票最新财务指标（{target_symbol}）:")
        fin_data = await em_source.get_financial_data(target_symbol)
        if fin_data.get('indicator') is None or fin_data['indicator'].empty:
            print(f"⚠️ {target_symbol} 无财务数据")
            print('--- indicator ---\n无数据')
        else:
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 1000)
            print(fin_data['indicator'].head())

    except Exception as e:
        print(f"❌ 示例运行失败: {e}")

    print("=" * 60)
    print("使用说明:")
    print("1. 直接运行此脚本即可测试 EastMoney 数据源")
    print("2. 可以通过参数指定股票代码、K线周期、返回K线条数和股票列表条数，例如:")
    print("   python example_eastmoney_usage.py -s 600519 -f weekly --kline-limit 50 --list-limit 20")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EastMoney 数据源示例")
    parser.add_argument('-s', '--symbol', type=str, help='股票代码')
    parser.add_argument('-f', '--freq', type=str, default='daily', choices=['daily', 'weekly', 'monthly'], help='K线周期')
    parser.add_argument('--kline-limit', type=int, default=30, help='返回K线条数')
    parser.add_argument('--list-limit', type=int, default=10, help='股票列表显示条数')
    args = parser.parse_args()

    asyncio.run(example_eastmoney_usage(args.symbol, args.freq, args.kline_limit, args.list_limit))

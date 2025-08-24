#!/usr/bin/env python3
"""
EastMoney 数据源（整合版，支持自定义 K 线数量 limit）
"""

import akshare as ak
import pandas as pd
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class EastMoneyDataSource:
    def __init__(self):
        pass

    async def get_stock_basic(self, symbol: str = None) -> Optional[List[Dict[str, Any]]]:
        try:
            result = []
            if symbol:
                stock_info = await self._fetch_single_stock(symbol)
                if stock_info:
                    result.extend(stock_info)
            else:
                all_stocks = await self._fetch_all_stocks()
                result.extend(all_stocks)
            return result
        except Exception as e:
            logger.error(f"东方财富网获取股票基本信息失败: {e}")
            return []

    async def _fetch_single_stock(self, symbol: str) -> List[Dict[str, Any]]:
        try:
            stock_info = ak.stock_individual_info_em(symbol)
            if not stock_info.empty:
                data = stock_info.to_dict('records')[0]
                return [{
                    'symbol': symbol,
                    'name': data.get('股票简称', ''),
                    'exchange': self._get_exchange_by_symbol(symbol),
                    'industry': data.get('所属行业', ''),
                    'market_type': data.get('市场类型', ''),
                    'listing_date': data.get('上市日期', ''),
                    'total_shares': self._parse_number(data.get('总股本', '')),
                    'circulating_shares': self._parse_number(data.get('流通股本', '')),
                    'pe_ratio': self._parse_number(data.get('市盈率', '')),
                    'pb_ratio': self._parse_number(data.get('市净率', '')),
                    'market_cap': self._parse_number(data.get('总市值', '')),
                    'circulating_market_cap': self._parse_number(data.get('流通市值', ''))
                }]
        except Exception as e:
            logger.warning(f"获取单只股票 {symbol} 信息失败: {e}")
        return []

    async def _fetch_all_stocks(self) -> List[Dict[str, Any]]:
        try:
            stock_list = ak.stock_info_a_code_name()
            if not stock_list.empty:
                result = []
                for _, row in stock_list.iterrows():
                    result.append({
                        'symbol': row['code'],
                        'name': row['name'],
                        'exchange': self._get_exchange_by_symbol(row['code']),
                        'industry': '',
                        'market_type': '',
                        'listing_date': '',
                        'total_shares': 0,
                        'circulating_shares': 0,
                        'pe_ratio': 0,
                        'pb_ratio': 0,
                        'market_cap': 0,
                        'circulating_market_cap': 0
                    })
                return result
        except Exception as e:
            logger.error(f"获取全部A股列表失败: {e}")
        return []

    async def get_stock_realtime_quote(self, symbol: str = None) -> Optional[List[Dict[str, Any]]]:
        try:
            price_info = ak.stock_zh_a_spot_em()
            if not price_info.empty:
                result = []
                for _, row in price_info.iterrows():
                    stock_data = {
                        'symbol': row['代码'],
                        'name': row['名称'],
                        'current_price': self._parse_number(row['最新价']),
                        'change_amount': self._parse_number(row['涨跌额']),
                        'change_percent': self._parse_number(row['涨跌幅']),
                        'open_price': self._parse_number(row['开盘']),
                        'high_price': self._parse_number(row['最高']),
                        'low_price': self._parse_number(row['最低']),
                        'prev_close': self._parse_number(row['昨收']),
                        'volume': self._parse_number(row['成交量']),
                        'amount': self._parse_number(row['成交额']),
                        'turnover_rate': self._parse_number(row['换手率']),
                        'pe_ratio': self._parse_number(row['市盈率']),
                        'pb_ratio': self._parse_number(row['市净率']),
                        'market_cap': self._parse_number(row['总市值']),
                        'circulating_market_cap': self._parse_number(row['流通市值']),
                        'quote_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    if symbol and row['代码'] == symbol:
                        return [stock_data]
                    result.append(stock_data)
                return result
            return []
        except Exception as e:
            logger.error(f"东方财富网获取实时行情失败: {e}")
            return []

    # ===== 新增 limit 参数 =====
    async def get_stock_kline(self, symbol: str, freq: str = 'daily', limit: int = 30) -> pd.DataFrame:
        """
        获取单只股票 K 线数据
        :param symbol: 股票代码
        :param freq: 'daily', 'weekly', 'monthly'
        :param limit: 返回条数
        :return: DataFrame
        """
        try:
            # === Step 1: 获取日线数据（东财源）
            df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date="19700101", adjust="")

            if df.empty:
                logger.warning(f"{symbol} 日线接口返回空表")
                return pd.DataFrame()

            # === Step 2: 列名统一
            rename_map = {
                '日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high',
                '最低': 'low', '成交量': 'volume', '成交额': 'amount'
            }
            df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

            if 'date' not in df.columns:
                logger.error(f"{symbol} 返回的K线数据缺少日期列")
                return pd.DataFrame()

            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date']).sort_values('date')

            # === Step 3: 周/月份重采样
            if freq in ['weekly', 'monthly']:
                df = df.set_index('date')
                agg_dict = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}
                if 'amount' in df.columns:
                    agg_dict['amount'] = 'sum'
                if freq == 'weekly':
                    df = df.resample('W-MON').agg(agg_dict)
                else:
                    df = df.resample('M').agg(agg_dict)
                df = df.reset_index()

            # === Step 4: 返回最近 limit 条
            df = df.dropna().tail(limit).reset_index(drop=True)

            return df

        except Exception:
            logger.exception(f"获取K线数据失败 {symbol}")
            return pd.DataFrame()

    async def get_financial_data(self, symbol: str) -> Dict[str, pd.DataFrame]:
        try:
            loop = asyncio.get_event_loop()
            indicator = await loop.run_in_executor(None, ak.stock_financial_report_sina, symbol)
            if indicator.empty:
                logger.warning(f"{symbol} 没有财务指标数据")
                indicator = pd.DataFrame()
            return {'indicator': indicator}
        except Exception as e:
            logger.error(f"获取财务数据失败 {symbol}: {e}")
            return {}

    async def test_connection(self) -> dict:
        try:
            result = await self.get_stock_basic('000001')
            if result and len(result) > 0:
                return {'success': True, 'error_msg': ''}
            else:
                return {'success': False, 'error_msg': '返回空数据，可能接口不可用或股票代码错误'}
        except Exception as e:
            return {'success': False, 'error_msg': str(e)}

    def _get_exchange_by_symbol(self, symbol: str) -> str:
        if symbol.startswith('6'):
            return 'SSE'
        elif symbol.startswith(('0', '3')):
            return 'SZSE'
        else:
            return 'UNKNOWN'

    def _parse_number(self, value) -> float:
        if pd.isna(value) or value in ['', '-']:
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            value = value.replace(',', '')
            try:
                if '万' in value:
                    return float(value.replace('万', '')) * 1e4
                if '亿' in value:
                    return float(value.replace('亿', '')) * 1e8
                return float(value)
            except ValueError:
                return 0.0
        return 0.0

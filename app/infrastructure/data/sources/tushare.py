import os
import tushare as ts
import pandas as pd
from typing import Dict, Any, Optional, List
import asyncio
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class TushareDataSource:
    """Tushare数据源适配器"""

    def __init__(self, token: Optional[str] = None):
        """
        初始化Tushare数据源

        Args:
            token: Tushare API token，可选。如果不传则自动从 .env 或环境变量读取 TU_SHARE_TOKEN
        """
        if not token:
            load_dotenv()
            token = os.getenv("TU_SHARE_TOKEN")

        if not token:
            raise RuntimeError("未找到 TU_SHARE_TOKEN，请在 .env 文件中配置")

        self.token = token
        ts.set_token(token)
        self.pro = ts.pro_api()

    async def get_stock_basic(self, exchange: str = None, list_status: str = 'L') -> Optional[List[Dict[str, Any]]]:
        """获取股票基本信息"""
        try:
            df = self.pro.stock_basic(
                exchange=exchange,
                list_status=list_status,
                fields='ts_code,symbol,name,area,industry,market,list_date,delist_date,is_hs'
            )
            return df.to_dict('records') if df is not None and not df.empty else []
        except Exception as e:
            logger.error(f"Tushare获取股票基本信息失败: {e}")
            return []

    async def get_stock_quote(self, ts_code: str, trade_date: str = None) -> Optional[Dict[str, Any]]:
        """获取股票行情数据"""
        try:
            if trade_date is None:
                trade_date = self._get_latest_trade_date()

            df = self.pro.daily(
                ts_code=ts_code,
                trade_date=trade_date,
                fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
            )
            return df.to_dict('records')[0] if df is not None and not df.empty else None
        except Exception as e:
            logger.error(f"Tushare获取股票行情失败: {e}")
            return None

    async def get_stock_realtime_quote(self, ts_code: str) -> Optional[Dict[str, Any]]:
        """获取股票实时行情（当日）"""
        try:
            df = ts.get_realtime_quotes(ts_code)
            if df is not None and not df.empty:
                data = df.to_dict('records')[0]
                return {
                    'ts_code': data.get('code'),
                    'name': data.get('name'),
                    'price': float(data.get('price', 0)),
                    'bid': float(data.get('bid', 0)),
                    'ask': float(data.get('ask', 0)),
                    'volume': int(data.get('volume', 0)),
                    'amount': float(data.get('amount', 0)),
                    'date': data.get('date'),
                    'time': data.get('time'),
                    'open': float(data.get('open', 0)),
                    'high': float(data.get('high', 0)),
                    'low': float(data.get('low', 0)),
                    'pre_close': float(data.get('pre_close', 0)),
                }
            return None
        except Exception as e:
            logger.error(f"Tushare获取实时行情失败: {e}")
            return None

    async def get_stock_kline(self, ts_code: str, period: str = 'daily',
                              start_date: str = None, end_date: str = None) -> Optional[List[Dict[str, Any]]]:
        """获取股票K线数据"""
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            if end_date is None:
                end_date = datetime.now().strftime('%Y%m%d')

            if period == 'daily':
                df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            elif period == 'weekly':
                df = self.pro.weekly(ts_code=ts_code, start_date=start_date, end_date=end_date)
            elif period == 'monthly':
                df = self.pro.monthly(ts_code=ts_code, start_date=start_date, end_date=end_date)
            else:
                logger.error(f"不支持的周期: {period}")
                return []

            return df.to_dict('records') if df is not None and not df.empty else []
        except Exception as e:
            logger.error(f"Tushare获取K线数据失败: {e}")
            return []

    async def get_stock_financial(self, ts_code: str, period: str = '20231231') -> Optional[List[Dict[str, Any]]]:
        """获取股票财务指标"""
        try:
            df = self.pro.income(ts_code=ts_code, period=period)
            return df.to_dict('records') if df is not None and not df.empty else []
        except Exception as e:
            logger.error(f"Tushare获取财务数据失败: {e}")
            return []

    def _get_latest_trade_date(self) -> str:
        """获取最新交易日期"""
        try:
            df = self.pro.trade_cal(exchange='SSE',
                                    start_date='20240101',
                                    end_date=datetime.now().strftime('%Y%m%d'))
            if df is not None and not df.empty:
                return df[df['is_open'] == 1]['cal_date'].iloc[-1]
        except Exception as e:
            logger.error(f"获取最新交易日期失败: {e}")
        return (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

    async def test_connection(self) -> dict:
        """测试Tushare连接，返回详细信息及一条示例股票数据（含 daily fallback）"""
        sample_stock = None
        try:
            # 尝试 stock_basic
            df = self.pro.stock_basic(exchange='SSE', list_status='L', limit=1)
            if df is not None and not df.empty:
                sample_stock = df.to_dict('records')[0]
                return {"success": True, "error_msg": "", "sample_stock": sample_stock}
        except Exception as e:
            error_basic = str(e)

        # stock_basic失败，尝试 daily 接口
        try:
            # 使用一只示例股票代码（上交所前10只股票之一）
            ts_code = "600000.SH"
            df_daily = self.pro.daily(ts_code=ts_code, start_date="20240101", end_date="20240131")
            if df_daily is not None and not df_daily.empty:
                sample_stock = {
                    "ts_code": ts_code,
                    "name": "示例股票(来自 daily)",
                    "daily_records": df_daily.to_dict('records')
                }
                return {"success": True, "error_msg": "stock_basic失败，已使用 daily fallback",
                        "sample_stock": sample_stock}
        except Exception as e2:
            return {"success": False, "error_msg": f"stock_basic失败: {error_basic}; daily fallback也失败: {e2}",
                    "sample_stock": None}

        # 两个接口都没有返回数据
        return {"success": False, "error_msg": "stock_basic与daily接口均未返回有效数据", "sample_stock": None}



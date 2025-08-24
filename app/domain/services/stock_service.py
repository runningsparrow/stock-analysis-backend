from typing import List, Optional

from app.core.exceptions import DataSourceException
from app.infrastructure.data.sources.eastmoney import EastMoneyDataSource
from app.domain.models.schemas.stock import StockResponse, StockKLineOut


class StockService:
    def __init__(self):
        self.data_source = EastMoneyDataSource()

    # ------------ 股票列表 ------------
    async def get_stocks(self, limit: int = 100, offset: int = 0) -> List[dict]:
        """通过东财获取股票列表并分页"""
        all_stocks = await self.data_source.get_stock_basic()
        return all_stocks[offset : offset + limit]

    # ------------ 单票基础信息 ------------
    async def get_stock(self, symbol: str) -> Optional[dict]:
        """通过东财获取单只股票基础信息"""
        stock = await self.data_source.get_stock_basic(symbol)
        return stock[0] if stock else None

    # ------------ K 线 ------------
    async def get_kline(
        self,
        symbol: str,
        freq: str = "daily",
        limit: int = 30
    ) -> List[dict]:
        """
        获取东财 K 线数据，若空则抛出 503
        """
        df = await self.data_source.get_stock_kline(symbol, freq, limit)

        if df.empty:
            raise DataSourceException("东财接口暂时不可用", status_code=503)

        # 统一列名
        df = df.rename(
            columns={
                "日期": "date",
                "开盘": "open",
                "收盘": "close",
                "最高": "high",
                "最低": "low",
                "成交量": "volume",
                "成交额": "amount",
            }
        )

        # 可读化字段
        df["volume_str"] = (df["volume"] / 1e4).round(2).astype(str) + " 万手"
        df["amount_str"] = (df["amount"] / 1e8).round(2).astype(str) + " 亿"

        # 只保留需要的列
        keep = ["date", "open", "high", "low", "close", "volume_str", "amount_str"]
        return df[keep].to_dict("records")

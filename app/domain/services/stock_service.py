from typing import List, Optional
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
    async def get_kline(self, symbol: str, freq: str = "daily", limit: int = 30) -> List[dict]:
        """通过东财获取 K 线并转 dict"""
        df = await self.data_source.get_stock_kline(symbol, freq, limit)
        return df.to_dict("records")
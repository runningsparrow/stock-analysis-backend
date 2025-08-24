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
        """
        返回字段与 StockKLineOut 完全一致
        """
        df = await self.data_source.get_stock_kline(symbol, freq, limit)
        if df.empty:
            return []

        # 1. 统一英文列
        col_map = {
            "日期": "date",
            "开盘": "open",
            "收盘": "close",
            "最高": "high",
            "最低": "low",
            "成交量": "volume",
            "成交额": "amount",
        }
        df = df.rename(columns=col_map)

        # 2. 生成可读化字段
        df["volume_str"] = (df["volume"] / 1e4).round(2).astype(str) + " 万手"
        df["amount_str"] = (df["amount"] / 1e8).round(2).astype(str) + " 亿"

        # 3. 只保留接口需要字段
        keep = ["date", "open", "high", "low", "close", "volume_str", "amount_str"]
        return df[keep].to_dict("records")
    
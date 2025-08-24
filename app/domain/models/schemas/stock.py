from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class StockBase(BaseModel):
    symbol: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    exchange: str = Field(..., description="交易所")


class StockResponse(StockBase):
    id: Optional[int] = Field(None, description="数据库ID（可选）")
    current_price: Optional[float] = Field(None, description="当前价格")
    change_percent: Optional[float] = Field(None, description="涨跌幅")
    volume: Optional[int] = Field(None, description="成交量")
    market_cap: Optional[float] = Field(None, description="市值")
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="更新时间（默认当前 UTC）"
    )

    class Config:
        from_attributes = True


class StockListResponse(BaseModel):
    stocks: list[StockResponse]
    total: int
    page: int
    size: int


class StockKLineOut(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume_str: str
    amount_str: str
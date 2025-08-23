from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StockBase(BaseModel):
    symbol: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    exchange: str = Field(..., description="交易所")

class StockResponse(StockBase):
    id: int = Field(..., description="股票ID")
    current_price: Optional[float] = Field(None, description="当前价格")
    change_percent: Optional[float] = Field(None, description="涨跌幅")
    volume: Optional[int] = Field(None, description="成交量")
    market_cap: Optional[float] = Field(None, description="市值")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True

class StockListResponse(BaseModel):
    stocks: list[StockResponse]
    total: int
    page: int
    size: int

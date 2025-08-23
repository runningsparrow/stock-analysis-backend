from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.domain.models.schemas.stock import StockResponse, StockListResponse
from app.domain.services.stock_service import StockService
from app.infrastructure.data.sources.tushare import TushareDataSource

router = APIRouter()

@router.get("/stocks", response_model=List[StockResponse])
async def get_stocks(
    limit: int = 100,
    offset: int = 0,
    stock_service: StockService = Depends()
):
    """获取股票列表"""
    try:
        stocks = await stock_service.get_stocks(limit=limit, offset=offset)
        return stocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票列表失败: {str(e)}")

@router.get("/stocks/{symbol}", response_model=StockResponse)
async def get_stock(
    symbol: str,
    stock_service: StockService = Depends()
):
    """获取单个股票信息"""
    try:
        stock = await stock_service.get_stock(symbol)
        if not stock:
            raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")
        return stock
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票信息失败: {str(e)}")

@router.get("/stocks/{symbol}/price")
async def get_stock_price(symbol: str):
    """获取股票实时价格"""
    try:
        # 这里可以集成实时数据源
        return {"symbol": symbol, "price": "实时价格数据"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票价格失败: {str(e)}")

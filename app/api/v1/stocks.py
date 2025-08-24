from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from app.domain.models.schemas.stock import StockResponse, StockKLineOut
from app.domain.services.stock_service import StockService

router = APIRouter(prefix="/stocks", tags=["Stocks"])


# ------------ 列表 ------------
@router.get("", response_model=List[StockResponse])
async def list_stocks(
        limit: int = Query(100, ge=1, le=1000),
        offset: int = Query(0, ge=0),
        service: StockService = Depends()
):
    try:
        stocks = await service.get_stocks(limit=limit, offset=offset)
        return stocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------ 单票基础信息 ------------
@router.get("/{symbol}", response_model=StockResponse)
async def get_stock(
        symbol: str,
        service: StockService = Depends()
):
    stock = await service.get_stock(symbol)
    if not stock:
        raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")
    return stock


# ------------ K 线 ------------
@router.get("/{symbol}/kline", response_model=List[StockKLineOut])
async def get_kline(
        symbol: str,
        freq: str = Query("daily", regex="^(daily|weekly|monthly)$"),
        limit: int = Query(30, ge=1, le=1000),
        service: StockService = Depends()
):
    try:
        return await service.get_kline(symbol, freq, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

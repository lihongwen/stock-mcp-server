"""AKShare data service with retry logic and caching."""

import time
from datetime import datetime
from decimal import Decimal
from typing import Any

import akshare as ak
import pandas as pd
from loguru import logger

from stock_mcp_server.models.market import MarketIndex, MarketBreadth, CapitalFlow
from stock_mcp_server.services.cache_service import get_cache
from stock_mcp_server.utils.date_utils import get_latest_trading_date, is_trading_time


class AKShareService:
    """Service for fetching data from AKShare."""

    def __init__(self) -> None:
        """Initialize AKShare service."""
        self.cache = get_cache()
        self.retry_count = 3
        self.retry_delay = 1.0
        logger.info("AKShare service initialized")

    def _retry_fetch(self, func: Any, *args: Any, **kwargs: Any) -> Any:
        """Retry fetching data with exponential backoff."""
        for attempt in range(self.retry_count):
            try:
                time.sleep(0.5)  # Rate limiting
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                if attempt == self.retry_count - 1:
                    logger.error(f"Failed after {self.retry_count} attempts: {e}")
                    raise
                logger.warning(f"Attempt {attempt + 1} failed: {e}, retrying...")
                time.sleep(self.retry_delay * (2**attempt))
        return None

    def get_index_spot(self, index_code: str = "000001") -> MarketIndex | None:
        """
        Get real-time index data.
        
        Args:
            index_code: Index code (default: 000001 for Shanghai Composite)
            
        Returns:
            MarketIndex model or None if failed
        """
        # Check cache first
        cached = self.cache.get("market_data", index_code=index_code)
        if cached:
            return cached

        try:
            # Fetch from AKShare
            df = self._retry_fetch(ak.stock_zh_index_spot_em)
            if df is None or df.empty:
                return None

            # Find the specific index
            row = df[df["代码"] == index_code]
            if row.empty:
                logger.warning(f"Index {index_code} not found")
                return None

            row = row.iloc[0]

            # Map to MarketIndex model
            index_data = MarketIndex(
                code=index_code,
                name=str(row["名称"]),
                current=Decimal(str(row["最新价"])),
                open=Decimal(str(row["今开"])),
                high=Decimal(str(row["最高"])),
                low=Decimal(str(row["最低"])),
                close=Decimal(str(row["最新价"])) if not is_trading_time() else None,
                pre_close=Decimal(str(row["昨收"])),
                change=Decimal(str(row["涨跌额"])),
                change_pct=Decimal(str(row["涨跌幅"])),
                amplitude=Decimal(str(row.get("振幅", 0))),
                volume=int(row.get("成交量", 0)),
                amount=Decimal(str(row.get("成交额", 0))),
                turnover_rate=Decimal(str(row.get("换手率", 0))) if "换手率" in row else None,
                timestamp=datetime.now(),
                trading_date=get_latest_trading_date(),
                market_status="open" if is_trading_time() else "closed",
            )

            # Cache the result
            self.cache.set("market_data", index_data, index_code=index_code)
            logger.info(f"Fetched index data: {index_code}")
            return index_data

        except Exception as e:
            logger.error(f"Error fetching index data: {e}")
            return None

    def get_market_breadth(self, date: str | None = None) -> MarketBreadth | None:
        """
        Get market breadth statistics.
        
        Args:
            date: Trading date (YYYY-MM-DD) or None for latest
            
        Returns:
            MarketBreadth model or None if failed
        """
        if date is None:
            date = get_latest_trading_date()

        # Check cache
        cached = self.cache.get("market_data", type="breadth", date=date)
        if cached:
            return cached

        try:
            # Fetch all A-share stocks
            df = self._retry_fetch(ak.stock_zh_a_spot_em)
            if df is None or df.empty:
                return None

            total = len(df)
            advancing = len(df[df["涨跌幅"] > 0])
            declining = len(df[df["涨跌幅"] < 0])
            unchanged = len(df[df["涨跌幅"] == 0])
            limit_up = len(df[df["涨跌幅"] >= 9.9])
            limit_down = len(df[df["涨跌幅"] <= -9.9])
            gain_over_5pct = len(df[df["涨跌幅"] > 5])
            loss_over_5pct = len(df[df["涨跌幅"] < -5])
            gain_over_7pct = len(df[df["涨跌幅"] > 7])
            loss_over_7pct = len(df[df["涨跌幅"] < -7])

            breadth = MarketBreadth(
                total_stocks=total,
                advancing=advancing,
                declining=declining,
                unchanged=unchanged,
                limit_up=limit_up,
                limit_down=limit_down,
                gain_over_5pct=gain_over_5pct,
                loss_over_5pct=loss_over_5pct,
                gain_over_7pct=gain_over_7pct,
                loss_over_7pct=loss_over_7pct,
                advance_decline_ratio=Decimal(str(advancing / max(declining, 1))),
                advance_pct=Decimal(str(advancing / total * 100)),
                decline_pct=Decimal(str(declining / total * 100)),
                date=date,
                timestamp=datetime.now(),
            )

            self.cache.set("market_data", breadth, type="breadth", date=date)
            logger.info(f"Fetched market breadth for {date}")
            return breadth

        except Exception as e:
            logger.error(f"Error fetching market breadth: {e}")
            return None

    def get_capital_flow(self, date: str | None = None) -> CapitalFlow | None:
        """
        Get capital flow data.
        
        Args:
            date: Trading date or None for latest
            
        Returns:
            CapitalFlow model or None if failed
        """
        if date is None:
            date = get_latest_trading_date()

        # Check cache
        cached = self.cache.get("market_data", type="capital_flow", date=date)
        if cached:
            return cached

        try:
            # Fetch northbound capital flow
            df = self._retry_fetch(ak.stock_hsgt_fund_flow_summary_em)
            if df is None or df.empty:
                return None

            latest = df.iloc[-1]

            flow = CapitalFlow(
                north_net=Decimal(str(latest.get("北向资金", 0))),
                north_inflow=Decimal(str(abs(latest.get("北向资金", 0)))) if latest.get("北向资金", 0) > 0 else Decimal("0"),
                north_outflow=Decimal(str(abs(latest.get("北向资金", 0)))) if latest.get("北向资金", 0) < 0 else Decimal("0"),
                date=date,
                timestamp=datetime.now(),
            )

            self.cache.set("market_data", flow, type="capital_flow", date=date)
            logger.info(f"Fetched capital flow for {date}")
            return flow

        except Exception as e:
            logger.error(f"Error fetching capital flow: {e}")
            return None


# Global instance
_akshare_service: AKShareService | None = None


def get_akshare_service() -> AKShareService:
    """Get global AKShare service instance."""
    global _akshare_service
    if _akshare_service is None:
        _akshare_service = AKShareService()
    return _akshare_service

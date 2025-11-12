"""E*TRADE Market API client"""
import json
from typing import Dict, Any, List, Optional


class MarketClient:
    """Client for E*TRADE Market API"""
    
    def __init__(self, session, base_url: str):
        """
        Initialize Market API client
        
        Args:
            session: Authenticated OAuth session
            base_url: Base URL for API requests
        """
        self.session = session
        self.base_url = base_url
    
    def get_quote(self, symbols: str, require_earnings_date: bool = False, 
                  skip_mini_options_check: bool = False) -> Dict[str, Any]:
        """
        Get quote for one or more symbols
        
        Args:
            symbols: Comma-separated list of symbols (e.g., "AAPL,MSFT,GOOGL")
            require_earnings_date: If true, return next earnings date
            skip_mini_options_check: If true, skip check for mini options
            
        Returns:
            Quote response data
        """
        url = f"{self.base_url}/v1/market/quote/{symbols}.json"
        
        params = {}
        if require_earnings_date:
            params["requireEarningsDate"] = "true"
        if skip_mini_options_check:
            params["skipMiniOptionsCheck"] = "true"
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def look_up_product(self, search: str, company: Optional[str] = None,
                       type: Optional[str] = None) -> Dict[str, Any]:
        """
        Look up products (stocks, options, mutual funds)
        
        Args:
            search: Full or partial symbol name
            company: Full or partial company name
            type: Security type (e.g., EQ for equity, MF for mutual fund, OPTN for option)
            
        Returns:
            Product lookup response data
        """
        url = f"{self.base_url}/v1/market/lookup/{search}.json"
        
        params = {}
        if company:
            params["company"] = company
        if type:
            params["type"] = type
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_option_chains(self, symbol: str, expiry_year: Optional[int] = None,
                         expiry_month: Optional[int] = None, expiry_day: Optional[int] = None,
                         strike_price_near: Optional[float] = None, no_of_strikes: Optional[int] = None,
                         include_weekly: bool = False, skip_adjusted: bool = False,
                         option_category: Optional[str] = None, chain_type: Optional[str] = None,
                         price_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get option chains for a symbol
        
        Args:
            symbol: Underlying symbol
            expiry_year: Expiration year (4-digit)
            expiry_month: Expiration month (1-12)
            expiry_day: Expiration day (1-31)
            strike_price_near: Strike price near value
            no_of_strikes: Number of strikes
            include_weekly: Include weekly options
            skip_adjusted: Skip adjusted options
            option_category: Option category (STANDARD, ALL, MINI)
            chain_type: Chain type (CALL, PUT, CALLPUT)
            price_type: Price type (ATNM, ALL)
            
        Returns:
            Option chains response data
        """
        url = f"{self.base_url}/v1/market/optionchains.json"
        
        params = {"symbol": symbol}
        
        if expiry_year:
            params["expiryYear"] = expiry_year
        if expiry_month:
            params["expiryMonth"] = expiry_month
        if expiry_day:
            params["expiryDay"] = expiry_day
        if strike_price_near:
            params["strikePriceNear"] = strike_price_near
        if no_of_strikes:
            params["noOfStrikes"] = no_of_strikes
        if include_weekly:
            params["includeWeekly"] = "true"
        if skip_adjusted:
            params["skipAdjusted"] = "true"
        if option_category:
            params["optionCategory"] = option_category
        if chain_type:
            params["chainType"] = chain_type
        if price_type:
            params["priceType"] = price_type
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_option_expire_dates(self, symbol: str, expiry_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get option expiration dates for a symbol
        
        Args:
            symbol: Underlying symbol
            expiry_type: Expiry type (WEEKLY, MONTHLY, QUARTERLY, ALL)
            
        Returns:
            Expiration dates response data
        """
        url = f"{self.base_url}/v1/market/optionexpiredate.json"
        
        params = {"symbol": symbol}
        if expiry_type:
            params["expiryType"] = expiry_type
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        return response.json()

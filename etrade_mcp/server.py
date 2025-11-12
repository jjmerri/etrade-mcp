"""E*TRADE MCP Server using FastMCP"""
import os
from typing import Optional
from fastmcp import FastMCP
from dotenv import load_dotenv

from etrade_mcp.auth import ETradeAuth
from etrade_mcp.market import MarketClient

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("E*TRADE Market API")

# Global auth and market client instances
_auth: Optional[ETradeAuth] = None
_market_client: Optional[MarketClient] = None
_request_token: Optional[str] = None
_request_token_secret: Optional[str] = None


def get_auth() -> ETradeAuth:
    """Get or create auth instance"""
    global _auth
    if _auth is None:
        consumer_key = os.getenv("ETRADE_CONSUMER_KEY")
        consumer_secret = os.getenv("ETRADE_CONSUMER_SECRET")
        environment = os.getenv("ETRADE_ENVIRONMENT", "sandbox")
        
        if not consumer_key or not consumer_secret:
            raise ValueError(
                "ETRADE_CONSUMER_KEY and ETRADE_CONSUMER_SECRET must be set in environment variables"
            )
        
        _auth = ETradeAuth(consumer_key, consumer_secret, environment)
    return _auth


def get_market_client() -> MarketClient:
    """Get market client (requires authentication)"""
    global _market_client
    if _market_client is None:
        raise ValueError(
            "Not authenticated. Please call etrade_authenticate first."
        )
    return _market_client


@mcp.tool()
def etrade_get_auth_url() -> str:
    """
    Get E*TRADE OAuth authorization URL.
    This is the first step in authentication - returns a URL for the user to visit.
    
    Returns:
        Authorization URL that the user should visit in their browser
    """
    global _request_token, _request_token_secret
    
    auth = get_auth()
    _request_token, _request_token_secret = auth.get_request_token()
    authorize_url = auth.get_authorize_url(_request_token)
    
    return f"Please visit this URL and authorize the application:\n{authorize_url}\n\nAfter authorizing, you will receive a verification code. Use etrade_authenticate with that code."


@mcp.tool()
def etrade_authenticate(verifier: str) -> str:
    """
    Complete E*TRADE OAuth authentication with verification code.
    
    Args:
        verifier: The verification code received after authorizing the application
        
    Returns:
        Success message
    """
    global _market_client, _request_token, _request_token_secret
    
    if not _request_token or not _request_token_secret:
        raise ValueError(
            "No request token found. Please call etrade_get_auth_url first."
        )
    
    auth = get_auth()
    session = auth.get_session(_request_token, _request_token_secret, verifier)
    _market_client = MarketClient(session, auth.base_url)
    
    return f"Successfully authenticated! Using {auth.environment} environment at {auth.base_url}"


@mcp.tool()
def etrade_get_quote(symbols: str, require_earnings_date: bool = False,
                     skip_mini_options_check: bool = False) -> dict:
    """
    Get stock quote for one or more symbols.
    
    Args:
        symbols: Comma-separated list of stock symbols (e.g., "AAPL", "MSFT,GOOGL")
        require_earnings_date: If true, return next earnings date
        skip_mini_options_check: If true, skip check for mini options
        
    Returns:
        Quote data including price, volume, bid/ask, and other market information
    """
    client = get_market_client()
    return client.get_quote(symbols, require_earnings_date, skip_mini_options_check)


@mcp.tool()
def etrade_lookup_product(search: str, company: Optional[str] = None,
                          type: Optional[str] = None) -> dict:
    """
    Look up products by symbol or company name.
    
    Args:
        search: Full or partial symbol name to search for
        company: Full or partial company name (optional)
        type: Security type - EQ (equity), MF (mutual fund), OPTN (option) (optional)
        
    Returns:
        List of matching products with details
    """
    client = get_market_client()
    return client.look_up_product(search, company, type)


@mcp.tool()
def etrade_get_option_chains(symbol: str, expiry_year: Optional[int] = None,
                            expiry_month: Optional[int] = None, expiry_day: Optional[int] = None,
                            strike_price_near: Optional[float] = None, no_of_strikes: Optional[int] = None,
                            include_weekly: bool = False, skip_adjusted: bool = False,
                            option_category: Optional[str] = None, chain_type: Optional[str] = None,
                            price_type: Optional[str] = None) -> dict:
    """
    Get option chains for a symbol.
    
    Args:
        symbol: Underlying stock symbol (e.g., "AAPL")
        expiry_year: Expiration year (4-digit, e.g., 2024)
        expiry_month: Expiration month (1-12)
        expiry_day: Expiration day (1-31)
        strike_price_near: Strike price near this value
        no_of_strikes: Number of strikes to return
        include_weekly: Include weekly options
        skip_adjusted: Skip adjusted options
        option_category: STANDARD, ALL, or MINI
        chain_type: CALL, PUT, or CALLPUT
        price_type: ATNM (at the money) or ALL
        
    Returns:
        Option chain data with available strikes and expiration dates
    """
    client = get_market_client()
    return client.get_option_chains(
        symbol, expiry_year, expiry_month, expiry_day,
        strike_price_near, no_of_strikes, include_weekly, skip_adjusted,
        option_category, chain_type, price_type
    )


@mcp.tool()
def etrade_get_option_expire_dates(symbol: str, expiry_type: Optional[str] = None) -> dict:
    """
    Get option expiration dates for a symbol.
    
    Args:
        symbol: Underlying stock symbol (e.g., "AAPL")
        expiry_type: WEEKLY, MONTHLY, QUARTERLY, or ALL (optional)
        
    Returns:
        List of available expiration dates for options
    """
    client = get_market_client()
    return client.get_option_expire_dates(symbol, expiry_type)


def main():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()

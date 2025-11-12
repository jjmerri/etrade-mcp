# E*TRADE MCP Server

A Model Context Protocol (MCP) server for E*TRADE's Market API, built with FastMCP.

## Features

This MCP server provides access to E*TRADE's Market API endpoints:

- **Quote**: Get real-time and delayed quotes for stocks, options, and mutual funds
- **Product Lookup**: Search for securities by symbol or company name
- **Option Chains**: Get option chains with strikes and expirations
- **Option Expire Dates**: Get available expiration dates for options

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -e .
```

3. Copy `.env.example` to `.env` and add your E*TRADE API credentials:
```bash
cp .env.example .env
```

4. Edit `.env` and add your credentials:
```
ETRADE_CONSUMER_KEY=your_consumer_key_here
ETRADE_CONSUMER_SECRET=your_consumer_secret_here
ETRADE_ENVIRONMENT=sandbox  # or 'production'
```

## Getting E*TRADE API Credentials

1. Go to [E*TRADE Developer Portal](https://developer.etrade.com/)
2. Sign up or log in
3. Create a new application
4. Get your Consumer Key and Consumer Secret
5. Start with the sandbox environment for testing

## Usage

### Running the Server

```bash
etrade-mcp
```

Or with Python:
```bash
python -m etrade_mcp.server
```

### Authentication Flow

1. Call `etrade_get_auth_url()` to get the authorization URL
2. Visit the URL in your browser and authorize the application
3. Copy the verification code
4. Call `etrade_authenticate(verifier="YOUR_CODE")` with the verification code

### Available Tools

#### `etrade_get_auth_url()`
Get the OAuth authorization URL. This is the first step in authentication.

**Returns**: Authorization URL to visit in browser

#### `etrade_authenticate(verifier: str)`
Complete authentication with the verification code from E*TRADE.

**Args**:
- `verifier`: Verification code from E*TRADE

**Returns**: Success message

#### `etrade_get_quote(symbols: str, require_earnings_date: bool = False, skip_mini_options_check: bool = False)`
Get stock quotes for one or more symbols.

**Args**:
- `symbols`: Comma-separated list of symbols (e.g., "AAPL,MSFT,GOOGL")
- `require_earnings_date`: Include next earnings date
- `skip_mini_options_check`: Skip mini options check

**Returns**: Quote data with prices, volume, bid/ask, etc.

#### `etrade_lookup_product(search: str, company: str = None, type: str = None)`
Look up products by symbol or company name.

**Args**:
- `search`: Symbol or partial symbol to search
- `company`: Company name (optional)
- `type`: Security type - EQ, MF, OPTN (optional)

**Returns**: List of matching products

#### `etrade_get_option_chains(symbol: str, ...)`
Get option chains for a symbol with various filters.

**Args**:
- `symbol`: Underlying symbol
- `expiry_year`, `expiry_month`, `expiry_day`: Expiration date filters
- `strike_price_near`: Filter strikes near this price
- `no_of_strikes`: Number of strikes to return
- `include_weekly`: Include weekly options
- `option_category`: STANDARD, ALL, MINI
- `chain_type`: CALL, PUT, CALLPUT
- And more...

**Returns**: Option chain data

#### `etrade_get_option_expire_dates(symbol: str, expiry_type: str = None)`
Get available option expiration dates.

**Args**:
- `symbol`: Underlying symbol
- `expiry_type`: WEEKLY, MONTHLY, QUARTERLY, ALL

**Returns**: List of expiration dates

## Example Usage with MCP Client

```python
# Get authorization URL
auth_url = etrade_get_auth_url()
# Visit the URL, authorize, get verifier code

# Authenticate
etrade_authenticate(verifier="12345")

# Get a quote
quote = etrade_get_quote(symbols="AAPL")

# Look up a product
results = etrade_lookup_product(search="Apple")

# Get option chains
chains = etrade_get_option_chains(
    symbol="AAPL",
    chain_type="CALL",
    price_type="ATNM"
)

# Get expiration dates
dates = etrade_get_option_expire_dates(symbol="AAPL")
```

## API Documentation

For detailed API documentation, see:
- [E*TRADE API Documentation](https://developer.etrade.com/home)
- [Market Quote API](https://apisb.etrade.com/docs/api/market/api-quote-v1.html)

## Environment Variables

- `ETRADE_CONSUMER_KEY`: Your E*TRADE consumer key (required)
- `ETRADE_CONSUMER_SECRET`: Your E*TRADE consumer secret (required)
- `ETRADE_ENVIRONMENT`: `sandbox` or `production` (default: sandbox)
- `ETRADE_SANDBOX_BASE_URL`: Sandbox API URL (default: https://apisb.etrade.com)
- `ETRADE_PROD_BASE_URL`: Production API URL (default: https://api.etrade.com)

## Security Notes

- Never commit your `.env` file or expose your API credentials
- Start with the sandbox environment for testing
- OAuth tokens expire; you'll need to re-authenticate periodically
- Production environment requires additional E*TRADE account approvals

## Reference

This server is based on E*TRADE's sample Python client, which is included in the `EtradePythonClient` directory for reference.

## License

MIT

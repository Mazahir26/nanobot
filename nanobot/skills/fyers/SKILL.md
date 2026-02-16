---
name: fyers
description: Trade on Fyers platform - place orders, manage portfolio, get market data. Use when user asks about stocks, trading, portfolio, holdings, or market quotes.
---

# Fyers Trading Platform

Execute trades and manage your Fyers trading account.

## Tools

### Server Monitoring
- `mcp_fyers_get_health()` — Check server health status
- `mcp_fyers_get_status()` — Get detailed server status and auth info

### Authentication

Authenticate before using trading tools.

### Step 1: Get Auth URL

Call `mcp_fyers_get_auth_url()` to generate the OAuth login URL.

### Step 2: Complete Authentication

**Auto-flow** (if callback server running can get to know from mcp_fyers_get_status):
- Open the URL in browser → Login → Redirect captures code automatically
- Call `mcp_fyers_authenticate()` with no arguments

**Manual flow** (headless/server):
- Open the URL in browser → Login → Copy `auth_code` from redirect URL
- Call `mcp_fyers_authenticate(auth_code="XYZ123")`

### Verify Status

Use `mcp_fyers_check_auth_status()` to verify authentication.

## Tools

### Portfolio Management
- `mcp_fyers_get_profile()` - User profile information
- `mcp_fyers_get_funds()` - Account balance and margin details
- `mcp_fyers_get_holdings()` - Portfolio holdings with P&L
- `mcp_fyers_get_positions()` - Current trading positions

### Trading
- `mcp_fyers_place_order(symbol, qty, side, type, productType, validity, ...)` - Place new order
  - `symbol`: Trading instrument (e.g., "NSE:SBIN-EQ")
  - `qty`: Number of units (integer)
  - `side`: 1 for BUY, -1 for SELL
  - `type`: 1=LIMIT, 2=MARKET, 3=SL-M, 4=SL-L
  - `productType`: "CNC", "INTRADAY", "MARGIN", etc.
  - `validity`: "DAY" or "IOC"
  - Optional: `limitPrice`, `stopPrice`, `disclosedQty`, `orderTag`
- `mcp_fyers_modify_order(id, ...)` - Modify existing order by ID
- `mcp_fyers_cancel_order(id)` - Cancel pending order by ID
- `mcp_fyers_get_orders()` - Order history and status

### Market Data
- `mcp_fyers_get_quotes(symbols)` - Real-time quotes for multiple symbols
  - `symbols`: List of instruments (e.g., `["NSE:SBIN-EQ", "NSE:RELIANCE-EQ"]`)

## Example Workflow

```
1. mcp_fyers_get_auth_url() → Open URL in browser
2. mcp_fyers_authenticate(auth_code="...") → Complete OAuth
3. mcp_fyers_check_auth_status() → Verify active
4. mcp_fyers_get_funds() → Check balance
5. mcp_fyers_place_order(symbol="NSE:SBIN-EQ", qty=10, side=1, type=2, productType="CNC", validity="DAY")
6. mcp_fyers_get_holdings() → Confirm position
```


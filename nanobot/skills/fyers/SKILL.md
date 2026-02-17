---
name: fyers
description: Trade on Fyers platform - place orders, manage portfolio, get market data. Use when user asks about stocks, trading, portfolio, holdings, or market quotes.
---

# Fyers Trading Platform

Execute trades and manage your Fyers trading account via MCP server.

## Quick Start

**First time setup:**
1. `mcp_fyers_get_auth_url()` → Open URL in browser
2. Login to Fyers → Auth code captured automatically (or copy manually)
3. `mcp_fyers_authenticate(auth_code="...")` → Token saved for future sessions

**Already authenticated:**
- Directly use trading tools: `mcp_fyers_get_holdings()`, `mcp_fyers_place_order(...)`, etc.
- Token persists across sessions in `fyers_token.json`

## Authentication Flow

### Check Server Status First

```bash
mcp_fyers_server_status()
```

This tells you:
- If callback server is running (auto-capture mode)
- Current authentication state
- Redirect URI configuration

### Step 1: Generate Auth URL

```bash
mcp_fyers_get_auth_url()
```

Returns a URL like: `https://api-t1.fyers.in/api/v3/generate-authcode?client_id=XXX&redirect_uri=...`

### Step 2: Complete OAuth Login

**Mode A: Automatic Callback (Recommended)**

Check if enabled: `mcp_fyers_server_status()` → `callback_server_enabled: true`
if `callback_server_enabled` this is returned true then user does not have to manualy paste the code (It will automaiclly login)

1. Open the auth URL in browser
2. Login to Fyers account
3. Redirected to callback server → auth code captured automatically
4. Call `mcp_fyers_authenticate()` with **no arguments**
5. ✅ Token saved to `fyers_token.json`

**Mode B: Manual Copy-Paste (Headless/Server)**

Check if enabled: `mcp_fyers_server_status()` → `callback_server_enabled: false`

1. Open the auth URL in browser
2. Login to Fyers account
3. **Copy the `auth_code` parameter** from redirect URL:
   - URL format: `http://localhost:300/?auth_code=eyJhbGciOiJIUzI1NiIs...`
   - Copy everything after `auth_code=`
4. Call `mcp_fyers_authenticate(auth_code="COPIED_CODE_HERE")`
5. ✅ Token saved to `fyers_token.json`

### Step 3: Verify Authentication

```bash
mcp_fyers_check_auth_status()
```

Returns:
- `"✓ Authenticated and connected to Fyers API"` → Ready to trade
- `"✗ Token invalid: ..."` → Re-authenticate
- `"Not authenticated..."` → Call `mcp_fyers_authenticate()`

### Token Persistence

- Access token saved to `fyers_token.json` after successful auth
- Automatically loaded on server restart
- No need to re-authenticate unless token expires
- Call `mcp_fyers_logout()` to clear token

## Tools Reference

### Server Monitoring

| Tool | Description |
|------|-------------|
| `mcp_fyers_server_health()` | Check server health and auth status |
| `mcp_fyers_server_status()` | Get detailed config (callback mode, token file path) |

### Authentication

| Tool | Description |
|------|-------------|
| `mcp_fyers_get_auth_url()` | Generate OAuth login URL |
| `mcp_fyers_authenticate(auth_code)` | Complete OAuth (code optional if auto-callback) |
| `mcp_fyers_check_auth_status()` | Verify authentication status |
| `mcp_fyers_logout()` | Clear stored token |

### Portfolio & Funds

| Tool | Description |
|------|-------------|
| `mcp_fyers_get_profile()` | User profile (name, email, account type) |
| `mcp_fyers_get_funds()` | Account balance, margins, collateral |
| `mcp_fyers_get_holdings()` | Portfolio holdings with P&L |
| `mcp_fyers_get_positions()` | Current open positions |

### Trading

| Tool | Description |
|------|-------------|
| `mcp_fyers_place_order(...)` | Place new order |
| `mcp_fyers_modify_order(id, ...)` | Modify existing order |
| `mcp_fyers_cancel_order(id)` | Cancel pending order |
| `mcp_fyers_get_orders()` | Order history |

### Market Data

| Tool | Description |
|------|-------------|
| `mcp_fyers_get_quotes(symbols)` | Real-time quotes for multiple symbols |

## Trading Parameters

### `mcp_fyers_place_order`

**Required:**
- `symbol`: Trading instrument (e.g., `"NSE:SBIN-EQ"`, `"NSE:NIFTY24FEB22000CE"`)
- `qty`: Quantity (integer, e.g., `10`)
- `side`: `1` = BUY, `-1` = SELL
- `type`: `1` = LIMIT, `2` = MARKET, `3` = SL-M, `4` = SL-L
- `productType`: `"CNC"` (delivery), `"INTRADAY"`, `"MARGIN"`, `"COV"`, `"BO"`
- `validity`: `"DAY"` or `"IOC"`

**Optional:**
- `limitPrice`: Price for LIMIT orders (e.g., `2250.50`)
- `stopPrice`: Stop loss trigger for SL orders
- `disclosedQty`: Quantity to disclose (for large orders)
- `orderTag`: Tag for tracking (e.g., `"my_strategy_1"`)
- `segment`: Segment ID (e.g., `10` for NSE_EQ)
- `stopLoss`: Stop loss for BO/CO orders
- `takeProfit`: Take profit for BO/CO orders

### `mcp_fyers_modify_order`

**Required:**
- `id`: Order ID to modify (e.g., `"2402170001234567"`)

**Optional (provide at least one):**
- `qty`: New quantity
- `limitPrice`: New limit price
- `stopPrice`: New stop price
- `type`: New order type
- `validity`: New validity

### `mcp_fyers_get_quotes`

**Required:**
- `symbols`: Array of instruments
  - Format: `"NSE:SYMBOL-EQ"` for equity
  - Example: `["NSE:SBIN-EQ", "NSE:RELIANCE-EQ", "NSE:TATAMOTORS-EQ"]`

## Example Workflows

### Workflow 1: First-Time Setup

```
1. mcp_fyers_server_status()
   → Check callback mode and auth state

2. mcp_fyers_get_auth_url()
   → Returns: "Open this URL: https://api-t1.fyers.in/..."

3. [User opens URL, logs in to Fyers]

4a. If auto-callback: mcp_fyers_authenticate()
4b. If manual: mcp_fyers_authenticate(auth_code="eyJhbGci...")

5. mcp_fyers_check_auth_status()
   → "✓ Authenticated and connected to Fyers API"
```

### Workflow 2: Check Portfolio

```
1. mcp_fyers_get_funds()
   → Returns: {"fund_available": 50000, "margin_used": 12000, ...}

2. mcp_fyers_get_holdings()
   → Returns: {"holdings": [{"symbol": "NSE:SBIN-EQ", "qty": 100, "pnl": 2500}, ...]}

3. mcp_fyers_get_positions()
   → Returns: {"positions": [{"symbol": "NSE:TATAMOTORS-EQ", "side": "BUY", "qty": 50}, ...]}
```

### Workflow 3: Place Market Order

```
1. mcp_fyers_get_quotes(symbols=["NSE:SBIN-EQ"])
   → Check current price: ₹225.50

2. mcp_fyers_place_order(
       symbol="NSE:SBIN-EQ",
       qty=10,
       side=1,
       type=2,
       productType="CNC",
       validity="DAY"
     )
   → Returns: {"id": "2402170001234567", "status": "success"}

3. mcp_fyers_get_orders()
   → Confirm order placed
```

### Workflow 4: Place Limit Order with Stop Loss

```
mcp_fyers_place_order(
    symbol="NSE:RELIANCE-EQ",
    qty=5,
    side=1,
    type=1,           # LIMIT order
    productType="CNC",
    validity="DAY",
    limitPrice=2450.00,
    stopLoss=2400.00,
    takeProfit=2550.00
)
```

### Workflow 5: Modify and Cancel Orders

```
1. mcp_fyers_get_orders()
   → Find order ID: "2402170001234567"

2. mcp_fyers_modify_order(
       id="2402170001234567",
       limitPrice=2260.00  # Increase limit price
     )

3. [If needed] mcp_fyers_cancel_order(id="2402170001234567")
```

## Symbol Format Reference

| Segment | Format | Example |
|---------|--------|---------|
| NSE Equity | `NSE:SYMBOL-EQ` | `NSE:SBIN-EQ` |
| NSE Futures | `NSE:SYMBOL24FEBFUT` | `NSE:NIFTY24FEBFUT` |
| NSE Options | `NSE:SYMBOL24FEB22000CE` | `NSE:NIFTY24FEB22000CE` |
| BSE Equity | `BSE:SYMBOL-EQ` | `BSE:RELIANCE-EQ` |
| MCX Commodity | `MCX:SYMBOL24FEBFUT` | `MCX:GOLD24FEBFUT` |

## Error Handling

**"Not authenticated"**
→ Call `mcp_fyers_check_auth_status()` then `mcp_fyers_authenticate()`

**"Token expired"**
→ Call `mcp_fyers_logout()` then re-authenticate

**"Invalid symbol"**
→ Check symbol format: `NSE:SYMBOL-EQ` for equity

**"Insufficient margin"**
→ Call `mcp_fyers_get_funds()` to check available balance

**"Order rejected"**
→ Call `mcp_fyers_get_orders()` to see rejection reason

## Configuration

The MCP server is configured via:
- `FYERS_APP_ID` / `FYERS_SECRET_KEY` → Fyers API credentials
- `FYERS_REDIRECT_URI` → Callback URL (auto-flow if `:8080`)
- `TOKEN_FILE` → Token persistence path (default: `./fyers_token.json`)

Server endpoints:
- MCP: `http://host:8333/mcp` (streamable HTTP transport)
- Callback: `http://host:8080/` (only if auto-flow enabled)
- Health: `http://host:8333/health` (requires `X-API-Key` header)

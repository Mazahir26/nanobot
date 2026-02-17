---
name: fyers
description: Trade on Fyers platform - place orders, manage portfolio, get market data, search symbols. Use when user asks about stocks, trading, portfolio, holdings, positions, orders, or market quotes.
---

# Fyers Trading Platform

Execute trades and manage your Fyers trading account via MCP server.

## Quick Start

**First time setup:**
1. `check_auth_status()` - Check if already authenticated
2. If not authenticated: `set_pin(pin="123456")` then `get_auth_url()`
3. Login to Fyers - authentication completes automatically
4. Done! Ready to trade

**Already authenticated:**
- Directly use trading tools: `get_holdings()`, `place_order()`, etc.

## Authentication Flow

### Step 1: Check Status (Always First)

```bash
check_auth_status()
```

- If "Authenticated" → Skip to trading
- If "Not authenticated" → Continue to Step 2

### Step 2: Set PIN (Only if not authenticated)

```bash
set_pin(pin="123456")
```

PIN is your 6-digit Fyers trading PIN. Required before authentication.

### Step 3: Get Auth URL

```bash
get_auth_url()
```

Returns OAuth login URL. Open in browser.

### Step 4: Login

1. Open auth URL in browser
2. Login to Fyers account
3. Redirected back - authentication completes automatically
4. Tokens saved, auto-refresh enabled

### Step 5: Verify (Optional)

```bash
check_auth_status()
```

Should confirm authenticated status.

## Tools Reference

### Authentication

| Tool | Description |
|------|-------------|
| `set_pin(pin)` | Set 6-digit trading PIN (required first) |
| `get_auth_url()` | Generate OAuth login URL |
| `check_auth_status()` | Verify authentication status |
| `refresh_access_token()` | Manually refresh token |
| `remove_pin()` | Clear PIN, stop auto-refresh |
| `logout()` | Clear token and logout |

### Portfolio & Funds

| Tool | Description |
|------|-------------|
| `get_profile()` | User profile info |
| `get_funds()` | Account balance, margins |
| `get_holdings()` | Portfolio holdings with P&L |
| `get_positions()` | Current open positions |
| `get_orders()` | Order history |

### Trading

| Tool | Description |
|------|-------------|
| `place_order(...)` | Place new order |
| `modify_order(id, ...)` | Modify existing order |
| `cancel_order(id)` | Cancel pending order |

### Market Data

| Tool | Description |
|------|-------------|
| `get_quotes(symbols)` | Real-time quotes |

### Symbol Search

| Tool | Description |
|------|-------------|
| `search_symbols(query, limit)` | Fuzzy search (handles typos) |
| `get_symbol_details(symbol)` | Get full symbol details |
| `refresh_symbol_master()` | Refresh symbol data |

## Trading Parameters

### `place_order`

**Required:**
- `symbol` - Trading instrument (e.g., `"NSE:SBIN-EQ"`)
- `qty` - Quantity (integer)
- `side` - `1` = BUY, `-1` = SELL
- `type` - `1` = LIMIT, `2` = MARKET, `3` = SL-M, `4` = SL-L
- `productType` - `"CNC"`, `"INTRADAY"`, `"MARGIN"`, etc.
- `validity` - `"DAY"` or `"IOC"`

**Optional:**
- `limitPrice` - Price for LIMIT orders
- `stopPrice` - Stop loss for SL orders
- `disclosedQty` - Quantity to disclose
- `orderTag` - Tag for tracking
- `stopLoss` / `takeProfit` - For BO/CO orders

### `get_quotes`

**Required:**
- `symbols` - Array of instruments
  - Example: `["NSE:SBIN-EQ", "NSE:RELIANCE-EQ"]`

### `search_symbols`

**Required:**
- `query` - Search term (company name or symbol)
- `limit` - Max results (default 20)

**Examples:**
- `"reliance"` → NSE:RELIANCE-EQ
- `"nifty 22000"` → NSE:NIFTY24FEB22000CE
- `"tata"` → All Tata companies

## Example Workflows

### First-Time Setup

```
1. check_auth_status() → "Not authenticated"
2. set_pin(pin="123456")
3. get_auth_url()
4. [Open URL, login to Fyers]
5. check_auth_status() → "Authenticated"
```

### Returning User (Already Authenticated)

```
1. check_auth_status() → "Authenticated"
2. get_holdings()  # Ready to trade
```

### Find Symbol and Place Order

```
1. search_symbols(query="reliance", limit=5)
2. get_quotes(symbols=["NSE:RELIANCE-EQ"])
3. place_order(symbol="NSE:RELIANCE-EQ", qty=5, side=1, type=2, productType="CNC", validity="DAY")
```

### Check Portfolio

```
1. get_funds()
2. get_holdings()
3. get_positions()
```

### Place Limit Order

```
place_order(
    symbol="NSE:RELIANCE-EQ",
    qty=5,
    side=1,
    type=1,
    productType="CNC",
    validity="DAY",
    limitPrice=2450.00
)
```

### Modify/Cancel Order

```
1. get_orders() → Find order ID
2. modify_order(id="...", limitPrice=2260.00)
3. cancel_order(id="...")  # If needed
```

**Tip:** Use `search_symbols()` to find exact symbol format.

## Error Handling

| Error | Solution |
|-------|----------|
| "PIN not set" | Call `set_pin(pin="123456")` before authentication |
| "Not authenticated" | Complete auth flow: set_pin → get_auth_url → login |
| "Token expired" | Call `logout()` then re-authenticate |
| "Invalid symbol" | Use `search_symbols()` to find correct format |
| "Insufficient margin" | Call `get_funds()` to check balance |
| "Order rejected" | Call `get_orders()` to see reason |

## Key Points

1. **PIN mandatory** - Must call `set_pin()` before `get_auth_url()`
2. **Auto-complete** - Login redirects back and auth completes automatically
3. **Auto-refresh** - Token refreshes automatically every 20 hours
4. **Fuzzy search** - Use `search_symbols()` to handle typos
5. **Check status first** - Always use `check_auth_status()` before trading

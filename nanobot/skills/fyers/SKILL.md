---
name: fyers
description: Trade stocks on Fyers platform - place orders, manage portfolio, check holdings, positions, funds, get market quotes, search symbols. Use this skill whenever the user mentions stocks, trading, portfolio, holdings, positions, orders, buy/sell stocks, market data, quotes, Fyers, Indian stock market, NSE, BSE, intraday, delivery, CNC, or anything related to equity trading in India.
---

# Fyers Trading Platform

Execute trades and manage your Fyers trading account via MCP server.

## Quick Start

**First time setup:**
1. `check_auth_status()` - Check if already authenticated
2. If not authenticated: `set_pin(pin="1234")` then `get_auth_url()`
3. Open the returned URL in browser → Login to Fyers
4. Authentication completes automatically (no copy-paste needed)
5. Done! Ready to trade

**Already authenticated:**
- Directly use trading tools: `get_holdings()`, `manage_order()`, etc.

---

## Authentication Flow

### Step 1: Check Status (Always First)

```python
check_auth_status()
```

- If "Authenticated" → Skip to trading
- If "Not authenticated" → Continue to Step 2

### Step 2: Set PIN (Required before auth)

```python
set_pin(pin="1234")  # Your 4-digit Fyers trading PIN
```

### Step 3: Get Auth URL

```python
get_auth_url()
```

Returns a clickable OAuth login URL. Open in browser to login. Auth code is captured automatically.

### Step 4: Verify

```python
check_auth_status()  # Should confirm authenticated
```

---

## MCP Configuration

Add to your `~/.nanobot/config.json`:

```json
{
  "tools": {
    "mcp_servers": {
      "fyers": {
        "url": "http://localhost:8000/sse/"
      }
    }
  }
}
```

**Prerequisites:**
- Fyers MCP server running on port 8000
- Set `FYERS_APP_ID` and `FYERS_SECRET_KEY` in server's `.env`

---

## Tools Reference (27 Tools)

### Authentication (6 tools)

| Tool | Description |
|------|-------------|
| `set_pin(pin)` | Set 4-digit trading PIN (required first) |
| `get_auth_url` | Generate OAuth login URL |
| `check_auth_status` | Verify authentication status |
| `refresh_access_token` | Manually refresh token |
| `remove_pin` | Clear PIN, stop auto-refresh |
| `logout` | Clear token and logout |

### Portfolio & Funds (5 tools)

| Tool | Description |
|------|-------------|
| `get_profile` | User profile information |
| `get_funds` | Account balance and margins |
| `get_holdings` | Portfolio holdings with P/L |
| `get_positions` | Current open positions |
| `get_quotes(symbols)` | Real-time quotes for symbols |

### Order Management (2 tools)

| Tool | Description |
|------|-------------|
| `manage_order(action, ...)` | Place/modify/cancel orders. **Actions:** `"place"`, `"modify"`, `"cancel"` |
| `place_batch_order(type, ...)` | Multi-order/multi-leg/exit-all. **Types:** `"multi"`, `"multi_leg"`, `"exit_all"` |

### GTT Orders (1 tool)

| Tool | Description |
|------|-------------|
| `manage_gtt_order(action, ...)` | Place/get/modify/cancel GTT orders. **Actions:** `"place"`, `"get"`, `"modify"`, `"cancel"` |

### Smart Orders (1 tool)

| Tool | Description |
|------|-------------|
| `manage_smart_order(action, ...)` | Place/get/modify/pause/resume/cancel smart orders. **Actions:** `"place_limit"`, `"place_trail"`, `"place_step"`, `"place_sip"`, `"get"`, `"modify"`, `"pause"`, `"resume"`, `"cancel"` |

### Smart Exits (1 tool)

| Tool | Description |
|------|-------------|
| `manage_smart_exit(action, ...)` | Create/get/modify/cancel smart exits. **Actions:** `"create"`, `"get"`, `"modify"`, `"cancel"` |

### History & Reports (1 tool)

| Tool | Description |
|------|-------------|
| `get_history(type, ...)` | Get order/trade history. **Types:** `"orders"`, `"trades"` |

### Market Data (1 tool)

| Tool | Description |
|------|-------------|
| `get_market_data(type, ...)` | Get candles/depth/status/option-chain. **Types:** `"candles"`, `"depth"`, `"status"`, `"option_chain"` |

### Position Management (1 tool)

| Tool | Description |
|------|-------------|
| `convert_position(...)` | Convert position product type (e.g., INTRADAY→CNC) |

### Symbol Search (3 tools)

| Tool | Description |
|------|-------------|
| `search_symbols(query, limit)` | Fuzzy search for symbols (handles typos) |
| `get_symbol_details(symbol)` | Get full symbol details |
| `refresh_symbol_master` | Refresh symbol data |

### Server (2 tools)

| Tool | Description |
|------|-------------|
| `server_health` | Check server health |
| `server_status` | Get server status |

---

## Order Parameters

### `manage_order(action="place", ...)`

**Required for place:**
- `symbol` - Trading symbol (e.g., `"NSE:RELIANCE-EQ"`)
- `qty` - Quantity (integer)
- `side` - `1` = BUY, `-1` = SELL
- `type` - `1` = LIMIT, `2` = MARKET, `3` = SL-M, `4` = SL-L
- `productType` - `"CNC"`, `"INTRADAY"`, `"MARGIN"`, `"MTF"`
- `validity` - `"DAY"` or `"IOC"`

**Optional:**
- `limitPrice` - Price for LIMIT orders
- `stopPrice` - Stop price for SL orders
- `disclosedQty` - Disclosed quantity
- `offlineOrder` - `true` for AMO
- `orderTag` - Tag for tracking
- `stopLoss` / `takeProfit` - For BO/CO orders

**For modify/cancel:**
- `id` - Order ID (required)

### `place_batch_order(type="multi", ...)`

**For "multi" (up to 10 orders):**
- `orders` - List of order objects

**For "multi_leg" (2L/3L/4L):**
- `orderType` - `"2L"`, `"3L"`, or `"4L"`
- `legs` - List of leg objects
- `productType` - `"INTRADAY"` or `"MARGIN"`

**For "exit_all":**
- `symbol` - Symbol to exit
- `productType` - Product type

---

## Symbol Format

Use exchange prefix with instrument type:

| Segment | Format | Example |
|---------|--------|---------|
| NSE Equity | `NSE:SYMBOL-EQ` | `NSE:RELIANCE-EQ` |
| BSE Equity | `BSE:SYMBOL-EQ` | `BSE:RELIANCE-EQ` |
| NSE F&O | `NSE:SYMBOLYYMMSTRIKECE/PE` | `NSE:NIFTY24FEB22000CE` |
| MCX | `MCX:SYMBOLYYMM` | `MCX:CRUDEOIL24FEB` |

---

## Example Workflows

### First-Time Setup

```python
check_auth_status()         # → "Not authenticated"
set_pin(pin="1234")         # Set 4-digit PIN
get_auth_url()              # → Returns URL
# Open URL in browser, login to Fyers
check_auth_status()         # → "Authenticated"
```

### Check Portfolio

```python
get_funds()                 # Account balance
get_holdings()              # Portfolio holdings
get_positions()             # Open positions
```

### Find Symbol and Place Order

```python
search_symbols(query="reliance", limit=5)
# → NSE:RELIANCE-EQ

get_quotes(symbols=["NSE:RELIANCE-EQ"])
# → Current price info

manage_order(
    action="place",
    symbol="NSE:RELIANCE-EQ",
    qty=5,
    side=1,          # BUY
    type=2,          # MARKET
    productType="CNC",
    validity="DAY"
)
```

### Place Limit Order

```python
manage_order(
    action="place",
    symbol="NSE:SBIN-EQ",
    qty=10,
    side=1,              # BUY
    type=1,              # LIMIT
    productType="CNC",
    validity="DAY",
    limitPrice=625.50
)
```

### Place GTT Order (Good Till Trigger)

```python
manage_gtt_order(
    action="place",
    symbol="NSE:RELIANCE-EQ",
    side=1,                    # BUY
    productType="CNC",
    leg1_price=2400,           # Price
    leg1_triggerPrice=2420,    # Trigger when price hits 2420
    leg1_qty=5                 # Quantity
)
```

### Modify/Cancel Order

```python
get_history(type="orders")   # Find order ID

manage_order(
    action="modify",
    id="240123001234",
    limitPrice=2450.00
)

manage_order(action="cancel", id="240123001234")
```

### Exit All Positions

```python
place_batch_order(
    type="exit_all",
    symbol="NSE:RELIANCE-EQ",
    productType="INTRADAY"
)
```

---

## Product Types

| Type | Description | Use Case |
|------|-------------|----------|
| `CNC` | Cash and Carry | Delivery/long-term holdings |
| `INTRADAY` | Intraday | Square-off same day |
| `MARGIN` | Margin Trading | Leverage, hold up to T+5 |
| `MTF` | Margin Trading Facility | Long-term with leverage |

---

## Order Types

| Type | Value | Description |
|------|-------|-------------|
| LIMIT | `1` | Execute at specified price |
| MARKET | `2` | Execute at best available price |
| SL-M | `3` | Stop Loss Market |
| SL-L | `4` | Stop Loss Limit |

---

## Error Handling

| Error | Solution |
|-------|----------|
| "PIN not set" | Call `set_pin(pin="1234")` before auth |
| "Not authenticated" | Complete auth flow |
| "Token expired" | Auto-refreshes, or call `logout()` and re-auth |
| "Invalid symbol" | Use `search_symbols()` to find correct format |
| "Insufficient margin" | Call `get_funds()` to check balance |

---

## Key Points

1. **Check status first** - Always use `check_auth_status()` before trading
2. **PIN mandatory** - Must call `set_pin()` before `get_auth_url()`
3. **Auto-capture** - OAuth flow captures auth code automatically (no copy-paste)
4. **Auto-refresh** - Token refreshes automatically every 3 hours
5. **Use search** - Always use `search_symbols()` to find exact symbol format
6. **Consolidated tools** - `manage_order`, `manage_gtt_order`, `manage_smart_order` handle multiple actions
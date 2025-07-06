# Analyze Financial Tick Data with TimescaleDB

Efficiently convert raw, real-time cryptocurrency data into insightful candlestick views using TimescaleDB hyperfunctions and continuous aggregates.

---

## Why Use Hyperfunctions?

TimescaleDB provides built-in **hyperfunctions**, making it easier to:

- ✅ Aggregate large volumes of financial data
- ✅ Generate candlestick charts with fewer SQL lines
- ✅ Optimize query performance for real-time dashboards

Key hyperfunctions you'll use:

| Function          | Purpose                                  |
| ----------------- | ---------------------------------------- |
| `time_bucket()`   | Groups data into fixed time intervals    |
| `FIRST()`         | Captures the opening price in the bucket |
| `LAST()`          | Captures the closing price in the bucket |
| `MIN()` / `MAX()` | Finds lowest and highest price points    |

---

## Step 1: Create a Continuous Aggregate

### What is a Continuous Aggregate?

A materialized view that automatically maintains pre-aggregated candlestick data, significantly reducing query overhead for real-time analysis.

#### Example: Create Daily OHLCV View

Connect to your TimescaleDB instance:

```sql
CREATE MATERIALIZED VIEW one_day_candle
WITH (timescaledb.continuous) AS
    SELECT
        time_bucket('1 day', time) AS bucket,
        symbol,
        FIRST(price, time) AS "open",
        MAX(price) AS high,
        MIN(price) AS low,
        LAST(price, time) AS "close",
        LAST(day_volume, time) AS day_volume
    FROM crypto_sample
    GROUP BY bucket, symbol;
```

✅ **Note:** You can adjust the `time_bucket` interval to other timeframes (e.g., `1 hour`, `15 minutes`).

---

## Step 2: Add an Automatic Refresh Policy

To keep your aggregates updated:

```sql
SELECT add_continuous_aggregate_policy('one_day_candle',
    start_offset => INTERVAL '3 days',
    end_offset => INTERVAL '1 day',
    schedule_interval => INTERVAL '1 day');
```

✅ This refreshes the last 2 days' worth of data every 24 hours.

---

## Step 3: Query the OHLCV Data

Example: Retrieve 14 days of Bitcoin candlestick data:

```sql
SELECT * FROM one_day_candle
WHERE symbol = 'BTC/USD'
AND bucket >= NOW() - INTERVAL '14 days'
ORDER BY bucket;
```

#### Sample Output:

| bucket              | symbol  | open    | high    | low     | close   | day\_volume |
| ------------------- | ------- | ------- | ------- | ------- | ------- | ----------- |
| 2022-11-24 00:00:00 | BTC/USD | 16587   | 16781.2 | 16463.4 | 16597.4 | 21803       |
| 2022-11-25 00:00:00 | BTC/USD | 16597.4 | 16610.1 | 16344.4 | 16503.1 | 20788       |
| 2022-11-26 00:00:00 | BTC/USD | 16507.9 | 16685.5 | 16384.5 | 16450.6 | 12300       |

---

## Step 4: Visualize OHLCV Data in Grafana

### Setup:

- ✅ Ensure your TimescaleDB is added as a **Data Source** in Grafana
- ✅ Grafana is accessible (e.g., [http://localhost:3000](http://localhost:3000))

#### Creating the Candlestick Chart:

1. Go to **Dashboards → New Dashboard → Add a new panel**
2. Select **Candlestick** from the visualization options
3. Click **Edit SQL** and paste your OHLCV query
4. In the **Format as** dropdown, select `Table`
5. Customize your table and chart appearance
6. Click **Apply** to save your visualization

---

### Grafana Candlestick Chart Preview

![Candlestick Chart Example](./preview/grafana_candlestick.png)

---

Understood. You want technical clarity with **what the query does, key points, and details clearly explained *before*** the SQL block, and no vague "technical notes" at the end. Here's the rewritten **Additional Essential Queries** section in your desired structured, precise, beginner-friendly style:

---

# Additional Essential Queries for Financial Tick Data

The following examples demonstrate important queries using TimescaleDB for financial datasets.

---

### 1. Calculate a 7-Day Simple Moving Average (SMA)

**Purpose:**
Compute the average closing price over a sliding window of the last 7 days, commonly used in financial analysis to smooth short-term price fluctuations.

**Key Details:**

* Uses `AVG()` window function for rolling average
* `PARTITION BY symbol` ensures separate SMA per crypto symbol
* `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` defines a 7-row sliding window
* Assumes one row per day (use with daily aggregates like `one_day_candle`)

**Query:**

```sql
SELECT
    bucket,
    symbol,
    AVG("close") OVER (
        PARTITION BY symbol
        ORDER BY bucket
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS sma_7
FROM one_day_candle
WHERE symbol = 'BTC/USD'
ORDER BY bucket;
```

---

### 2. Rolling 7-Day Price Volatility (Standard Deviation)

**Purpose:**
Measure daily price volatility based on the high-low price range within the last 7 days.

**Key Details:**

* Calculates standard deviation of `high - low` using `STDDEV_POP()`
* Helps understand how much price fluctuates within a time window
* Uses same sliding window logic as SMA

**Query:**

```sql
SELECT
    bucket,
    symbol,
    STDDEV_POP(high - low) OVER (
        PARTITION BY symbol
        ORDER BY bucket
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS volatility_7
FROM one_day_candle
WHERE symbol = 'BTC/USD'
ORDER BY bucket;
```

---

### 3. Total Daily Trading Volume (Per Symbol or Globally)

**Purpose:**
Aggregate daily traded volume to track market activity per symbol or across all assets.

**Per Symbol (BTC/USD example):**

```sql
SELECT
    bucket,
    symbol,
    SUM(day_volume) AS total_volume
FROM one_day_candle
WHERE symbol = 'BTC/USD'
GROUP BY bucket, symbol
ORDER BY bucket;
```

**All Symbols Combined:**

```sql
SELECT
    bucket,
    SUM(day_volume) AS total_volume_all_symbols
FROM one_day_candle
GROUP BY bucket
ORDER BY bucket;
```

**Key Details:**

* Uses simple `SUM()` aggregation per time bucket
* For global totals, omit `symbol` from `GROUP BY`

---

### 4. Day-over-Day Percentage Price Change

**Purpose:**
Calculate the daily percentage change in closing price, showing market movement in relative terms.

**Key Details:**

* `LAG()` retrieves previous day's closing price
* Formula: `((current - previous) / previous) * 100`
* Rounded to 2 decimals for clarity

**Query:**

```sql
SELECT
    bucket,
    symbol,
    ROUND(
        100 * (
            ("close" - LAG("close") OVER (PARTITION BY symbol ORDER BY bucket))
            / LAG("close") OVER (PARTITION BY symbol ORDER BY bucket)
        )::numeric, 2
    ) AS pct_change
FROM one_day_candle
WHERE symbol = 'BTC/USD'
ORDER BY bucket;
```

---

### 5. Detect Days with Large Price Swings (High Price Range)

**Purpose:**
Identify days where the difference between the highest and lowest price exceeds a threshold, indicating high volatility.

**Key Details:**

* Calculates absolute price range as `high - low`
* Filters days with large swings (example: > 500 units)
* Threshold is adjustable based on asset price levels

**Query:**

```sql
SELECT
    bucket,
    symbol,
    high,
    low,
    ROUND((high - low)::numeric, 2) AS price_range
FROM one_day_candle
WHERE symbol = 'BTC/USD'
AND (high - low) > 500
ORDER BY price_range DESC;
```

---

### 6. Generate Custom Time Bucket Views (Hourly, Weekly, Monthly)

**Purpose:**
Aggregate price data at different time intervals to create OHLC views for varied analysis (e.g., intraday, weekly trends).

**Hourly OHLC Example:**

```sql
SELECT
    time_bucket('1 hour', time) AS bucket,
    symbol,
    FIRST(price, time) AS "open",
    MAX(price) AS high,
    MIN(price) AS low,
    LAST(price, time) AS "close"
FROM crypto_sample
WHERE symbol = 'BTC/USD'
GROUP BY bucket, symbol
ORDER BY bucket;
```

**Key Details:**

* `time_bucket()` groups data into fixed intervals
* Change `'1 hour'` to `'15 minutes'`, `'1 week'`, `'1 month'`, etc.
* Ideal for raw tables like `crypto_sample` — can also be materialized using continuous aggregates

---

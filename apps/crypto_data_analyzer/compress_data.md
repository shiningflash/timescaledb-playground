# 📦 Compress Time-Series Data with Hypercore (TimescaleDB Columnstore)

As your crypto datasets grow, efficiently storing and querying historical data becomes essential. TimescaleDB's **Hypercore** with native columnstore compression enables massive storage savings and query speed improvements.

---

## 🚀 Why Compress Data?

✅ Save significant disk space (up to **90x** compression possible)
✅ Improve analytical query performance by reducing memory footprint
✅ Retain full SQL compatibility with standard Postgres features

> **Note:** Compression ratio varies based on dataset size, distribution, and configuration.

---

# 🛠️ How Hypercore Compression Works

* Hypercore uses **native Postgres features**, no external storage formats required
* Data converts from row-oriented to column-oriented format
* Similar data stored adjacently improves compression efficiency
* Certain queries benefit from **block-level filtering and optimized ordering**

---

# ⚡ Step 1: Enable Compression for Historical Data

Connect to your TimescaleDB instance:

```sql
-- Enable compression with optimal settings
ALTER TABLE crypto_sample
SET (
    timescaledb.compress,
    timescaledb.compress_orderby = 'time DESC',
    timescaledb.compress_segmentby = 'symbol'
);
```

**Best Practices:**

* `compress_orderby = 'time DESC'` — optimizes time-based queries
* `compress_segmentby = 'symbol'` — groups data efficiently by crypto symbol

---

# 🔄 Step 2: Automate Compression with a Policy

Automatically compress chunks older than 1 day:

```sql
SELECT add_compression_policy('crypto_sample', INTERVAL '1 day');
```

Output:

```text
 add_compression_policy
------------------------
                   1003
(1 row)
```

✅ **Tip:** You can adjust the interval for your data retention needs.

---

# 🏗️ Step 3: Manually Convert Existing Chunks (Optional)

To compress already existing data immediately:

```sql
CALL convert_to_columnstore(c) FROM show_chunks('crypto_sample') c;
```

✅ This retroactively converts older chunks to columnstore format.

---

# 📏 Step 4: Compare Dataset Size Before and After Compression

```sql
SELECT
    pg_size_pretty(before_compression_total_bytes) AS before,
    pg_size_pretty(after_compression_total_bytes) AS after
FROM hypertable_columnstore_stats('crypto_sample');
```

### Example Output:

| before | after |
| ------ | ----- |
| 298 MB | 21 MB |

> 🔥 Massive space savings for historical tick data!

---

# ⚡ Step 5: Experience Query Performance Improvements

Running aggregated candlestick queries is now significantly faster:

```sql
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

✅ With compressed columnstore:

* Query time ≈ **15 ms**

❌ Without compression (rowstore):

* Query time ≈ **1 second**

---

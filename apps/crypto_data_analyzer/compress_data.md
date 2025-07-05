# Compress Time-Series Data with Hypercore (TimescaleDB Columnstore)

As your time-series datasets grow, efficiently storing and querying historical data becomes essential. TimescaleDB's **Hypercore**, powered by native **Columnstore Compression**, enables massive space savings and significant performance boosts — all while keeping full SQL compatibility.

---

## Why Compress Your Data?

- ✅ Save disk space — up to **90x compression**, depending on data type
- ✅ Improve query speed — less data read into memory
- ✅ Native Postgres experience — no extra tools or formats
- ✅ Ideal for **event-driven**, **financial**, or **IoT** time-series datasets

> ⚠️ Compression ratios vary based on your dataset's structure, types of columns, and configuration.

---

# How Hypercore Columnstore Compression Works

* Converts row-based storage into column-oriented format
* Groups similar data together to improve compressibility
* Uses standard Postgres storage structures under the hood
* Enables **block-level filtering** and **segment-based optimizations**
* Great for historical data that changes rarely or never

---

# Step 1: Enable Compression on Your Hypertable

Before using compression, you must define how TimescaleDB organizes the compressed chunks.

### Example for `crypto_sample` table:

```sql
ALTER TABLE crypto_sample
SET (
    timescaledb.compress,                            -- Enable compression
    timescaledb.compress_orderby = 'time DESC',      -- Sort by time (descending is common for recent-first queries)
    timescaledb.compress_segmentby = 'symbol'        -- Group data by symbol to improve query filtering
);
```

---

## **Understanding Parameters**

| Parameter              | Description                                             | Example                      |
| ---------------------- | ------------------------------------------------------- | ---------------------------- |
| `timescaledb.compress` | Enables compression for the table                       | `SET (timescaledb.compress)` |
| `compress_orderby`     | Sorts rows in chunks — improves ordered queries         | `'time DESC'`, `'time ASC'`  |
| `compress_segmentby`   | Groups similar data together for compression efficiency | `'symbol'`, `'device_id'`    |

**Best Practices:**

- ✔ Use `time DESC` for datasets queried from most-recent to oldest
- ✔ Segment by a high-cardinality column, like `symbol` or device identifier
- ✔ Adjust based on your data patterns

---

# Step 2: Automate Compression with a Retention Policy

A **compression policy** tells TimescaleDB to automatically compress chunks older than a defined interval.

### Example:

```sql
SELECT add_compression_policy('crypto_sample', INTERVAL '1 day');
```

This compresses chunks once they're **older than 1 day**.

---

## **Retention Policy Details**

| Parameter    | Description                                 | Example                            |
| ------------ | ------------------------------------------- | ---------------------------------- |
| `table_name` | The hypertable to apply the policy to       | `'crypto_sample'`                  |
| `INTERVAL`   | Age of chunks to compress (relative to now) | `'1 day'`, `'7 days'`, `'1 month'` |

**Other Possibilities:**

- ✔ Use larger intervals for critical recent data: `INTERVAL '30 days'` keeps last month uncompressed
- ✔ Combine with **data retention policies** to eventually drop old data:

```sql
SELECT add_retention_policy('crypto_sample', INTERVAL '90 days');
```

This keeps only 90 days of data, saving even more space.

---

# Step 3: Manually Compress Existing Chunks (Optional but Recommended)

The compression policy applies **moving forward**, but existing chunks remain uncompressed until manually processed.

### Manual Execution:

```sql
CALL convert_to_columnstore(c) FROM show_chunks('crypto_sample') c;
```

This compresses **all existing chunks** eligible under your policy.

You can also compress specific chunks:

```sql
CALL compress_chunk('_timescaledb_internal._hyper_1_5_chunk');
```

Get chunk names with:

```sql
SELECT show_chunks('crypto_sample');
```

---

# Step 4: Verify Compression Results

Compare table size before and after compression:

```sql
SELECT
    pg_size_pretty(before_compression_total_bytes) AS before,
    pg_size_pretty(after_compression_total_bytes) AS after
FROM hypertable_columnstore_stats('crypto_sample');
```

**Example Output:**

| before | after |
| ------ | ----- |
| 298 MB | 21 MB |

🔥 Massive storage savings for historical tick data!

---

# Step 5: Query with Performance Improvements

Compressed chunks reduce disk I/O and memory usage, speeding up analytical queries:

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

**Typical Results:**

| Storage Type | Query Time |
| ------------ | ---------- |
| Rowstore     | \~1 second |
| Columnstore  | \~15 ms    |

- ✅ Best for historical data that is queried often but rarely updated
- ✅ Real-time inserts stay in rowstore format until eligible for compression

---

# ⚙️ Additional Notes & Options

- ✔ Compression does **not** affect real-time inserts
- ✔ Chunks automatically decompress when updated
- ✔ Segment and ordering columns significantly impact efficiency — test based on query patterns
- ✔ Compression is reversible with:

```sql
CALL decompress_chunk('<chunk_name>');
```

---

# 💡 Summary

- ✅ Reduce storage costs dramatically
- ✅ Improve analytical query speeds, especially on historical data
- ✅ Combine compression with retention policies for maximum efficiency
- ✅ Fine-tune based on your data structure and access patterns

---

# What's Next

Return to [Analyze Financial Data](./analyze_data.md) to continue building real-time crypto insights with TimescaleDB.

---

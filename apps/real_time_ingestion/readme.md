# Real-Time Data Ingestion with TimescaleDB and Twelve Data

Stream and store real-time cryptocurrency and stock tick data directly into TimescaleDB using Python and WebSocket connections.

This project demonstrates:

* High-performance time-series ingestion with batching  
* Storing market data in TimescaleDB hypertables  
* Optimized hypertable creation with TimescaleDB Hypercore  
* Visualizing data with Grafana dashboards  

---

## Prerequisites

- Tiger Cloud or self-hosted TimescaleDB instance  
- API key from [Twelve Data](https://twelvedata.com/), and add it to `.env`.
- Python 3.8+  
- `psycopg2-binary`, `twelvedata`, `websocket-client`, `python-dotenv` 

---

## Setup Instructions

### 1. Database Table Setup

Connect to your TimescaleDB instance:

```bash
psql "postgresql://postgres:postgres@localhost:5432/timescale_practice"
```

Create hypertable for real-time tick data.

```sql
-- Hypertable for real-time tick data
CREATE TABLE crypto_ws_table (
    "time" TIMESTAMPTZ NOT NULL,  -- Exact timestamp of the price update
    symbol TEXT,                  -- Market symbol, e.g., BTC/USD
    price DOUBLE PRECISION,       -- Current price at that time
    day_volume NUMERIC NULL       -- 24-hour trading volume
) WITH (
   tsdb.hypertable,
   tsdb.partition_column = 'time',
   tsdb.segmentby = 'symbol',
   tsdb.orderby = 'time DESC'
);

-- Relational table for crypto asset metadata
CREATE TABLE crypto_assets (
    symbol TEXT UNIQUE,
    "name" TEXT
);
````

---

### 2. Python Environment Setup

In the project root:

```bash
cd apps/real_time_ingestion
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3. Configure the WebSocket Ingestor

Add the `.env` file. See `.env.sample` for more details.

---

### 4. Run the Ingestor

```bash
python websocket_ingestor.py
```

Expected output:

```
Current batch size: 23
Current batch size: 47
Batch insert #1
Current batch size: 12
...
```

Data will be inserted in batches for efficient storage.

---

## Grafana Integration

1. Log in to Grafana (e.g., [http://localhost:3000](http://localhost:3000))
2. Add TimescaleDB as a new PostgreSQL data source
3. Use connection details matching your TimescaleDB instance
4. Enable `TimescaleDB` option during configuration
5. Create dashboards to visualize webhook data

---

## Notes

- Batching improves ingestion speed and reduces overhead
- Hypertables automatically partition your time-series data
- Hypercore optimizes for both transactional and analytical workloads
- You can run separate scripts for different symbol groups (e.g., stocks, crypto)

---

## Troubleshooting

If you see errors like:

```
TDWebSocket ERROR: Handshake status 200 OK
```

- Double-check your Twelve Data API key
- Confirm TimescaleDB is reachable

---

## 📚 References

* [Twelve Data API](https://twelvedata.com/)
* [TimescaleDB Documentation](https://docs.timescale.com/)
* [Grafana Documentation](https://grafana.com/docs/grafana/latest/)

---

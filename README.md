<p align="center">
  <img src="./images/timescale_icon.svg" alt="TimescaleDB Logo" width="400"/>
</p>

# Timescaledb Playground

**A Practical TimescaleDB Playground**
Real-world projects, performance tuning, and fun experiments demonstrating how to effectively use **TimescaleDB** for time-series data, storage optimization, and real-time analytics.

---

## 🎯 Key Features

- ✅ Connection examples (local and cloud)
- ✅ Schema design following best practices
- ✅ Hypertables for efficient time-series storage
- ✅ Continuous aggregates for real-time analytics
- ✅ Compression and columnstore for space and speed improvements
- ✅ Grafana dashboards for interactive data visualization

---

# Apps Included

Explore experimentation-inspired, ready-to-use apps under the `apps/` directory.

---

## 1. **Crypto Data Analyzer** [`apps/crypto_data_analyzer`](./apps/crypto_data_analyzer)

A complete, step-by-step solution for storing, analyzing, compressing, and visualizing real-time cryptocurrency market data using TimescaleDB.

### ✨ What it Includes:

* ✔️ Tick-by-tick crypto trade data stored in optimized hypertables
* ✔️ TimescaleDB hyperfunctions for generating candlestick (OHLCV) metrics
* ✔️ Continuous aggregates for lightning-fast historical queries
* ✔️ Columnstore compression to reduce storage footprint dramatically
* ✔️ Beautiful Grafana dashboards for real-time visual insights

### 📚 Documentation:

* [Project Setup Guide](./apps/crypto_data_analyzer/README.md)
* [Analyze Financial Data](./apps/crypto_data_analyzer/analyze_data.md)
* [Compress Historical Data](./apps/crypto_data_analyzer/compress_data.md)

---

## 2. **Real-Time Ingestion Pipeline** [`apps/real_time_ingestion`](./apps/real_time_ingestion)

A real-time data pipeline that streams live cryptocurrency and stock price data from Twelve Data WebSocket API directly into TimescaleDB, optimized for high-ingest workloads.

### ✨ What it Includes:

* ✔️ Real-time price ingestion for crypto and stock symbols using WebSocket
* ✔️ Efficient batch inserts into TimescaleDB hypertables
* ✔️ Segmented and time-ordered storage for fast querying
* ✔️ Customizable batching strategy to maximize throughput
* ✔️ Logs for monitoring event flow, batch status, and connection health
* ✔️ Grafana integration for live dashboards on ingested data

### 📚 Documentation:

* [Real-Time Ingestion Setup Guide](./apps/real_time_ingestion/README.md)

---

# Apps Coming Soon

New apps demonstrating:

- 📦 IoT sensor data storage and querying
- 📦 Real-time energy monitoring with TimescaleDB
- 📦 Fun visualization projects using TimescaleDB with animations

Stay tuned for more hands-on projects!

---

# 🤝 Contributions Welcome

Suggestions, improvements, or new app ideas? Open a pull request or start a discussion to grow this TimescaleDB learning hub together.

---

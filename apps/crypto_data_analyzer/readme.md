# Crypto Data Analyzer with TimescaleDB

Leverage **TimescaleDB Hypertables** to efficiently store, analyze, and optimize real-time cryptocurrency tick data.

---

## Project Overview

This project demonstrates:

- ✅ High-performance storage of time-series crypto data using TimescaleDB
- ✅ Real-time query capabilities optimized for financial data
- ✅ Beautiful dashboards with Grafana for visual insights
- ✅ Practical compression techniques for historical data

---

# Quick Start Guide

## 1. Connect to Your TimescaleDB (Tiger Cloud or Local)

* **Option 1:** Use Tiger Cloud SQL Editor
* **Option 2:** Connect with `psql`:

```bash
psql "postgres://<username>:<password>@<host>:<port>/<database-name>"
```

---

## 2. Create the Hypertable for Real-Time Crypto Data

* Review the schema setup in:

```bash
apps/crypto_sample/schema_setup.sql
```

Run the SQL commands inside to create the optimized hypertable structure.

---

## 3. Load Financial Tick Data

* Download the dataset:

[🌐 Download Crypto Dataset (crypto\_sample.zip)](https://docs.tigerdata.com/tutorials/latest/financial-tick-data/financial-tick-dataset/)

* Extract the `.csv` files into your local project directory under `apps/crypto_sample/`

* Load the data using:

```sql
\COPY crypto_sample FROM 'apps/crypto_data_analyzer/crypto_sample/tutorial_sample_tick.csv' CSV HEADER;
\COPY company FROM 'apps/crypto_data_analyzer/crypto_sample/tutorial_sample_assets.csv' CSV HEADER;
```

**⚠️ Note:** Loading millions of rows may take several minutes, depending on system resources.

---

# 📊 Connect Grafana for Real-Time Dashboards

1. Open Grafana in your browser:

   * **Self-hosted:** [http://localhost:3000](http://localhost:3000)
     *(Default credentials: `admin` / `admin`)*

2. Add TimescaleDB as a new data source:

   * Go to: `Connections → Data Sources → Add new`
   * Select **PostgreSQL**
   * Configure with your TimescaleDB connection details:

```
Host: <host>:<port>
Database: <database-name>
Username: <username>
Password: <password>
```

* **TLS/SSL Mode:** `require`
* **PostgreSQL Options:** Enable `TimescaleDB`

3. Click `Save & Test` to confirm your connection is working.

---

# Dive into Financial Data Analysis

[🟢 **Analyze the Data Now** → `analyze_data.md`](./analyze_data.md)

> ⚡ **Highly Recommended:** Start querying and visualizing crypto market patterns with optimized SQL examples provided in the [analyze\_data.md](./analyze_data.md) file.

---

# Compress Historical Data for Optimal Performance

[🟢 **Compress Data Now** → `compress_data.md`](./compress_data.md)

> ⚡ **Highly Recommended:** Learn how to compress historical chunks using TimescaleDB’s built-in features for reduced storage and faster queries, detailed in [compress\_data.md](./compress_data.md).

---

# 🤝 Contributions & Improvements

Contributions welcome! Feel free to submit pull requests, ideas, or improvements to extend this project further.

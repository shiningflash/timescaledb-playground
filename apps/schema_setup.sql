-- Create crypto_sample table for time-series price and volume data
CREATE TABLE crypto_sample (
    time        TIMESTAMPTZ NOT NULL,           -- Timestamp of the event
    symbol      TEXT         NOT NULL,           -- Cryptocurrency symbol (e.g., BTC, ETH)
    price       DOUBLE PRECISION,                -- Price at that timestamp
    day_volume  BIGINT,                          -- Daily traded volume
    PRIMARY KEY (time, symbol)                  -- Composite Primary Key for uniqueness
);

-- Convert crypto_sample into a TimescaleDB hypertable
SELECT create_hypertable('crypto_sample', 'time');

-- Optimised index for querying by symbol and latest data
CREATE INDEX idx_crypto_symbol_time ON crypto_sample (symbol, time DESC);


-- Lookup table for company or crypto symbol details
CREATE TABLE company (
    symbol TEXT NOT NULL PRIMARY KEY,    -- Symbol (must be unique)
    name   TEXT NOT NULL                 -- Full company or cryptocurrency name
);

"""
WebSocket data ingestion pipeline for cryptocurrency and stock prices.

This script establishes a WebSocket connection with Twelve Data, receives real-time
market data, and stores batched events into a PostgreSQL-compatible TimescaleDB.

Environment Variables:
    DB_HOST (str): Database hostname.
    DB_PORT (str): Database port.
    DB_NAME (str): Database name.
    DB_USER (str): Database username.
    DB_PASS (str): Database password.
    TWELVE_DATA_SECRET_API_KEY (str): Twelve Data API key.

Raises:
    ValueError: If the API key is not found in the environment variables.

"""

import os
import time
from datetime import UTC, datetime
from typing import Any

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values
from twelvedata import TDClient

# Load environment variables
load_dotenv()


class WebsocketPipeline:
    """Handles WebSocket data ingestion and database batching."""

    DB_TABLE: str = "crypto_ws_table"
    DB_COLUMNS: tuple[str, ...] = ("time", "symbol", "price", "day_volume")
    MAX_BATCH_SIZE: int = 3

    def __init__(self, conn: psycopg2.extensions.connection, api_key: str) -> None:
        """
        Initialize the WebSocket pipeline.

        Args:
            conn: Active PostgreSQL database connection.
            api_key: API key for Twelve Data.

        """
        self.conn = conn
        self.api_key = api_key
        self.current_batch: list[tuple[Any, ...]] = []
        self.insert_counter: int = 0

    def _insert_values(self, data: list[tuple[Any, ...]]) -> None:
        """
        Insert batched records into the database.

        Args:
            data: List of tuples representing database rows to insert.

        """
        if self.conn and data:
            with self.conn.cursor() as cursor:
                columns = ",".join(self.DB_COLUMNS)
                sql = f"INSERT INTO {self.DB_TABLE} ({columns}) VALUES %s"
                execute_values(cursor, sql, data)
            self.conn.commit()

    def _on_event(self, event: dict[str, Any]) -> None:
        """
        Callback handler for WebSocket events.

        Args:
            event: Dictionary containing event data.

        """
        event_type = event.get("event")
        current_time = datetime.now(UTC)

        if event_type == "price":
            timestamp = datetime.fromtimestamp(event["timestamp"], tz=UTC)
            record = (
                timestamp,
                event["symbol"],
                event["price"],
                event.get("day_volume"),
            )
            self.current_batch.append(record)

            print(
                f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"{event['symbol']} | Price: {event['price']} | "
                f"Volume: {event.get('day_volume')} | "
                f"Batch Size: {len(self.current_batch)}",
            )

            if len(self.current_batch) >= self.MAX_BATCH_SIZE:
                self._insert_values(self.current_batch)
                self.insert_counter += 1
                print(
                    f"Batch Insert #{self.insert_counter} completed with "
                    f"{self.MAX_BATCH_SIZE} records.",
                )
                self.current_batch.clear()

        elif event_type == "heartbeat":
            print(f"Heartbeat received at {current_time.strftime('%H:%M:%S')}")
        else:
            print(f"Received unrecognized event '{event_type}', ignoring...")

    def start(self, symbols: list[str]) -> None:
        """
        Start the WebSocket stream and handle incoming events.

        Args:
            symbols: List of asset symbols to subscribe to.

        """
        print(f"Connecting to Twelve Data WebSocket for symbols: {symbols}")
        td = TDClient(apikey=self.api_key)
        ws = td.websocket(on_event=self._on_event)

        ws.subscribe(symbols)
        ws.connect()

        try:
            while True:
                ws.heartbeat()
                print(
                    f"Heartbeat sent at {datetime.now(UTC).strftime('%H:%M:%S')}",
                )
                time.sleep(10)
        except KeyboardInterrupt:
            print("WebSocket connection interrupted by user.")


def get_database_connection() -> psycopg2.extensions.connection:
    """
    Establish a connection to the PostgreSQL database.

    Returns:
        A PostgreSQL database connection object.

    Raises:
        ValueError: If required database credentials are missing.

    """
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "timescale_practice")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "postgres")

    return psycopg2.connect(
        database=db_name,
        host=db_host,
        user=db_user,
        password=db_pass,
        port=db_port,
    )


def get_api_key() -> str:
    """
    Retrieve the Twelve Data API key from environment variables.

    Returns:
        API key as a string.

    Raises:
        ValueError: If the API key is not found.

    """
    api_key = os.getenv("TWELVE_DATA_SECRET_API_KEY")
    if not api_key:
        raise ValueError("Missing Twelve Data API Key in .env")
    return api_key


if __name__ == "__main__":
    connection = get_database_connection()
    api_key = get_api_key()

    subscribed_symbols = ["BTC/USD", "ETH/USD", "MSFT", "AAPL"]
    pipeline = WebsocketPipeline(conn=connection, api_key=api_key)
    pipeline.start(symbols=subscribed_symbols)

import time
import os
import psycopg2

from twelvedata import TDClient
from psycopg2.extras import execute_values
from datetime import datetime
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class WebsocketPipeline:
    DB_TABLE = "crypto_ws_table"
    DB_COLUMNS = ["time", "symbol", "price", "day_volume"]
    MAX_BATCH_SIZE = 3

    def __init__(self, conn, api_key):
        self.conn = conn
        self.api_key = api_key
        self.current_batch = []
        self.insert_counter = 0

    def _insert_values(self, data):
        if self.conn:
            with self.conn.cursor() as cursor:
                sql = f"""
                INSERT INTO {self.DB_TABLE} ({','.join(self.DB_COLUMNS)})
                VALUES %s;
                """
                execute_values(cursor, sql, data)
            self.conn.commit()

    def _on_event(self, event):
        if event.get("event") == "price":
            timestamp = datetime.utcfromtimestamp(event["timestamp"])
            readable_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            record = (
                timestamp,
                event["symbol"],
                event["price"],
                event.get("day_volume")
            )
            self.current_batch.append(record)

            # Preview event details
            print(f"[{readable_time}] {event['symbol']} | Price: {event['price']} | Volume: {event.get('day_volume')} | Batch Size: {len(self.current_batch)}")

            if len(self.current_batch) >= self.MAX_BATCH_SIZE:
                self._insert_values(self.current_batch)
                self.insert_counter += 1
                print(f"Batch Insert #{self.insert_counter} completed with {self.MAX_BATCH_SIZE} records.")
                self.current_batch.clear()

        elif event.get("event") == "heartbeat":
            print(f"Heartbeat received at {datetime.utcnow().strftime('%H:%M:%S')}")

        else:
            print(f"Received event: {event.get('event')}, ignoring...")

    def start(self, symbols):
        print(f"Connecting to Twelve Data WebSocket for symbols: {symbols}")
        td = TDClient(apikey=self.api_key)
        ws = td.websocket(on_event=self._on_event)
        ws.subscribe(symbols)
        ws.connect()

        while True:
            ws.heartbeat()
            print(f"Heartbeat sent at {datetime.utcnow().strftime('%H:%M:%S')}")
            time.sleep(10)


if __name__ == "__main__":
    # Load config from .env
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "timescale_practice")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "postgres")
    API_KEY = os.getenv("TWELVE_DATA_SECRET_API_KEY")

    if not API_KEY:
        raise ValueError("Missing Twelve Data API Key in .env")

    conn = psycopg2.connect(
        database=DB_NAME,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

    symbols = ["BTC/USD", "ETH/USD", "MSFT", "AAPL"]
    pipeline = WebsocketPipeline(conn, api_key=API_KEY)
    pipeline.start(symbols=symbols)

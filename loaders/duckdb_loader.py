import os
import duckdb
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

DUCKDB_PATH = os.getenv("DUCKDB_PATH", "data/crypto.duckdb")


def get_connection() -> duckdb.DuckDBPyConnection:
    """
    Returns a connection to the DuckDB database.
    Creates the file if it doesn't exist.
    """
    return duckdb.connect(DUCKDB_PATH)


def create_raw_table(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Creates the raw coins table if it doesn't exist.
    This is the landing zone — data exactly as it comes from the API.
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_coin_prices (
            id                      VARCHAR,
            symbol                  VARCHAR,
            name                    VARCHAR,
            current_price           DOUBLE,
            market_cap              DOUBLE,
            market_cap_rank         INTEGER,
            total_volume            DOUBLE,
            high_24h                DOUBLE,
            low_24h                 DOUBLE,
            price_change_24h        DOUBLE,
            price_change_pct_24h    DOUBLE,
            price_change_pct_7d     DOUBLE,
            price_change_pct_30d    DOUBLE,
            circulating_supply      DOUBLE,
            total_supply            DOUBLE,
            extracted_at            TIMESTAMP
        )
    """)


def load_coins(coins: list[dict]) -> int:
    """
    Loads raw coin data into DuckDB.
    Returns the number of records inserted.
    """
    extracted_at = datetime.now(timezone.utc)
    conn = get_connection()
    create_raw_table(conn)

    records = []
    for coin in coins:
        records.append((
            coin.get("id"),
            coin.get("symbol"),
            coin.get("name"),
            coin.get("current_price"),
            coin.get("market_cap"),
            coin.get("market_cap_rank"),
            coin.get("total_volume"),
            coin.get("high_24h"),
            coin.get("low_24h"),
            coin.get("price_change_24h"),
            coin.get("price_change_percentage_24h"),
            coin.get("price_change_percentage_7d_in_currency"),
            coin.get("price_change_percentage_30d_in_currency"),
            coin.get("circulating_supply"),
            coin.get("total_supply"),
            extracted_at
        ))

    conn.executemany("""
        INSERT INTO raw_coin_prices VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, records)

    conn.close()
    return len(records)


if __name__ == "__main__":
    from extractors.coingecko import extract_coins

    coins = extract_coins()
    inserted = load_coins(coins)
    print(f"Inserted {inserted} records into DuckDB.")

    conn = get_connection()
    result = conn.execute("""
        SELECT symbol, current_price, market_cap_rank, extracted_at
        FROM raw_coin_prices
        ORDER BY market_cap_rank
        LIMIT 5
    """).fetchall()
    conn.close()

    print("\nTop 5 coins in database:")
    for row in result:
        print(f"  {row[0].upper()} | ${row[1]:,.2f} | Rank #{row[2]} | {row[3]}")
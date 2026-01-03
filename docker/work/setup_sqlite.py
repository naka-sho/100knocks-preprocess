#!/usr/bin/env python3
"""
Setup script to create SQLite database from CSV files.
This script creates a SQLite database with the same schema as PostgreSQL
and loads all CSV data into it.
"""

import sqlite3
import csv
import os
from pathlib import Path

# Database file path
DB_PATH = Path(__file__).parent / "dsdojo.db"
DATA_DIR = Path(__file__).parent / "data"

def create_tables(conn):
    """Create all tables with schema compatible with SQLite."""
    cursor = conn.cursor()
    
    # Drop existing tables if they exist
    tables = ['customer', 'category', 'product', 'store', 'receipt', 'geocode']
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    
    # Customer table
    cursor.execute("""
        CREATE TABLE customer(
            customer_id            TEXT PRIMARY KEY,
            customer_name          TEXT,
            gender_cd              TEXT,
            gender                 TEXT,
            birth_day              TEXT,
            age                    INTEGER,
            postal_cd              TEXT,
            address                TEXT,
            application_store_cd   TEXT,
            application_date       TEXT,
            status_cd              TEXT
        )
    """)
    
    # Category table
    cursor.execute("""
        CREATE TABLE category(
            category_major_cd     TEXT,
            category_major_name   TEXT,
            category_medium_cd    TEXT,
            category_medium_name  TEXT,
            category_small_cd     TEXT PRIMARY KEY,
            category_small_name   TEXT
        )
    """)
    
    # Product table
    cursor.execute("""
        CREATE TABLE product(
            product_cd            TEXT PRIMARY KEY,
            category_major_cd     TEXT,
            category_medium_cd    TEXT,
            category_small_cd     TEXT,
            unit_price            INTEGER,
            unit_cost             INTEGER
        )
    """)
    
    # Store table
    cursor.execute("""
        CREATE TABLE store(
            store_cd      TEXT PRIMARY KEY,
            store_name    TEXT,
            prefecture_cd TEXT,
            prefecture    TEXT,
            address       TEXT,
            address_kana  TEXT,
            tel_no        TEXT,
            longitude     REAL,
            latitude      REAL,
            floor_area    REAL
        )
    """)
    
    # Receipt table
    cursor.execute("""
        CREATE TABLE receipt(
            sales_ymd       INTEGER,
            sales_epoch     INTEGER,
            store_cd        TEXT,
            receipt_no      INTEGER,
            receipt_sub_no  INTEGER,
            customer_id     TEXT,
            product_cd      TEXT,
            quantity        INTEGER,
            amount          INTEGER,
            PRIMARY KEY (sales_ymd, store_cd, receipt_no, receipt_sub_no)
        )
    """)
    
    # Geocode table
    cursor.execute("""
        CREATE TABLE geocode(
            postal_cd       TEXT,
            prefecture      TEXT,
            city            TEXT,
            town            TEXT,
            street          TEXT,
            address         TEXT,
            full_address    TEXT,
            longitude       REAL,
            latitude        REAL
        )
    """)
    
    conn.commit()
    print("✓ Tables created successfully")

def load_csv_data(conn, table_name, csv_file):
    """Load data from CSV file into specified table."""
    cursor = conn.cursor()
    
    if not csv_file.exists():
        print(f"Warning: {csv_file} not found, skipping...")
        return
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip header row
        
        # Create placeholder string for SQL
        placeholders = ','.join(['?' for _ in headers])
        
        # Insert data
        row_count = 0
        for row in reader:
            cursor.execute(
                f"INSERT INTO {table_name} VALUES ({placeholders})",
                row
            )
            row_count += 1
        
        conn.commit()
        print(f"✓ Loaded {row_count} rows into {table_name}")

def main():
    """Main function to setup SQLite database."""
    print("Setting up SQLite database for Data Science 100 Knocks...")
    print(f"Database path: {DB_PATH}")
    print(f"Data directory: {DATA_DIR}")
    
    # Remove existing database if it exists
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("✓ Removed existing database")
    
    # Create connection
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Create tables
        print("\nCreating tables...")
        create_tables(conn)
        
        # Load data from CSV files
        print("\nLoading data from CSV files...")
        tables = ['customer', 'category', 'product', 'receipt', 'store', 'geocode']
        for table in tables:
            csv_file = DATA_DIR / f"{table}.csv"
            load_csv_data(conn, table, csv_file)
        
        print(f"\n✓ SQLite database created successfully: {DB_PATH}")
        print(f"  Database size: {DB_PATH.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Show table counts
        print("\nTable row counts:")
        cursor = conn.cursor()
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count:,} rows")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()

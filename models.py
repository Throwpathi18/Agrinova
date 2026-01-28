import sqlite3
import os

DB_PATH = 'farmer_app.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Markets Table
    c.execute('''CREATE TABLE IF NOT EXISTS markets
                 (id INTEGER PRIMARY KEY, name TEXT, lat REAL, lon REAL, contact TEXT)''')
    
    # Schemes Table
    c.execute('''CREATE TABLE IF NOT EXISTS schemes
                 (id INTEGER PRIMARY KEY, name TEXT, category TEXT, benefit TEXT, link TEXT)''')
    
    # Seed Data
    c.execute("DELETE FROM markets")
    markets = [
        ('Central Grain Market', 28.6139, 77.2090, '+91-9876543210'),
        ('Rural Farmers Hub', 28.7041, 77.1025, '+91-9988776655'),
        ('West Side Mandi', 19.0760, 72.8777, '+91-9000011122')
    ]
    c.executemany("INSERT INTO markets (name, lat, lon, contact) VALUES (?,?,?,?)", markets)
    
    c.execute("DELETE FROM schemes")
    schemes = [
        ('PM-Kisan Samman Nidhi', 'Income Support', '₹6,000 per year in 3 installments', 'https://pmkisan.gov.in/'),
        ('Fasal Bima Yojana', 'Insurance', 'Low premium insurance for crop loss', 'https://pmfby.gov.in/'),
        ('Kisan Credit Card', 'Credit', 'Low interest loans for farming needs', 'https://www.myscheme.gov.in/')
    ]
    c.executemany("INSERT INTO schemes (name, category, benefit, link) VALUES (?,?,?,?)", schemes)
    
    conn.commit()
    conn.close()

def get_markets():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    markets = conn.execute("SELECT * FROM markets").fetchall()
    conn.close()
    return [dict(m) for m in markets]

def get_schemes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    schemes = conn.execute("SELECT * FROM schemes").fetchall()
    conn.close()
    return [dict(s) for s in schemes]

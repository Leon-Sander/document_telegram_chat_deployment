import sqlite3
from utils import load_config

config = load_config()

def init_db():
    conn = sqlite3.connect(config['sqlite']['db_path'])
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_tokens INTEGER,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_cost REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_telemetry(total_tokens, prompt_tokens, completion_tokens, total_cost):
    conn = sqlite3.connect(config['sqlite']['db_path'])
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO telemetry (total_tokens, prompt_tokens, completion_tokens, total_cost)
        VALUES (?, ?, ?, ?)
    ''', (total_tokens, prompt_tokens, completion_tokens, total_cost))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
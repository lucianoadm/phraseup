# utils/db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("data/phraseup.db")
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """Inicializa e faz migração se necessário"""
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se a tabela existe
    cursor.execute("PRAGMA table_info(history)")
    existing_columns = [col[1] for col in cursor.fetchall()]

    if not existing_columns:
        # Tabela nova
        cursor.executescript("""
            CREATE TABLE history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT NOT NULL,
                output_text TEXT NOT NULL,
                level TEXT,
                created_at TEXT DEFAULT (datetime('now','localtime'))
            );
        """)
        print("✅ Tabela 'history' criada com sucesso!")

    elif "input_text" not in existing_columns:
        # Migração da tabela antiga
        print("🔄 Migrando tabela history (adicionando colunas novas)...")
        cursor.execute("ALTER TABLE history RENAME TO history_old")
        
        cursor.executescript("""
            CREATE TABLE history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT NOT NULL,
                output_text TEXT NOT NULL,
                level TEXT,
                created_at TEXT DEFAULT (datetime('now','localtime'))
            );
            
            INSERT INTO history (input_text, output_text, level, created_at)
            SELECT input_text, output_text, level, created_at FROM history_old;
            
            DROP TABLE history_old;
        """)
        print("✅ Migração concluída!")
    else:
        print("✅ Tabela history já está atualizada.")

    conn.commit()
    conn.close()


def save_history(input_text: str, output_text: str, level: str = "normal"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (input_text, output_text, level, created_at)
        VALUES (?, ?, ?, datetime('now','localtime'))
    """, (input_text, output_text, level))
    conn.commit()
    conn.close()


def get_history(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT input_text, output_text, level, created_at
        FROM history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    data = cursor.fetchall()
    conn.close()
    return data


def clear_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()


# 🔥 NOVAS FUNÇÕES PARA A ABA LIBRARY
def get_library(limit: int = 100):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, input_text, output_text, level, created_at
        FROM history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    data = cursor.fetchall()
    conn.close()
    return data


def delete_from_library(item_id: int):
    """Remove um item específico da biblioteca pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
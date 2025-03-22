import sqlite3


class Database:
    def __init__(self, db_path="documents.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT UNIQUE,
                file_name TEXT,
                file_path TEXT
            )
        """)
        self.conn.commit()

    def insert_document(self, file_id, file_name, file_path):
        try:
            self.cursor.execute("INSERT INTO documents (file_id, file_name, file_path) VALUES (?, ?, ?)",
                                (file_id, file_name, file_path))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def document_exists(self, file_id):
        self.cursor.execute("SELECT 1 FROM documents WHERE file_id = ?", (file_id,))
        return self.cursor.fetchone() is not None

    def get_all_file_names(self):
        self.cursor.execute("SELECT file_name FROM documents")
        return [row[0] for row in self.cursor.fetchall()]

    def get_file_path(self, file_name):
        self.cursor.execute("SELECT file_path FROM documents WHERE file_name = ?", (file_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.conn.close()

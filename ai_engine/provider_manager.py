import sqlite3
from backend.config import DATABASE_PATH

class ProviderManager:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path

    def get_active_providers(self):
        """Fetches active providers from the database, ordered by success rate and latency."""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                SELECT id, endpoint, provider, success_rate, latency
                FROM apis
                WHERE status = 'active'
                ORDER BY success_rate DESC, latency ASC
            """)
            providers = [
                {
                    "id": row[0],
                    "endpoint": row[1],
                    "name": row[2],
                    "success_rate": row[3],
                    "latency": row[4]
                }
                for row in c.fetchall()
            ]
            conn.close()
            return providers
        except Exception as e:
            print(f"❌ Error fetching active providers: {e}")
            return []

    def update_provider_stats(self, provider_id, success, latency):
        """Updates the success rate and latency of a provider."""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            # Calculate new success rate (simple moving average for now)
            c.execute("SELECT success_rate FROM apis WHERE id = ?", (provider_id,))
            row = c.fetchone()
            if row:
                old_rate = row[0]
                new_rate = (old_rate * 0.9) + (0.1 if success else 0.0)

                c.execute("""
                    UPDATE apis
                    SET success_rate = ?, latency = ?, last_checked = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (new_rate, latency, provider_id))
                conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Error updating provider stats: {e}")

    def deactivate_provider(self, provider_id):
        """Marks a provider as inactive."""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("UPDATE apis SET status = 'inactive' WHERE id = ?", (provider_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Error deactivating provider: {e}")


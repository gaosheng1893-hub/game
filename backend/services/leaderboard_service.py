from common.database import get_db_connection

class LeaderboardService:
    @staticmethod
    def get_leaderboard(limit: int = 10):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT u.id, u.username, u.total_score, u.completed_stations,
                   ROW_NUMBER() OVER (ORDER BY u.total_score DESC) as ranking
            FROM users u
            WHERE u.total_score > 0
            ORDER BY u.total_score DESC
            LIMIT %s
        """, (limit,))
        
        leaderboard = cursor.fetchall()
        connection.close()
        
        return leaderboard

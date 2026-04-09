from fastapi import HTTPException
from common.database import get_db_connection
from services.achievement_service import AchievementService

class ProgressService:
    @staticmethod
    def get_user_progress(user_id: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM user_progress WHERE user_id = %s", (user_id,))
        progress = cursor.fetchall()
        connection.close()
        
        return progress
    
    @staticmethod
    def submit_answer(user_id: int, station_id: int, question_id: int, answer: str):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # 获取正确答案
        cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
        question = cursor.fetchone()
        
        if not question:
            connection.close()
            raise HTTPException(status_code=404, detail="问题不存在")
        
        is_correct = answer == question['correct_answer']
        score = question['score'] if is_correct else 0
        
        # 更新用户进度
        cursor.execute("""
            INSERT INTO user_progress (user_id, station_id, completed, score, created_at)
            VALUES (%s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE
            completed = %s,
            score = GREATEST(score, %s),
            updated_at = NOW()
        """, (user_id, station_id, is_correct, score, is_correct, score))
        
        # 更新用户总分和完成站点数
        cursor.execute("""
            UPDATE users 
            SET total_score = (SELECT COALESCE(SUM(score), 0) FROM user_progress WHERE user_id = %s),
                completed_stations = (SELECT COUNT(*) FROM user_progress WHERE user_id = %s AND completed = TRUE)
            WHERE id = %s
        """, (user_id, user_id, user_id))
        
        # 更新排行榜
        cursor.execute("""
            INSERT INTO leaderboard (user_id, score, ranking)
            VALUES (%s, (SELECT total_score FROM users WHERE id = %s), 0)
            ON DUPLICATE KEY UPDATE
            score = (SELECT total_score FROM users WHERE id = %s)
        """, (user_id, user_id, user_id))
        
        # 检查成就
        new_achievements = AchievementService.check_achievements(user_id, connection, cursor)
        
        connection.commit()
        connection.close()
        
        return {"is_correct": is_correct, "score": score, "new_achievements": new_achievements}

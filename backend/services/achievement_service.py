from common.database import get_db_connection

class AchievementService:
    @staticmethod
    def check_achievements(user_id: int, connection, cursor):
        # 获取用户统计信息
        cursor.execute("SELECT total_score, completed_stations FROM users WHERE id = %s", (user_id,))
        user_stats = cursor.fetchone()
        
        # 获取正确答题数
        cursor.execute("SELECT COUNT(*) as count FROM user_progress WHERE user_id = %s AND completed = TRUE", (user_id,))
        correct_answers = cursor.fetchone()['count']
        
        # 计算正确率
        cursor.execute("SELECT COUNT(*) as count FROM user_progress WHERE user_id = %s", (user_id,))
        total_answers = cursor.fetchone()['count']
        accuracy = (correct_answers / total_answers * 100) if total_answers > 0 else 0
        
        # 检查各种成就条件
        achievements_to_unlock = []
        new_achievements = []
        
        cursor.execute("SELECT * FROM achievements")
        achievements = cursor.fetchall()
        
        for achievement in achievements:
            # 检查是否已经获得该成就
            cursor.execute(
                "SELECT * FROM user_achievements WHERE user_id = %s AND achievement_id = %s",
                (user_id, achievement['id'])
            )
            if cursor.fetchone():
                continue
            
            # 检查成就条件
            should_unlock = False
            if achievement['condition_type'] == 'completed_stations' and user_stats['completed_stations'] >= achievement['condition_value']:
                should_unlock = True
            elif achievement['condition_type'] == 'score' and user_stats['total_score'] >= achievement['condition_value']:
                should_unlock = True
            elif achievement['condition_type'] == 'accuracy' and accuracy >= achievement['condition_value']:
                should_unlock = True
            
            if should_unlock:
                achievements_to_unlock.append(achievement['id'])
                new_achievements.append(achievement)
        
        # 解锁成就
        for achievement_id in achievements_to_unlock:
            cursor.execute(
                "INSERT INTO user_achievements (user_id, achievement_id, obtained_at) VALUES (%s, %s, NOW())",
                (user_id, achievement_id)
            )
        
        return new_achievements
    
    @staticmethod
    def get_user_achievements(user_id: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT a.*, ua.obtained_at 
            FROM achievements a
            LEFT JOIN user_achievements ua ON a.id = ua.achievement_id AND ua.user_id = %s
            ORDER BY a.id
        """, (user_id,))
        
        achievements = cursor.fetchall()
        connection.close()
        
        return achievements

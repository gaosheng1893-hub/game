from fastapi import HTTPException
from common.database import get_db_connection
import bcrypt

class AdminService:
    # 站点管理
    @staticmethod
    def get_all_stations():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM stations ORDER BY position")
        stations = cursor.fetchall()
        connection.close()
        return stations
    
    @staticmethod
    def create_station(name: str, content: str, position: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # 检查位置是否已存在
        cursor.execute("SELECT * FROM stations WHERE position = %s", (position,))
        if cursor.fetchone():
            connection.close()
            raise HTTPException(status_code=400, detail="该位置已存在站点")
        # 检查位置是否为正整数
        if not isinstance(position, int) or position <= 0:
            connection.close()
            raise HTTPException(status_code=400, detail="位置必须是正整数")
        cursor.execute("INSERT INTO stations (name, content, position) VALUES (%s, %s, %s)", (name, content, position))
        connection.commit()
        station_id = cursor.lastrowid
        cursor.execute("SELECT * FROM stations WHERE id = %s", (station_id,))
        station = cursor.fetchone()
        connection.close()
        return station
    
    @staticmethod
    def update_station(station_id: int, name: str, content: str, position: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # 检查位置是否已被其他站点使用
        cursor.execute("SELECT * FROM stations WHERE position = %s AND id != %s", (position, station_id))
        if cursor.fetchone():
            connection.close()
            raise HTTPException(status_code=400, detail="该位置已被其他站点使用")
        # 检查位置是否为正整数
        if not isinstance(position, int) or position <= 0:
            connection.close()
            raise HTTPException(status_code=400, detail="位置必须是正整数")
        cursor.execute("UPDATE stations SET name = %s, content = %s, position = %s WHERE id = %s", (name, content, position, station_id))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="站点不存在")
        cursor.execute("SELECT * FROM stations WHERE id = %s", (station_id,))
        station = cursor.fetchone()
        connection.close()
        return station
    
    @staticmethod
    def delete_station(station_id: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM stations WHERE id = %s", (station_id,))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="站点不存在")
        connection.close()
        return {"message": "站点删除成功"}
    
    # 问题管理
    @staticmethod
    def get_all_questions():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT q.*, s.name as station_name FROM questions q JOIN stations s ON q.station_id = s.id")
        questions = cursor.fetchall()
        connection.close()
        return questions
    
    @staticmethod
    def create_question(station_id: int, question: str, option_a: str, option_b: str, option_c: str, option_d: str, correct_answer: str, score: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # 检查该站点是否已存在相同问题
        cursor.execute("SELECT * FROM questions WHERE station_id = %s AND question = %s", (station_id, question))
        if cursor.fetchone():
            connection.close()
            raise HTTPException(status_code=400, detail="该站点已存在相同问题")
        cursor.execute("INSERT INTO questions (station_id, question, option_a, option_b, option_c, option_d, correct_answer, score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (station_id, question, option_a, option_b, option_c, option_d, correct_answer, score))
        connection.commit()
        question_id = cursor.lastrowid
        cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
        question = cursor.fetchone()
        connection.close()
        return question
    
    @staticmethod
    def update_question(question_id: int, question: str, option_a: str, option_b: str, option_c: str, option_d: str, correct_answer: str, score: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # 获取当前问题的站点ID
        cursor.execute("SELECT station_id FROM questions WHERE id = %s", (question_id,))
        current_question = cursor.fetchone()
        if not current_question:
            connection.close()
            raise HTTPException(status_code=404, detail="问题不存在")
        station_id = current_question['station_id']
        # 检查该站点是否已存在相同问题（排除当前问题）
        cursor.execute("SELECT * FROM questions WHERE station_id = %s AND question = %s AND id != %s", (station_id, question, question_id))
        if cursor.fetchone():
            connection.close()
            raise HTTPException(status_code=400, detail="该站点已存在相同问题")
        cursor.execute("UPDATE questions SET question = %s, option_a = %s, option_b = %s, option_c = %s, option_d = %s, correct_answer = %s, score = %s WHERE id = %s", (question, option_a, option_b, option_c, option_d, correct_answer, score, question_id))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="问题不存在")
        cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
        question = cursor.fetchone()
        connection.close()
        return question
    
    @staticmethod
    def delete_question(question_id: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM questions WHERE id = %s", (question_id,))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="问题不存在")
        connection.close()
        return {"message": "问题删除成功"}
    
    # 成就管理
    @staticmethod
    def get_all_achievements():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM achievements")
        achievements = cursor.fetchall()
        connection.close()
        return achievements
    
    @staticmethod
    def create_achievement(name: str, description: str, icon: str, condition_type: str, condition_value: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("INSERT INTO achievements (name, description, icon, condition_type, condition_value) VALUES (%s, %s, %s, %s, %s)", (name, description, icon, condition_type, condition_value))
        connection.commit()
        achievement_id = cursor.lastrowid
        cursor.execute("SELECT * FROM achievements WHERE id = %s", (achievement_id,))
        achievement = cursor.fetchone()
        connection.close()
        return achievement
    
    @staticmethod
    def update_achievement(achievement_id: int, name: str, description: str, icon: str, condition_type: str, condition_value: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("UPDATE achievements SET name = %s, description = %s, icon = %s, condition_type = %s, condition_value = %s WHERE id = %s", (name, description, icon, condition_type, condition_value, achievement_id))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="成就不存在")
        cursor.execute("SELECT * FROM achievements WHERE id = %s", (achievement_id,))
        achievement = cursor.fetchone()
        connection.close()
        return achievement
    
    @staticmethod
    def delete_achievement(achievement_id: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM achievements WHERE id = %s", (achievement_id,))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="成就不存在")
        connection.close()
        return {"message": "成就删除成功"}
    
    # 奖品管理
    @staticmethod
    def get_all_lottery_records():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT l.*, u.username FROM lottery l JOIN users u ON l.user_id = u.id ORDER BY l.created_at DESC")
        records = cursor.fetchall()
        connection.close()
        return records
    
    @staticmethod
    def get_winners():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT l.*, u.username FROM lottery l JOIN users u ON l.user_id = u.id WHERE l.winner = TRUE ORDER BY l.created_at DESC")
        winners = cursor.fetchall()
        connection.close()
        return winners
    
    @staticmethod
    def set_winner(lottery_id: int, prize: str):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("UPDATE lottery SET winner = TRUE, prize = %s WHERE id = %s", (prize, lottery_id))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="抽奖记录不存在")
        cursor.execute("SELECT * FROM lottery WHERE id = %s", (lottery_id,))
        record = cursor.fetchone()
        connection.close()
        return record
    
    # 奖品级别管理
    @staticmethod
    def get_all_prizes():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prizes ORDER BY level ASC")
        prizes = cursor.fetchall()
        connection.close()
        return prizes
    
    @staticmethod
    def create_prize(name: str, level: int, probability: float, description: str):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # 检查奖品级别是否已存在
        cursor.execute("SELECT * FROM prizes WHERE level = %s", (level,))
        if cursor.fetchone():
            connection.close()
            raise HTTPException(status_code=400, detail="该奖品级别已存在")
        # 检查奖品级别是否在有效范围内
        if not isinstance(level, int) or level < 1 or level > 5:
            connection.close()
            raise HTTPException(status_code=400, detail="奖品级别必须是1-5之间的整数")
        # 检查概率是否在有效范围内
        if not isinstance(probability, (int, float)) or probability < 0 or probability > 1:
            connection.close()
            raise HTTPException(status_code=400, detail="概率必须是0-1之间的数值")
        cursor.execute("INSERT INTO prizes (name, level, probability, description) VALUES (%s, %s, %s, %s)", (name, level, probability, description))
        connection.commit()
        prize_id = cursor.lastrowid
        cursor.execute("SELECT * FROM prizes WHERE id = %s", (prize_id,))
        prize = cursor.fetchone()
        connection.close()
        return prize
    
    @staticmethod
    def update_prize(prize_id: int, name: str, level: int, probability: float, description: str):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # 检查奖品级别是否已被其他奖品使用
        cursor.execute("SELECT * FROM prizes WHERE level = %s AND id != %s", (level, prize_id))
        if cursor.fetchone():
            connection.close()
            raise HTTPException(status_code=400, detail="该奖品级别已被其他奖品使用")
        # 检查奖品级别是否在有效范围内
        if not isinstance(level, int) or level < 1 or level > 5:
            connection.close()
            raise HTTPException(status_code=400, detail="奖品级别必须是1-5之间的整数")
        # 检查概率是否在有效范围内
        if not isinstance(probability, (int, float)) or probability < 0 or probability > 1:
            connection.close()
            raise HTTPException(status_code=400, detail="概率必须是0-1之间的数值")
        cursor.execute("UPDATE prizes SET name = %s, level = %s, probability = %s, description = %s WHERE id = %s", (name, level, probability, description, prize_id))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="奖品不存在")
        cursor.execute("SELECT * FROM prizes WHERE id = %s", (prize_id,))
        prize = cursor.fetchone()
        connection.close()
        return prize
    
    @staticmethod
    def delete_prize(prize_id: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM prizes WHERE id = %s", (prize_id,))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="奖品不存在")
        connection.close()
        return {"message": "奖品删除成功"}
    
    # 用户管理
    @staticmethod
    def get_all_users():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email, total_score, completed_stations, created_at FROM users")
        users = cursor.fetchall()
        connection.close()
        return users
    
    @staticmethod
    def create_user(username: str, email: str, password: str):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        connection.commit()
        user_id = cursor.lastrowid
        cursor.execute("SELECT id, username, email, total_score, completed_stations, created_at FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        connection.close()
        return user
    
    @staticmethod
    def update_user(user_id: int, username: str, email: str, password: str):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s", (username, email, hashed_password, user_id))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="用户不存在")
        cursor.execute("SELECT id, username, email, total_score, completed_stations, created_at FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        connection.close()
        return user
    
    @staticmethod
    def delete_user(user_id: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()
        if cursor.rowcount == 0:
            connection.close()
            raise HTTPException(status_code=404, detail="用户不存在")
        connection.close()
        return {"message": "用户删除成功"}

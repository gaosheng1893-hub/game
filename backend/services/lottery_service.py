import random
from fastapi import HTTPException
from common.database import get_db_connection

class LotteryService:
    @staticmethod
    def perform_lottery(user_id: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # 检查用户是否已经抽过奖
        cursor.execute("SELECT * FROM lottery WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            connection.close()
            raise HTTPException(status_code=400, detail="您已经抽过奖了")
        
        # 检查用户是否完成了所有站点
        cursor.execute("SELECT completed_stations, total_score FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user['completed_stations'] < 10:
            connection.close()
            raise HTTPException(status_code=400, detail="请先完成所有站点再抽奖")
        
        # 获取用户积分
        total_score = user['total_score']
        
        # 获取所有奖品
        cursor.execute("SELECT * FROM prizes ORDER BY level ASC")
        prizes = cursor.fetchall()
        
        if not prizes:
            connection.close()
            raise HTTPException(status_code=500, detail="奖品配置错误")
        
        # 根据积分计算中奖概率和奖品等级概率
        # 基础中奖概率 = 10%
        base_win_probability = 0.1
        # 积分越高，中奖概率和高等级奖品概率越高
        # 每100积分增加5%的中奖概率，最高增加到50%
        score_bonus = min(total_score / 100 * 0.05, 0.4)
        win_probability = base_win_probability + score_bonus
        
        # 生成随机数
        random_value = random.random()
        
        is_winner = random_value < win_probability
        prize_id = None
        prize_name = None
        
        if is_winner:
            # 根据积分计算各等级奖品的概率
            # 基础概率分布
            base_probabilities = {}
            for prize in prizes:
                base_probabilities[prize['level']] = prize['probability']
            
            # 积分越高，高等级奖品的概率越高
            # 每100积分增加高等级奖品的概率，降低低等级奖品的概率
            adjusted_probabilities = {}
            total_adjusted_probability = 0
            
            for prize in prizes:
                level = prize['level']
                # 等级越高，积分加成越高
                level_bonus = (level - 1) * (total_score / 1000)  # 每1000积分增加等级加成
                adjusted_prob = base_probabilities[level] * (1 + level_bonus)
                adjusted_probabilities[level] = adjusted_prob
                total_adjusted_probability += adjusted_prob
            
            # 归一化概率
            for level in adjusted_probabilities:
                adjusted_probabilities[level] /= total_adjusted_probability
            
            # 根据调整后的概率选择奖品
            prize_random = random.random()
            cumulative_prob = 0
            selected_prize = None
            
            for prize in prizes:
                cumulative_prob += adjusted_probabilities[prize['level']]
                if prize_random <= cumulative_prob:
                    selected_prize = prize
                    break
            
            if selected_prize:
                prize_id = selected_prize['id']
                prize_name = selected_prize['name']
        
        # 保存抽奖结果
        cursor.execute(
            "INSERT INTO lottery (user_id, winner, prize, prize_id) VALUES (%s, %s, %s, %s)",
            (user_id, is_winner, prize_name, prize_id)
        )
        connection.commit()
        connection.close()
        
        return {"is_winner": is_winner, "prize_name": prize_name, "prize_id": prize_id}
    
    @staticmethod
    def submit_address(user_id: int, name: str, phone: str, address: str):
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 检查用户是否是中奖者
        cursor.execute("SELECT winner FROM lottery WHERE user_id = %s", (user_id,))
        lottery_result = cursor.fetchone()
        
        if not lottery_result or not lottery_result[0]:
            connection.close()
            raise HTTPException(status_code=400, detail="您不是中奖者")
        
        # 更新邮寄地址
        cursor.execute(
            "UPDATE lottery SET name = %s, phone = %s, address = %s WHERE user_id = %s",
            (name, phone, address, user_id)
        )
        connection.commit()
        connection.close()
        
        return {"message": "地址提交成功"}
    
    @staticmethod
    def export_winners():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT l.name, l.phone, l.address, l.prize, l.created_at
            FROM lottery l
            WHERE l.winner = TRUE AND l.address IS NOT NULL
            ORDER BY l.created_at DESC
        """)
        
        winners = cursor.fetchall()
        connection.close()
        
        return winners
    
    @staticmethod
    def get_lottery_result(user_id: int):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM lottery WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        connection.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="未找到抽奖记录")
        
        return result

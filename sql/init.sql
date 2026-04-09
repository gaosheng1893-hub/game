-- 数据库初始化脚本
-- 版本: 1.0
-- 日期: 2026-04-07

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS map_game CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE map_game;

-- 删除现有表（如果存在）
DROP TABLE IF EXISTS leaderboard;
DROP TABLE IF EXISTS lottery;
DROP TABLE IF EXISTS prizes;
DROP TABLE IF EXISTS user_achievements;
DROP TABLE IF EXISTS achievements;
DROP TABLE IF EXISTS user_progress;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS stations;
DROP TABLE IF EXISTS users;

-- 1. 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    total_score INT DEFAULT 0,
    completed_stations INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 站点表
CREATE TABLE stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    position INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 问题表
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    question TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_answer ENUM('A', 'B', 'C', 'D') NOT NULL,
    score INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. 用户进度表
CREATE TABLE user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    station_id INT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_station (user_id, station_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. 成就表
CREATE TABLE achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    icon VARCHAR(50) NOT NULL,
    condition_type VARCHAR(50) NOT NULL,
    condition_value INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. 用户成就表
CREATE TABLE user_achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    achievement_id INT NOT NULL,
    obtained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_achievement (user_id, achievement_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. 奖品级别表
CREATE TABLE prizes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    level INT NOT NULL, -- 奖品级别，1-5，1最低，5最高
    probability FLOAT NOT NULL, -- 基础中奖概率
    description VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. 抽奖表
CREATE TABLE lottery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    winner BOOLEAN DEFAULT FALSE,
    prize VARCHAR(100) DEFAULT NULL,
    prize_id INT DEFAULT NULL, -- 关联奖品级别表
    name VARCHAR(50) DEFAULT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    address TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (prize_id) REFERENCES prizes(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. 排行榜表
CREATE TABLE leaderboard (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    score INT NOT NULL,
    ranking INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入默认站点数据
INSERT INTO stations (name, content, position) VALUES
('幽州', '幽州是三国时期北方的重要州郡，是公孙瓒的根据地，也是桃园三结义的故事背景所在地。', 1),
('冀州', '冀州是袁绍的大本营，在三国初期是北方最强大的势力范围，拥有丰富的资源和人口。', 2),
('青州', '青州位于山东半岛，是曹操统一北方的重要战略要地，也是许多著名战役的发生地。', 3),
('徐州', '徐州是兵家必争之地，陶谦曾在此让徐州给刘备，后来成为曹操与刘备争夺的焦点。', 4),
('豫州', '豫州是中原腹地，曹操的故乡，也是三国时期政治、经济的中心区域。', 5),
('兖州', '兖州是曹操发迹之地，他在这里招募了大量人才，为后来的曹魏政权奠定了基础。', 6),
('荆州', '荆州是三国时期的战略要地，刘备曾在此借荆州，引发了一系列重要的历史事件。', 7),
('扬州', '扬州是孙权的根据地，江南水乡，经济发达，是东吴政权的核心区域。', 8),
('益州', '益州是刘备的根据地，地势险要，资源丰富，为蜀汉政权提供了坚实的后方。', 9),
('凉州', '凉州是西北边陲，马超、韩遂等西凉军阀的活动区域，以骑兵著称。', 10);

-- 插入默认问题数据
INSERT INTO questions (station_id, question, option_a, option_b, option_c, option_d, correct_answer, score) VALUES
-- 幽州的问题
(1, '桃园三结义的故事发生在哪个州？', '幽州', '冀州', '青州', '徐州', 'A', 10),
-- 冀州的问题
(2, '袁绍在官渡之战中被谁击败？', '刘备', '孙权', '曹操', '吕布', 'C', 10),
-- 青州的问题
(3, '青州黄巾起义被谁平定？', '刘备', '曹操', '袁绍', '孙权', 'B', 10),
-- 徐州的问题
(4, '陶谦将徐州让给了谁？', '曹操', '刘备', '吕布', '袁绍', 'B', 10),
-- 豫州的问题
(5, '曹操的故乡在哪里？', '豫州', '兖州', '冀州', '徐州', 'A', 10),
-- 兖州的问题
(6, '曹操在兖州招募了哪位重要谋士？', '诸葛亮', '周瑜', '荀彧', '司马懿', 'C', 10),
-- 荆州的问题
(7, '刘备借荆州的故事中，他向谁借的荆州？', '曹操', '孙权', '袁绍', '刘璋', 'B', 10),
-- 扬州的问题
(8, '孙权的根据地主要在哪个州？', '扬州', '荆州', '益州', '徐州', 'A', 10),
-- 益州的问题
(9, '刘备入蜀后，谁成为了益州牧？', '刘璋', '刘备', '诸葛亮', '关羽', 'B', 10),
-- 凉州的问题
(10, '西凉马超的父亲是谁？', '马腾', '马岱', '马良', '马谡', 'A', 10);

-- 插入默认成就数据
INSERT INTO achievements (name, description, icon, condition_type, condition_value) VALUES
('新手入门', '完成第一个站点', '🌟', 'completed_stations', 1),
('稳步前进', '完成5个站点', '🏃', 'completed_stations', 5),
('通关达人', '完成所有站点', '🏆', 'completed_stations', 10),
('积分达人', '获得100积分', '🎯', 'score', 100),
('答题高手', '正确率达到80%', '✌️', 'accuracy', 80);

-- 插入默认奖品数据
INSERT INTO prizes (name, level, probability, description) VALUES
('安慰奖', 1, 0.5, '参与奖，感谢您的参与'),
('三等奖', 2, 0.3, '小礼品一份'),
('二等奖', 3, 0.15, '中等价值奖品'),
('一等奖', 4, 0.04, '高价值奖品'),
('特等奖', 5, 0.01, '超级大奖');

-- 插入默认用户（密码：123456）
-- 注意：生产环境中请删除此默认用户
INSERT INTO users (username, email, password, total_score, completed_stations) VALUES
('admin', 'admin@example.com', '$2b$12$eLgdvjXi2cbQYvgFGpMS1OcYxGejkdmytvumfsvte765ikSfUVfRi', 0, 0);

-- 创建索引
CREATE INDEX idx_users_score ON users (total_score DESC);
CREATE INDEX idx_leaderboard_score ON leaderboard (score DESC);
CREATE INDEX idx_user_progress_user ON user_progress (user_id);
CREATE INDEX idx_user_progress_station ON user_progress (station_id);

-- 优化表结构
OPTIMIZE TABLE users, stations, questions, user_progress, achievements, user_achievements, prizes, lottery, leaderboard;

-- 显示创建结果
SELECT '数据库初始化完成！' AS message;
SELECT '表结构创建成功：' AS message;
SELECT table_name FROM information_schema.tables WHERE table_schema = 'map_game';

SELECT '默认数据插入成功：' AS message;
SELECT COUNT(*) AS stations_count FROM stations;
SELECT COUNT(*) AS questions_count FROM questions;
SELECT COUNT(*) AS achievements_count FROM achievements;
SELECT COUNT(*) AS users_count FROM users;

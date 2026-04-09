import os
import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接配置
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'map_game')
}

# 数据库连接函数
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"数据库连接错误: {e}")

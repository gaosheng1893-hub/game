from fastapi import HTTPException
from common.database import get_db_connection
from common.jwt_utils import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from common.jwt_utils import ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    @staticmethod
    def register_user(username: str, email: str, password: str):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # 检查用户名是否已存在
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            connection.close()
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 检查邮箱是否已存在
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            connection.close()
            raise HTTPException(status_code=400, detail="邮箱已被注册")
        
        # 创建用户
        hashed_password = get_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        connection.commit()
        connection.close()
        
        return {"message": "注册成功"}
    
    @staticmethod
    def login_user(username: str, password: str):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        connection.close()
        
        if not user or not verify_password(password, user['password']):
            raise HTTPException(
                status_code=401,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user['username']}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}

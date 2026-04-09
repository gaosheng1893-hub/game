from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入路由
from routes.auth import auth_router
from routes.station import station_router
from routes.progress import progress_router
from routes.achievement import achievement_router
from routes.leaderboard import leaderboard_router
from routes.lottery import lottery_router
from routes.admin import admin_router

# 注册路由
app.include_router(auth_router)
app.include_router(station_router)
app.include_router(progress_router)
app.include_router(achievement_router)
app.include_router(leaderboard_router)
app.include_router(lottery_router)
app.include_router(admin_router)

# 测试接口
@app.get("/")
async def read_root():
    return {"message": "地图闯关游戏后端API"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
from fastapi import APIRouter
from controllers.admin_controller import router as admin_controller_router

admin_router = APIRouter()

# 导入管理后台的所有路由
admin_router.include_router(admin_controller_router)

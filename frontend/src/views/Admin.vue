<template>
  <div class="admin-container">
    <div class="admin-header">
      <h1>管理后台</h1>
      <p class="admin-subtitle">欢迎回来，管理员</p>
    </div>
    <div class="admin-menu">
      <router-link to="/admin/stations" class="menu-item">
        <div class="menu-icon">🏪</div>
        <span>站点设置</span>
      </router-link>
      <router-link to="/admin/questions" class="menu-item">
        <div class="menu-icon">❓</div>
        <span>问题设置</span>
      </router-link>
      <router-link to="/admin/achievements" class="menu-item">
        <div class="menu-icon">🏆</div>
        <span>成就设置</span>
      </router-link>
      <router-link to="/admin/prizes" class="menu-item">
        <div class="menu-icon">🏆</div>
        <span>奖品设置</span>
      </router-link>
     <router-link to="/admin/users" class="menu-item">
        <div class="menu-icon">👥</div>
        <span>用户设置</span>
      </router-link>
      <router-link to="/admin/lottery" class="menu-item">
        <div class="menu-icon">🎁</div>
        <span>抽奖记录</span>
      </router-link>
     </div>
    <div class="admin-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Admin'
}
</script>

<style scoped>
.admin-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 120px);
}

.admin-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.admin-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin: 0 0 10px 0;
  font-weight: 700;
}

.admin-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

.admin-menu {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  justify-content: center;
}

.menu-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #ffffff;
  color: #333;
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-width: 120px;
  text-align: center;
}

.menu-item:hover {
  background-color: #f5f5f5;
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.menu-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.menu-item span {
  font-size: 0.95rem;
  font-weight: 500;
}

.menu-item.router-link-active {
  background-color: #e3f2fd;
  border: 1px solid #2196F3;
}

.admin-content {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  min-height: 600px;
}

@media (max-width: 768px) {
  .admin-container {
    padding: 10px;
  }
  
  .admin-header h1 {
    font-size: 2rem;
  }
  
  .admin-menu {
    flex-direction: column;
    align-items: center;
  }
  
  .menu-item {
    width: 100%;
    max-width: 300px;
    flex-direction: row;
    justify-content: flex-start;
    padding: 15px;
  }
  
  .menu-icon {
    font-size: 1.5rem;
    margin-right: 15px;
    margin-bottom: 0;
  }
  
  .admin-content {
    padding: 20px;
  }
}
</style>

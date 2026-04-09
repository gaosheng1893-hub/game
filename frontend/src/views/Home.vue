<template>
  <div class="home">
    <div class="hero-section">
      <h1>地图闯关游戏</h1>
      <p>欢迎参加地图闯关游戏，开始你的冒险之旅！</p>
      <div class="button-group">
        <button @click="startGame" class="start-btn" v-if="isAuthenticated">开始游戏</button>
        <button @click="goToAuth" class="auth-btn" v-else>登录/注册</button>
      </div>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <div class="feature-icon">🗺️</div>
        <h3>探索地图</h3>
        <p>在精美的地图上探索各个站点，发现隐藏的宝藏和秘密</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3>挑战答题</h3>
        <p>每个站点都有精心设计的题目，考验你的知识和智慧</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🏆</div>
        <h3>成就系统</h3>
        <p>解锁各种成就，展示你的游戏成就和荣誉</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🎁</div>
        <h3>幸运抽奖</h3>
        <p>完成所有站点后参与抽奖，有机会获得丰厚奖品</p>
      </div>
    </div>
  </div>
</template>

<script>
import auth from '../services/auth.js'

export default {
  data() {
    return {
      isAuthenticated: auth.isAuthenticated()
    }
  },
  watch: {
    '$route': {
      handler: function() {
        this.isAuthenticated = auth.isAuthenticated()
      },
      immediate: true
    }
  },
  methods: {
    startGame() {
      this.$router.push('/map')
    },
    goToAuth() {
      this.$router.push('/auth')
    }
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.hero-section {
  text-align: center;
  padding: 4rem 2rem;
  color: white;
}

h1 {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-section p {
  font-size: 1.5rem;
  margin-bottom: 2.5rem;
  opacity: 0.9;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.start-btn,
.auth-btn {
  padding: 1.2rem 3rem;
  font-size: 1.2rem;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.start-btn {
  background: white;
  color: #667eea;
}

.start-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.auth-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.auth-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}
</style>
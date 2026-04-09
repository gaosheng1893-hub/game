<template>
  <div class="leaderboard">
    <div class="header">
      <h2>排行榜</h2>
      <p>查看顶尖玩家的成绩</p>
    </div>
    
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <div class="error-icon">⚠️</div>
      <p>{{ error }}</p>
      <button @click="loadLeaderboard" class="retry-btn">重试</button>
    </div>
    
    <div v-else class="leaderboard-container">
      <div v-if="leaderboard.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <p>暂无排行榜数据</p>
      </div>
      <div v-else>
        <div class="top-three">
          <div v-for="(player, index) in topThree" :key="player.id" 
               :class="['player-card', `rank-${index + 1}`]">
            <div class="rank-badge">{{ index + 1 }}</div>
            <div class="player-info">
              <div class="player-name">{{ player.username }}</div>
              <div class="player-score">{{ player.total_score }} 分</div>
              <div class="player-stations">完成 {{ player.completed_stations }} 个站点</div>
            </div>
            <div class="trophy-icon">
              <span v-if="index === 0">🏆</span>
              <span v-else-if="index === 1">🥈</span>
              <span v-else>🥉</span>
            </div>
          </div>
        </div>
        
        <div class="other-players">
          <div v-for="(player, index) in otherPlayers" :key="player.id" class="player-row">
            <div class="rank">{{ index + 4 }}</div>
            <div class="player-name">{{ player.username }}</div>
            <div class="player-score">{{ player.total_score }} 分</div>
            <div class="player-stations">{{ player.completed_stations }} 个站点</div>
          </div>
        </div>
      </div>
    </div>
    
    <button @click="goBack" class="back-btn">返回首页</button>
  </div>
</template>

<script>
import game from '../services/game.js'

export default {
  data() {
    return {
      leaderboard: [],
      loading: false,
      error: null
    }
  },
  computed: {
    topThree() {
      return this.leaderboard.slice(0, 3)
    },
    otherPlayers() {
      return this.leaderboard.slice(3, 10)
    }
  },
  async mounted() {
    await this.loadLeaderboard()
  },
  methods: {
    async loadLeaderboard() {
      this.loading = true
      this.error = null
      try {
        this.leaderboard = await game.getLeaderboard(10)
      } catch (error) {
        console.error('加载排行榜失败:', error)
        this.error = '加载排行榜失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    goBack() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: white;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: white;
  text-align: center;
  padding: 2rem;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.8rem 1.5rem;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #666;
  text-align: center;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}
</style>

<style scoped>
.leaderboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 3rem;
}

.header h2 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.leaderboard-container {
  max-width: 800px;
  margin: 0 auto;
}

.top-three {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.player-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  position: relative;
  min-width: 200px;
  flex: 1;
  transition: transform 0.3s;
}

.player-card:hover {
  transform: translateY(-5px);
}

.player-card.rank-1 {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  transform: scale(1.1);
}

.player-card.rank-2 {
  background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
}

.player-card.rank-3 {
  background: linear-gradient(135deg, #cd7f32 0%, #e8a87c 100%);
}

.rank-badge {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #667eea;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.player-info {
  text-align: center;
}

.player-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.player-score {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 0.3rem;
}

.player-stations {
  font-size: 0.9rem;
  color: #666;
}

.trophy-icon {
  text-align: center;
  font-size: 2.5rem;
  margin-top: 0.5rem;
}

.other-players {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.player-row {
  display: grid;
  grid-template-columns: 50px 1fr 100px 100px;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s;
}

.player-row:last-child {
  border-bottom: none;
}

.player-row:hover {
  background-color: #f8f9fa;
}

.player-row .rank {
  font-size: 1.2rem;
  font-weight: bold;
  color: #667eea;
  text-align: center;
}

.player-row .player-name {
  font-size: 1rem;
  color: #333;
  font-weight: 500;
}

.player-row .player-score {
  font-size: 1rem;
  color: #667eea;
  font-weight: bold;
  text-align: right;
}

.player-row .player-stations {
  font-size: 0.9rem;
  color: #666;
  text-align: right;
}

.back-btn {
  display: block;
  margin: 2rem auto 0;
  padding: 1rem 2rem;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}
</style>
<template>
  <div class="achievements">
    <h2>成就系统</h2>
    <div class="achievements-container">
      <div 
        v-for="achievement in achievements" 
        :key="achievement.id"
        :class="['achievement', { 'unlocked': achievement.obtained_at }]"
      >
        <div class="achievement-icon">{{ achievement.icon }}</div>
        <div class="achievement-info">
          <h3>{{ achievement.name }}</h3>
          <p>{{ achievement.description }}</p>
          <div v-if="achievement.obtained_at" class="unlock-date">
            解锁时间：{{ formatDate(achievement.obtained_at) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import game from '../services/game.js'
import auth from '../services/auth.js'

export default {
  data() {
    return {
      achievements: []
    }
  },
  async mounted() {
    await this.loadAchievements()
  },
  methods: {
    async loadAchievements() {
      try {
        const user = await auth.getCurrentUser()
        if (user) {
          this.achievements = await game.getUserAchievements(user.id)
        }
      } catch (error) {
        console.error('加载成就失败:', error)
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toISOString().split('T')[0]
    }
  }
}
</script>

<style scoped>
.achievements {
  padding: 2rem;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.achievements-container {
  max-width: 800px;
  margin: 0 auto;
}

.achievement {
  display: flex;
  align-items: center;
  background-color: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
  opacity: 0.6;
  transition: all 0.3s;
}

.achievement.unlocked {
  opacity: 1;
  border-left: 5px solid #4CAF50;
}

.achievement-icon {
  font-size: 3rem;
  margin-right: 1.5rem;
}

.achievement-info {
  flex: 1;
}

.achievement-info h3 {
  margin-bottom: 0.5rem;
  color: #333;
}

.achievement-info p {
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.unlock-date {
  font-size: 0.8rem;
  color: #999;
}
</style>
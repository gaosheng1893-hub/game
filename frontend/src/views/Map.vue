<template>
  <div class="map">
    <div class="map-header">
      <h2>三国州郡地图</h2>
      <div class="user-info">
        <span>积分: {{ userScore }}</span>
        <span>完成: {{ completedStations }}/{{ stations.length }}</span>
      </div>
    </div>
    
    <div class="map-container">
      <div class="map-background">
        <div class="terrain"></div>
        <div class="route-container">
          
          <!-- 站点 -->
          <div 
            v-for="(station, index) in stations" 
            :key="station.id"
            :class="['station-point', { 
              'completed': station.completed, 
              'current': station.current,
              'locked': station.locked
            }]"
            :style="getStationPosition(index)"
            @click="goToStation(station.id)"
          >
            <div class="station-icon">
              <span v-if="station.completed">✓</span>
              <span v-else-if="station.current">★</span>
              <span v-else>🔒</span>
            </div>
            <div class="station-label">{{ station.name }}</div>
          </div>
          
          <!-- 玩家角色 -->
          <div class="player-character" :style="playerPosition"></div>
        </div>
      </div>
      
      <div class="station-details" v-if="selectedStation">
        <div class="station-card">
          <h3>{{ selectedStation.name }}</h3>
          <p>{{ selectedStation.description }}</p>
          <div class="station-status">
            <span v-if="selectedStation.completed" class="status-completed">已完成</span>
            <span v-else-if="selectedStation.current" class="status-current">进行中</span>
            <span v-else class="status-locked">未解锁</span>
          </div>
          <div class="station-points" v-if="selectedStation.completed">
            +{{ selectedStation.points }} 分
          </div>
          <button 
            class="station-btn" 
            @click="goToStation(selectedStation.id)"
            :disabled="selectedStation.locked"
          >
            {{ selectedStation.locked ? '未解锁' : '进入站点' }}
          </button>
        </div>
      </div>
    </div>
    
    <div class="map-footer">
      <button @click="goToLeaderboard" class="footer-btn">查看排行榜</button>
    </div>
  </div>
</template>

<script>
import game from '../services/game.js'
import auth from '../services/auth.js'

export default {
  data() {
    return {
      stations: [],
      userProgress: [],
      userScore: 0,
      completedStations: 0,
      selectedStation: null
    }
  },
  async mounted() {
    await this.loadStations()
    await this.loadUserProgress()
  },
  computed: {
    playerPosition() {
      const currentStation = this.stations.find(s => s.current)
      if (currentStation) {
        const index = this.stations.indexOf(currentStation)
        const position = this.getStationPosition(index)
        return {
          left: position.left,
          top: position.top,
          transition: 'all 1s ease-in-out'
        }
      }
      return this.getStationPosition(0)
    }
  },
  methods: {
    getStationPosition(index) {
      // 根据实际地图调整各州郡的位置
      const positions = [
        { left: '18%', top: '18%' },    // 幽州 - 北方（北京附近）
        { left: '25%', top: '30%' },    // 冀州 - 华北（河北南部）
        { left: '32%', top: '40%' },    // 青州 - 山东半岛
        { left: '38%', top: '48%' },    // 徐州 - 华东（江苏北部）
        { left: '42%', top: '42%' },    // 豫州 - 中原（河南）
        { left: '35%', top: '35%' },    // 兖州 - 华北南部（山东西部）
        { left: '50%', top: '55%' },    // 荆州 - 中南（湖北）
        { left: '65%', top: '65%' },    // 扬州 - 江南（江苏南部、浙江）
        { left: '58%', top: '35%' },    // 益州 - 西南（四川）
        { left: '12%', top: '40%' }     // 凉州 - 西北（甘肃）
      ]
      return positions[index] || positions[0]
    },
    async loadStations() {
      try {
        const stations = await game.getStations()
        this.stations = stations.map((station, index) => ({
          ...station,
          description: station.content || this.getStationDescription(station.name),
          completed: false,
          current: false,
          locked: index > 0,
          points: 0
        }))
      } catch (error) {
        console.error('加载站点失败:', error)
      }
    },
    async loadUserProgress() {
      try {
        const user = await auth.getCurrentUser()
        if (user) {
          this.userScore = user.total_score || 0
          this.completedStations = user.completed_stations || 0
          
          const progress = await game.getUserProgress(user.id)
          progress.forEach(p => {
            const station = this.stations.find(s => s.id === p.station_id)
            if (station) {
              station.completed = p.completed
              station.points = p.score
            }
          })
          
          this.updateStationStatus()
        }
      } catch (error) {
        console.error('加载用户进度失败:', error)
      }
    },
    updateStationStatus() {
      let foundCurrent = false
      this.stations.forEach((station, index) => {
        if (!foundCurrent && !station.completed) {
          station.current = true
          station.locked = false
          foundCurrent = true
        } else if (!station.completed && index > 0) {
          station.locked = !this.stations[index - 1].completed
        }
      })
    },
    getStationDescription(name) {
      const descriptions = {
        '幽州': '幽州是三国时期北方的重要州郡，是公孙瓒的根据地，也是桃园三结义的故事背景所在地。',
        '冀州': '冀州是袁绍的大本营，在三国初期是北方最强大的势力范围，拥有丰富的资源和人口。',
        '青州': '青州位于山东半岛，是曹操统一北方的重要战略要地，也是许多著名战役的发生地。',
        '徐州': '徐州是兵家必争之地，陶谦曾在此让徐州给刘备，后来成为曹操与刘备争夺的焦点。',
        '豫州': '豫州是中原腹地，曹操的故乡，也是三国时期政治、经济的中心区域。',
        '兖州': '兖州是曹操发迹之地，他在这里招募了大量人才，为后来的曹魏政权奠定了基础。',
        '荆州': '荆州是三国时期的战略要地，刘备曾在此借荆州，引发了一系列重要的历史事件。',
        '扬州': '扬州是孙权的根据地，江南水乡，经济发达，是东吴政权的核心区域。',
        '益州': '益州是刘备的根据地，地势险要，资源丰富，为蜀汉政权提供了坚实的后方。',
        '凉州': '凉州是西北边陲，马超、韩遂等西凉军阀的活动区域，以骑兵著称。'
      }
      return descriptions[name] || '探索这个神秘的州郡'
    },
    goToStation(id) {
      const station = this.stations.find(s => s.id === id)
      if (station && !station.locked) {
        this.$router.push(`/station/${id}`)
      }
    },
    goToLeaderboard() {
      this.$router.push('/leaderboard')
    }
  }
}
</script>

<style scoped>
.map {
  min-height: 100vh;
  background: linear-gradient(135deg, #8B4513 0%, #CD853F 100%);
  padding: 2rem;
}

.map-header {
  text-align: center;
  color: white;
  margin-bottom: 3rem;
}

.map-header h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.user-info {
  display: flex;
  justify-content: center;
  gap: 2rem;
  font-size: 1.2rem;
  opacity: 0.9;
}

.map-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 0;
}

.map-background {
  position: relative;
  height: 600px;
  margin-bottom: 4rem;
  background: url('https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=three%20kingdoms%20kill%20style%20map%2C%20ancient%20chinese%20provinces%2C%20colorful%20art%2C%20detailed%20borders%2C%20game%20style&image_size=landscape_16_9');
  background-size: cover;
  background-position: center;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.terrain {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 0;
}

.route-container {
  position: relative;
  height: 100%;
  width: 100%;
  z-index: 1;
}



.station-point {
  position: absolute;
  transform: translate(-50%, -50%);
  z-index: 2;
  cursor: pointer;
  transition: all 0.3s ease;
}

.station-point:hover {
  transform: translate(-50%, -50%) scale(1.1);
}

.station-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  z-index: 2;
  transition: all 0.3s ease;
}

.station-point.completed .station-icon {
  background: #4CAF50;
  color: white;
}

.station-point.current .station-icon {
  background: #FFD700;
  color: white;
  animation: pulse 2s infinite;
}

.station-point.locked .station-icon {
  background: #9e9e9e;
  color: white;
  opacity: 0.6;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.station-label {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 10px;
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
  white-space: nowrap;
}

.player-character {
  position: absolute;
  transform: translate(-50%, -50%);
  width: 50px;
  height: 70px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 60"><circle cx="20" cy="15" r="10" fill="%23FFD700"/><path d="M20 25 L10 45 L20 40 L30 45 Z" fill="%238B4513"/><path d="M15 50 L20 45 L25 50" stroke="%23333" stroke-width="2" fill="none"/><path d="M12 35 L28 35" stroke="%23CD853F" stroke-width="3" fill="none"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
  z-index: 3;
  transition: all 1s ease-in-out;
  animation: walk 1s infinite alternate;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
}

@keyframes walk {
  0% {
    transform: translate(-50%, -50%) rotate(-5deg);
  }
  100% {
    transform: translate(-50%, -50%) rotate(5deg);
  }
}

/* 地图装饰元素 */
.map-background::before {
  content: '';
  position: absolute;
  top: 10%;
  left: 10%;
  width: 80%;
  height: 80%;
  background: radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
              radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
  z-index: 0;
}

.station-details {
  max-width: 600px;
  margin: 0 auto;
}

.station-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}

.station-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.station-card p {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.station-status {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.status-completed {
  background: #4CAF50;
  color: white;
}

.status-current {
  background: #FFD700;
  color: #333;
}

.status-locked {
  background: #9e9e9e;
  color: white;
}

.station-points {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #4CAF50;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-weight: bold;
  font-size: 0.9rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.station-btn {
  padding: 0.8rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  margin-top: 1rem;
}

.station-btn:hover:not(:disabled) {
  background: #764ba2;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.station-btn:disabled {
  background: #9e9e9e;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.map-footer {
  text-align: center;
  margin-top: 3rem;
}

.footer-btn {
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

.footer-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .route-path {
    height: 120px;
  }
  
  .station-icon {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }
  
  .player-character {
    width: 35px;
    height: 50px;
  }
  
  .station-label {
    font-size: 0.8rem;
  }
}
</style>
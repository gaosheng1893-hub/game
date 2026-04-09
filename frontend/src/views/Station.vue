<template>
  <div class="station-page">
    <div class="station-header">
      <button @click="goBack" class="back-btn">← 返回地图</button>
      <h2>{{ station.name }}</h2>
      <div class="progress-indicator">
        <span>进度: {{ currentStation }}/{{ totalStations }}</span>
      </div>
    </div>
    
    <div class="content">
      <div v-if="!showQuiz && !showResult" class="station-content">
        <div class="content-card">
          <div class="content-icon">📖</div>
          <h3>站点内容</h3>
          <p>{{ station.content }}</p>
          <button @click="startQuiz" class="start-quiz-btn">开始答题</button>
        </div>
      </div>
      
      <div v-if="showQuiz && !showResult" class="quiz-container">
        <div class="quiz-card">
          <div class="quiz-header">
            <div class="question-number">问题 {{ currentQuestionIndex + 1 }}/{{ questions.length }}</div>
            <div class="timer" v-if="timeLeft > 0">
              ⏱️ {{ formatTime(timeLeft) }}
            </div>
          </div>
          
          <div class="question-content">
            <h3>{{ currentQuestion.question }}</h3>
            <div class="options-grid">
              <div 
                v-for="(option, index) in getOptions()" 
                :key="index"
                :class="['option-card', { 
                  'selected': selectedOption === index,
                  'correct': showAnswer && index === correctOptionIndex,
                  'wrong': showAnswer && selectedOption === index && index !== correctOptionIndex
                }]"
                @click="selectOption(index)"
              >
                <div class="option-label">{{ ['A', 'B', 'C', 'D'][index] }}</div>
                <div class="option-text">{{ option }}</div>
              </div>
            </div>
          </div>
          
          <div class="quiz-footer">
            <button 
              @click="submitAnswer" 
              class="submit-btn"
              :disabled="selectedOption === null || showAnswer"
            >
              {{ showAnswer ? '继续' : '提交答案' }}
            </button>
          </div>
        </div>
      </div>
      
      <div v-if="showResult" class="result-container">
        <div class="result-card">
          <div class="result-icon">
            <span v-if="isCorrect">🎉</span>
            <span v-else>😔</span>
          </div>
          <h3>{{ isCorrect ? '回答正确！' : '回答错误' }}</h3>
          <p v-if="!isCorrect" class="correct-answer">
            正确答案：{{ ['A', 'B', 'C', 'D'][correctOptionIndex] }}
          </p>
          <div class="score-display">
            <span v-if="isCorrect">+{{ currentQuestion.points }} 分</span>
            <span v-else>0 分</span>
          </div>
          <div class="result-stats">
            <div class="stat-item">
              <span class="stat-label">正确率</span>
              <span class="stat-value">{{ accuracy }}%</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">总积分</span>
              <span class="stat-value">{{ totalScore }}</span>
            </div>
          </div>
          <button @click="nextQuestion" class="next-btn">
            {{ hasNextQuestion ? '下一题' : '下一站' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 成就提示弹窗 -->
    <div v-if="showAchievement && newAchievement" class="achievement-popup">
      <div class="achievement-content">
        <div class="achievement-icon-large">{{ newAchievement.icon }}</div>
        <h3>🏆 成就解锁！</h3>
        <h4>{{ newAchievement.name }}</h4>
        <p>{{ newAchievement.description }}</p>
        <button @click="closeAchievement" class="close-btn">关闭</button>
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
      station: {},
      questions: [],
      showQuiz: false,
      showResult: false,
      showAnswer: false,
      currentQuestionIndex: 0,
      selectedOption: null,
      isCorrect: false,
      correctOptionIndex: 0,
      timeLeft: 30,
      timer: null,
      currentStation: 1,
      totalStations: 10,
      accuracy: 100,
      totalScore: 0,
      correctCount: 0,
      totalAnswered: 0,
      showAchievement: false,
      newAchievement: null
    }
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentQuestionIndex] || {}
    },
    hasNextQuestion() {
      return this.currentQuestionIndex < this.questions.length - 1
    }
  },
  async mounted() {
    await this.loadStation()
    this.currentStation = parseInt(this.$route.params.id)
  },
  watch: {
    '$route.params.id': {
      handler: async function(newId) {
        console.log('Route param changed:', newId)
        await this.loadStation()
        this.currentStation = parseInt(newId)
      },
      immediate: false
    }
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer)
    }
  },
  methods: {
    async loadStation() {
      console.log('loadStation called')
      try {
        const stationId = this.$route.params.id
        console.log('Loading station:', stationId)
        this.station = await game.getStation(stationId)
        console.log('Station loaded:', this.station)
        this.questions = this.station.questions || []
        console.log('Questions:', this.questions)
        
        // 获取站点总数
        const stations = await game.getStations()
        this.totalStations = stations.length
        console.log('Total stations:', this.totalStations)
        
        // 重置问题相关状态
        this.currentQuestionIndex = 0
        this.showQuiz = false
        this.showResult = false
        this.showAnswer = false
        this.selectedOption = null
        this.isCorrect = false
        this.correctOptionIndex = 0
        this.timeLeft = 30
        if (this.timer) {
          clearInterval(this.timer)
          this.timer = null
        }
      } catch (error) {
        console.error('加载站点失败:', error)
      }
    },
    startQuiz() {
      this.showQuiz = true
      this.startTimer()
    },
    startTimer() {
      this.timeLeft = 30
      this.timer = setInterval(() => {
        this.timeLeft--
        if (this.timeLeft <= 0) {
          clearInterval(this.timer)
          this.timeUp()
        }
      }, 1000)
    },
    timeUp() {
      this.showAnswer = true
      this.showResult = true
      this.isCorrect = false
      this.totalAnswered++
    },
    getOptions() {
      if (!this.currentQuestion) return []
      return [
        this.currentQuestion.option_a,
        this.currentQuestion.option_b,
        this.currentQuestion.option_c,
        this.currentQuestion.option_d
      ]
    },
    selectOption(index) {
      if (!this.showAnswer) {
        this.selectedOption = index
      }
    },
    async submitAnswer() {
      if (this.showAnswer) {
        this.nextQuestion()
        return
      }
      
      if (this.selectedOption === null) return
      
      clearInterval(this.timer)
      this.showAnswer = true
      
      const answer = ['A', 'B', 'C', 'D'][this.selectedOption]
      this.correctOptionIndex = ['A', 'B', 'C', 'D'].indexOf(this.currentQuestion.correct_answer)
      
      try {
        const user = await auth.getCurrentUser()
        const result = await game.submitAnswer(
          user.id,
          parseInt(this.$route.params.id),
          this.currentQuestion.id,
          answer
        )
        
        this.isCorrect = result.is_correct
        this.totalAnswered++
        
        if (this.isCorrect) {
          this.correctCount++
          this.totalScore += result.score
        }
        
        this.accuracy = Math.round((this.correctCount / this.totalAnswered) * 100)
        
        // 检查是否有新成就
        if (result.new_achievements && result.new_achievements.length > 0) {
          this.newAchievement = result.new_achievements[0]
          this.showAchievement = true
        }
        
        setTimeout(() => {
          this.showResult = true
        }, 1000)
      } catch (error) {
        console.error('提交答案失败:', error)
      }
    },
    nextQuestion() {
      console.log('nextQuestion called')
      console.log('hasNextQuestion:', this.hasNextQuestion)
      console.log('currentQuestionIndex:', this.currentQuestionIndex)
      console.log('questions.length:', this.questions.length)
      if (this.hasNextQuestion) {
        this.currentQuestionIndex++
        this.resetQuestion()
      } else {
        this.goToNextStation()
      }
    },
    resetQuestion() {
      this.showResult = false
      this.showAnswer = false
      this.selectedOption = null
      this.startTimer()
    },
    goToNextStation() {
      console.log('goToNextStation called')
      const currentId = parseInt(this.$route.params.id)
      const nextId = currentId + 1
      console.log('currentId:', currentId)
      console.log('nextId:', nextId)
      console.log('totalStations:', this.totalStations)
      if (nextId <= this.totalStations) {
        console.log('Navigating to station:', nextId)
        this.$router.push(`/station/${nextId}`)
      } else {
        console.log('Navigating to lottery')
        this.$router.push('/lottery')
      }
    },
    goBack() {
      this.$router.push('/map')
    },
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins}:${secs.toString().padStart(2, '0')}`
    },
    closeAchievement() {
      this.showAchievement = false
      this.newAchievement = null
    }
  }
}
</script>

<style scoped>
.station-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.station-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  color: white;
}

.back-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.station-header h2 {
  font-size: 2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.progress-indicator {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
}

.content {
  max-width: 900px;
  margin: 0 auto;
}

.content-card,
.quiz-card,
.result-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.content-icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
}

.content-card h3,
.quiz-card h3,
.result-card h3 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.content-card p {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #666;
  margin-bottom: 2rem;
  text-align: left;
}

.start-quiz-btn {
  padding: 1.2rem 3rem;
  font-size: 1.2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.start-quiz-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.question-number {
  font-size: 1.2rem;
  color: #667eea;
  font-weight: 600;
}

.timer {
  font-size: 1.2rem;
  color: #f44336;
  font-weight: 600;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.question-content h3 {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  color: #333;
  line-height: 1.6;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.option-card {
  background: #f8f9fa;
  border: 3px solid #e0e0e0;
  border-radius: 15px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.option-card:hover:not(.selected):not(.correct):not(.wrong) {
  background: #e9ecef;
  border-color: #667eea;
  transform: translateY(-3px);
}

.option-card.selected {
  background: #e3f2fd;
  border-color: #2196F3;
  transform: scale(1.02);
}

.option-card.correct {
  background: #d4edda;
  border-color: #28a745;
  animation: correctPulse 0.5s;
}

.option-card.wrong {
  background: #f8d7da;
  border-color: #dc3545;
  animation: shake 0.5s;
}

@keyframes correctPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

.option-label {
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
  flex-shrink: 0;
}

.option-card.correct .option-label {
  background: #28a745;
}

.option-card.wrong .option-label {
  background: #dc3545;
}

.option-text {
  font-size: 1.1rem;
  color: #333;
  flex: 1;
}

.quiz-footer {
  margin-top: 2rem;
}

.submit-btn,
.next-btn {
  padding: 1.2rem 3rem;
  font-size: 1.2rem;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.next-btn {
  background: #4CAF50;
  color: white;
}

.next-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.result-icon {
  font-size: 6rem;
  margin-bottom: 1.5rem;
  animation: bounce 0.5s;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.result-card h3 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.result-card h3:first-child {
  color: #4CAF50;
}

.result-card h3:first-child.wrong {
  color: #f44336;
}

.correct-answer {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.score-display {
  font-size: 2rem;
  font-weight: bold;
  color: #4CAF50;
  margin-bottom: 2rem;
  padding: 1rem 2rem;
  background: #d4edda;
  border-radius: 15px;
  display: inline-block;
}

.result-stats {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin-bottom: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 1rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
}

/* 成就提示弹窗样式 */
.achievement-popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.achievement-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 3rem;
  text-align: center;
  color: white;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.5s ease;
  max-width: 500px;
  width: 80%;
}

.achievement-icon-large {
  font-size: 6rem;
  margin-bottom: 1.5rem;
  animation: bounce 0.5s;
}

.achievement-content h3 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.achievement-content h4 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #FFD700;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.achievement-content p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  line-height: 1.5;
  opacity: 0.9;
}

.close-btn {
  padding: 0.8rem 2rem;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.close-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@media (max-width: 768px) {
  .achievement-content {
    padding: 2rem;
    width: 90%;
  }
  
  .achievement-icon-large {
    font-size: 4rem;
  }
}
</style>
<template>
  <div class="lottery">
    <h2>抽奖系统</h2>
    
    <!-- 管理员中奖名单 -->
    <div v-if="isAdmin" class="admin-section">
      <h3>中奖名单管理</h3>
      <div class="admin-actions">
        <button @click="exportWinners" class="export-btn" :disabled="loadingWinners">
          {{ loadingWinners ? '导出中...' : '导出中奖名单' }}
        </button>
      </div>
      <div v-if="loadingWinners" class="loading">加载中...</div>
      <div v-else-if="winners.length > 0" class="winners-table">
        <table>
          <thead>
            <tr>
              <th>序号</th>
              <th>用户名</th>
              <th>奖品</th>
              <th>姓名</th>
              <th>手机号</th>
              <th>地址</th>
              <th>抽奖时间</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(winner, index) in winners" :key="winner.id">
              <td>{{ index + 1 }}</td>
              <td>{{ winner.username }}</td>
              <td>{{ winner.prize }}</td>
              <td>{{ winner.name || '-' }}</td>
              <td>{{ winner.phone || '-' }}</td>
              <td>{{ winner.address || '-' }}</td>
              <td>{{ new Date(winner.created_at).toLocaleString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="no-winners">
        <p>暂无中奖记录</p>
      </div>
    </div>
    
    <!-- 用户抽奖界面 -->
    <div v-if="!isAdmin" class="lottery-container">
      <div v-if="!hasLottery && !hasAlreadyLottery" class="lottery-start">
        <p>恭喜你完成了所有站点！现在可以参加抽奖了。</p>
        <button @click="startLottery" class="lottery-btn" :disabled="loading">
          {{ loading ? '抽奖中...' : '开始抽奖' }}
        </button>
      </div>
      <div v-else-if="hasAlreadyLottery && !isWinner" class="lottery-result">
        <h3>已参与抽奖</h3>
        <p>你已经参与过抽奖，每人只能抽奖一次。</p>
        <p class="note">感谢你的参与！</p>
      </div>
      <div v-else-if="hasAlreadyLottery && isWinner" class="lottery-winner">
        <h3>恭喜你中奖了！</h3>
        <p>你已经中奖，奖品是：{{ lotteryResult.prize }}</p>
        <p v-if="lotteryResult.name">地址已提交，我们会尽快将奖品寄给你。</p>
        <form v-else @submit.prevent="submitAddress" class="address-form">
          <div class="form-group">
            <label>姓名</label>
            <input type="text" v-model="address.name" required>
          </div>
          <div class="form-group">
            <label>手机号</label>
            <input type="tel" v-model="address.phone" required>
          </div>
          <div class="form-group">
            <label>地址</label>
            <textarea v-model="address.address" required></textarea>
          </div>
          <button type="submit" class="submit-btn" :disabled="submitting">
            {{ submitting ? '提交中...' : '提交地址' }}
          </button>
        </form>
      </div>
      <div v-else-if="!isWinner && hasLottery" class="lottery-result">
        <h3>很遗憾</h3>
        <p>这次没有中奖，再接再厉！</p>
        <p class="note">每人只能抽奖一次，感谢参与！</p>
      </div>
      <div v-else class="lottery-winner">
        <h3>恭喜你中奖了！</h3>
        <p>请填写你的邮寄地址，我们会将奖品寄给你。</p>
        <form @submit.prevent="submitAddress" class="address-form">
          <div class="form-group">
            <label>姓名</label>
            <input type="text" v-model="address.name" required>
          </div>
          <div class="form-group">
            <label>手机号</label>
            <input type="tel" v-model="address.phone" required>
          </div>
          <div class="form-group">
            <label>地址</label>
            <textarea v-model="address.address" required></textarea>
          </div>
          <button type="submit" class="submit-btn" :disabled="submitting">
            {{ submitting ? '提交中...' : '提交地址' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import game from '../services/game.js'

export default {
  data() {
    return {
      hasLottery: false,
      hasAlreadyLottery: false,
      isWinner: false,
      lotteryResult: null,
      address: {
        name: '',
        phone: '',
        address: ''
      },
      loading: false,
      submitting: false,
      isAdmin: false,
      winners: [],
      loadingWinners: false
    }
  },
  mounted() {
    // 检查用户是否已经抽过奖
    this.checkLotteryStatus()
    // 检查是否为管理员
    this.checkAdminStatus()
    // 如果是管理员，获取中奖名单
    if (this.isAdmin) {
      this.getWinners()
    }
  },
  methods: {
    checkAdminStatus() {
      const user = JSON.parse(localStorage.getItem('user'))
      // 假设admin用户为管理员
      this.isAdmin = user && user.username === 'admin'
    },
    async checkLotteryStatus() {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (user) {
          // 尝试获取抽奖结果
          const result = await game.getLotteryResult(user.id)
          this.hasAlreadyLottery = true
          this.isWinner = result.winner
          this.lotteryResult = result
          console.log('用户已经抽过奖，获取到抽奖结果:', result)
        }
      } catch (error) {
        console.error('检查抽奖状态失败:', error)
        console.error('错误信息:', error.message)
        if (error.message && (error.message.includes('未找到抽奖记录') || error.message.includes('404'))) {
          // 用户未抽奖，不需要处理
          console.log('用户未抽奖')
        } else if (error.message && (error.message.includes('您已经抽过奖了') || error.message.includes('已经抽过奖'))) {
          this.hasAlreadyLottery = true
          console.log('用户已经抽过奖，更新状态')
        }
      }
    },
    async getWinners() {
      if (!this.isAdmin) return
      
      try {
        this.loadingWinners = true
        const result = await game.getWinners()
        this.winners = result
        console.log('获取中奖名单成功:', result)
      } catch (error) {
        console.error('获取中奖名单失败:', error)
        alert('获取中奖名单失败，请稍后重试')
      } finally {
        this.loadingWinners = false
      }
    },
    exportWinners() {
      if (this.winners.length === 0) {
        alert('暂无中奖记录')
        return
      }
      
      // 生成CSV内容
      const headers = ['序号', '用户名', '奖品', '姓名', '手机号', '地址', '抽奖时间']
      const rows = this.winners.map((winner, index) => [
        index + 1,
        winner.username,
        winner.prize,
        winner.name || '-',
        winner.phone || '-',
        winner.address || '-',
        new Date(winner.created_at).toLocaleString()
      ])
      
      // 组合成CSV字符串
      const csvContent = [
        headers.join(','),
        ...rows.map(row => row.join(','))
      ].join('\n')
      
      // 创建下载链接
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', `中奖名单_${new Date().toISOString().slice(0, 10)}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    async startLottery() {
      try {
        this.loading = true
        const user = JSON.parse(localStorage.getItem('user'))
        const userId = user.id
        const result = await game.lottery(userId)
        this.hasLottery = true
        this.isWinner = result.is_winner
        this.lotteryResult = result
        
        // 如果是管理员，刷新中奖名单
        if (this.isAdmin) {
          this.getWinners()
        }
      } catch (error) {
        console.error('抽奖失败:', error)
        console.error('错误信息:', error.message)
        console.error('错误详情:', error.response?.data)
        if (error.message && (error.message.includes('您已经抽过奖了') || error.message.includes('已经抽过奖'))) {
          this.hasAlreadyLottery = true
          // 尝试获取抽奖结果
          try {
            const user = JSON.parse(localStorage.getItem('user'))
            const result = await game.getLotteryResult(user.id)
            this.isWinner = result.winner
            this.lotteryResult = result
          } catch (e) {
            console.error('获取抽奖结果失败:', e)
          }
          console.log('用户已经抽过奖，更新状态')
        } else {
          alert(error.message || '抽奖失败，请稍后重试')
        }
      } finally {
        this.loading = false
      }
    },
    async submitAddress() {
      try {
        this.submitting = true
        const user = JSON.parse(localStorage.getItem('user'))
        const userId = user.id
        await game.submitAddress(userId, this.address.name, this.address.phone, this.address.address)
        alert('地址提交成功！我们会尽快将奖品寄给你。')
        // 更新本地抽奖结果
        this.lotteryResult.name = this.address.name
        this.lotteryResult.phone = this.address.phone
        this.lotteryResult.address = this.address.address
        
        // 如果是管理员，刷新中奖名单
        if (this.isAdmin) {
          this.getWinners()
        }
      } catch (error) {
        console.error('提交地址失败:', error)
        alert(error.message || '提交地址失败，请稍后重试')
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>

<style scoped>
.lottery {
  padding: 2rem;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

h3 {
  color: #333;
  margin-bottom: 1rem;
}

.lottery-container {
  max-width: 600px;
  margin: 0 auto;
}

/* 管理员部分样式 */
.admin-section {
  background-color: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.admin-actions {
  margin-bottom: 1rem;
  text-align: right;
}

.export-btn {
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  background-color: #4CAF50;
  color: white;
}

.export-btn:hover {
  background-color: #45a049;
}

.export-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.winners-table {
  overflow-x: auto;
}

.winners-table table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.winners-table th,
.winners-table td {
  padding: 0.8rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.winners-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.winners-table tr:hover {
  background-color: #f5f5f5;
}

.no-winners {
  text-align: center;
  padding: 2rem;
  color: #666;
}

/* 抽奖部分样式 */
.lottery-start,
.lottery-result,
.lottery-winner {
  background-color: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

p {
  margin-bottom: 2rem;
  color: #666;
}

.lottery-btn,
.restart-btn,
.submit-btn {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.lottery-btn {
  background-color: #f44336;
  color: white;
  font-weight: bold;
}

.lottery-btn:hover {
  background-color: #d32f2f;
}

.lottery-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.restart-btn {
  background-color: #4CAF50;
  color: white;
}

.restart-btn:hover {
  background-color: #45a049;
}

.submit-btn {
  background-color: #2196F3;
  color: white;
  margin-top: 1rem;
}

.submit-btn:hover {
  background-color: #1976D2;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.address-form {
  text-align: left;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.form-group textarea {
  height: 100px;
  resize: vertical;
}

.note {
  font-style: italic;
  color: #999;
}
</style>
<template>
  <div class="lottery-container">
    <h2>抽奖记录</h2>
    
    <!-- 抽奖记录列表 -->
    <div class="list-container">
      <h3>抽奖记录</h3>
      <table class="lottery-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>是否中奖</th>
            <th>奖品</th>
            <th>姓名</th>
            <th>电话</th>
            <th>地址</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in lotteryRecords" :key="record.id">
            <td>{{ record.id }}</td>
            <td>{{ record.username }}</td>
            <td>{{ record.winner ? '是' : '否' }}</td>
            <td>{{ record.prize || '未设置' }}</td>
            <td>{{ record.name || '未填写' }}</td>
            <td>{{ record.phone || '未填写' }}</td>
            <td>{{ record.address || '未填写' }}</td>
            <td>{{ formatDate(record.created_at) }}</td>
            <td>
              <button v-if="!record.winner" @click="setWinner(record)" class="btn btn-edit">设置中奖</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 设置中奖对话框 -->
    <div v-if="selectedRecord" class="modal">
      <div class="modal-content">
        <h3>设置中奖</h3>
        <form @submit.prevent="confirmWinner">
          <div class="form-group">
            <label for="prize">奖品</label>
            <input type="text" id="prize" v-model="prize" required>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">确认</button>
            <button type="button" @click="selectedRecord = null" class="btn btn-cancel">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Lottery',
  data() {
    return {
      lotteryRecords: [],
      selectedRecord: null,
      prize: ''
    }
  },
  mounted() {
    this.fetchLotteryRecords()
  },
  methods: {
    async fetchLotteryRecords() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/lottery', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('获取抽奖记录失败')
        this.lotteryRecords = await response.json()
      } catch (error) {
        console.error('获取抽奖记录失败:', error)
        alert('获取抽奖记录失败')
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString()
    },
    setWinner(record) {
      this.selectedRecord = record
      this.prize = ''
    },
    async confirmWinner() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/lottery/winners', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            lottery_id: this.selectedRecord.id,
            prize: this.prize
          })
        })
        if (!response.ok) throw new Error('设置中奖失败')
        const updatedRecord = await response.json()
        const index = this.lotteryRecords.findIndex(r => r.id === updatedRecord.id)
        if (index !== -1) {
          this.lotteryRecords[index] = updatedRecord
        }
        this.selectedRecord = null
        this.prize = ''
        alert('设置中奖成功')
      } catch (error) {
        console.error('设置中奖失败:', error)
        alert('设置中奖失败')
      }
    }
  }
}
</script>

<style scoped>
.lottery-container {
  max-width: 1200px;
  margin: 0 auto;
}

.list-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.lottery-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.lottery-table th,
.lottery-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.lottery-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.lottery-table tr:hover {
  background-color: #f5f5f5;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-edit {
  background-color: #2196F3;
  color: white;
}

.btn-edit:hover {
  background-color: #0b7dda;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-cancel {
  background-color: #9e9e9e;
  color: white;
  margin-left: 10px;
}

.btn-cancel:hover {
  background-color: #757575;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .lottery-table {
    font-size: 14px;
  }
  
  .lottery-table th,
  .lottery-table td {
    padding: 8px;
  }
  
  .btn {
    padding: 6px 12px;
    font-size: 14px;
  }
}
</style>

<template>
  <div class="achievements-container">
    <h2>成就设置</h2>
    
    <!-- 添加成就表单 -->
    <div class="form-container">
      <h3>添加新成就</h3>
      <form @submit.prevent="addAchievement">
        <div class="form-group">
          <label for="name">成就名称</label>
          <input type="text" id="name" v-model="newAchievement.name" required>
        </div>
        <div class="form-group">
          <label for="description">成就描述</label>
          <textarea id="description" v-model="newAchievement.description" required></textarea>
        </div>
        <div class="form-group">
          <label for="icon">成就图标</label>
          <input type="text" id="icon" v-model="newAchievement.icon" required>
        </div>
        <div class="form-group">
          <label for="condition_type">条件类型</label>
          <select id="condition_type" v-model="newAchievement.condition_type" required>
            <option value="completed_stations">完成站点数</option>
            <option value="score">积分</option>
            <option value="accuracy">正确率</option>
          </select>
        </div>
        <div class="form-group">
          <label for="condition_value">条件值</label>
          <input type="number" id="condition_value" v-model="newAchievement.condition_value" required>
        </div>
        <button type="submit" class="btn btn-primary">添加成就</button>
      </form>
    </div>
    
    <!-- 成就列表 -->
    <div class="list-container">
      <h3>成就列表</h3>
      <table class="achievements-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>图标</th>
            <th>名称</th>
            <th>描述</th>
            <th>条件类型</th>
            <th>条件值</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="achievement in achievements" :key="achievement.id">
            <td>{{ achievement.id }}</td>
            <td>{{ achievement.icon }}</td>
            <td>{{ achievement.name }}</td>
            <td>{{ achievement.description }}</td>
            <td>{{ getConditionTypeName(achievement.condition_type) }}</td>
            <td>{{ achievement.condition_value }}</td>
            <td>
              <button @click="editAchievement(achievement)" class="btn btn-edit">编辑</button>
              <button @click="deleteAchievement(achievement.id)" class="btn btn-delete">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 编辑成就对话框 -->
    <div v-if="editingAchievement" class="modal">
      <div class="modal-content">
        <h3>编辑成就</h3>
        <form @submit.prevent="updateAchievement">
          <div class="form-group">
            <label for="edit-name">成就名称</label>
            <input type="text" id="edit-name" v-model="editingAchievement.name" required>
          </div>
          <div class="form-group">
            <label for="edit-description">成就描述</label>
            <textarea id="edit-description" v-model="editingAchievement.description" required></textarea>
          </div>
          <div class="form-group">
            <label for="edit-icon">成就图标</label>
            <input type="text" id="edit-icon" v-model="editingAchievement.icon" required>
          </div>
          <div class="form-group">
            <label for="edit-condition_type">条件类型</label>
            <select id="edit-condition_type" v-model="editingAchievement.condition_type" required>
              <option value="completed_stations">完成站点数</option>
              <option value="score">积分</option>
              <option value="accuracy">正确率</option>
            </select>
          </div>
          <div class="form-group">
            <label for="edit-condition_value">条件值</label>
            <input type="number" id="edit-condition_value" v-model="editingAchievement.condition_value" required>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">保存</button>
            <button type="button" @click="editingAchievement = null" class="btn btn-cancel">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Achievements',
  data() {
    return {
      achievements: [],
      newAchievement: {
        name: '',
        description: '',
        icon: '🌟',
        condition_type: 'completed_stations',
        condition_value: 1
      },
      editingAchievement: null
    }
  },
  mounted() {
    this.fetchAchievements()
  },
  methods: {
    async fetchAchievements() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/achievements', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('获取成就失败')
        this.achievements = await response.json()
      } catch (error) {
        console.error('获取成就失败:', error)
        alert('获取成就失败')
      }
    },
    getConditionTypeName(conditionType) {
      const typeMap = {
        'completed_stations': '完成站点数',
        'score': '积分',
        'accuracy': '正确率'
      }
      return typeMap[conditionType] || conditionType
    },
    async addAchievement() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/achievements', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.newAchievement)
        })
        if (!response.ok) throw new Error('添加成就失败')
        const newAchievement = await response.json()
        this.achievements.push(newAchievement)
        this.newAchievement = {
          name: '',
          description: '',
          icon: '🌟',
          condition_type: 'completed_stations',
          condition_value: 1
        }
        alert('成就添加成功')
      } catch (error) {
        console.error('添加成就失败:', error)
        alert('添加成就失败')
      }
    },
    editAchievement(achievement) {
      this.editingAchievement = { ...achievement }
    },
    async updateAchievement() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/admin/achievements/${this.editingAchievement.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.editingAchievement)
        })
        if (!response.ok) throw new Error('更新成就失败')
        const updatedAchievement = await response.json()
        const index = this.achievements.findIndex(a => a.id === updatedAchievement.id)
        if (index !== -1) {
          this.achievements[index] = updatedAchievement
        }
        this.editingAchievement = null
        alert('成就更新成功')
      } catch (error) {
        console.error('更新成就失败:', error)
        alert('更新成就失败')
      }
    },
    async deleteAchievement(achievementId) {
      if (!confirm('确定要删除这个成就吗？')) return
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/admin/achievements/${achievementId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('删除成就失败')
        this.achievements = this.achievements.filter(a => a.id !== achievementId)
        alert('成就删除成功')
      } catch (error) {
        console.error('删除成就失败:', error)
        alert('删除成就失败')
      }
    }
  }
}
</script>

<style scoped>
.achievements-container {
  max-width: 1000px;
  margin: 0 auto;
}

.form-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-group textarea {
  height: 100px;
  resize: vertical;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-edit {
  background-color: #2196F3;
  color: white;
  margin-right: 10px;
}

.btn-edit:hover {
  background-color: #0b7dda;
}

.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn-delete:hover {
  background-color: #da190b;
}

.btn-cancel {
  background-color: #9e9e9e;
  color: white;
  margin-left: 10px;
}

.btn-cancel:hover {
  background-color: #757575;
}

.list-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.achievements-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.achievements-table th,
.achievements-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.achievements-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.achievements-table tr:hover {
  background-color: #f5f5f5;
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
  max-width: 600px;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .achievements-table {
    font-size: 14px;
  }
  
  .achievements-table th,
  .achievements-table td {
    padding: 8px;
  }
  
  .btn {
    padding: 8px 12px;
    font-size: 14px;
  }
}
</style>

<template>
  <div class="prizes-container">
    <h2>奖品设置</h2>
    
    <!-- 添加奖品表单 -->
    <div class="form-container">
      <h3>添加新奖品</h3>
      <form @submit.prevent="addPrize">
        <div class="form-group">
          <label for="name">奖品名称</label>
          <input type="text" id="name" v-model="newPrize.name" required>
        </div>
        <div class="form-group">
          <label for="level">奖品级别</label>
          <input type="number" id="level" v-model.number="newPrize.level" min="1" max="5" required>
        </div>
        <div class="form-group">
          <label for="probability">基础概率</label>
          <input type="number" id="probability" v-model.number="newPrize.probability" min="0" max="1" step="0.01" required>
        </div>
        <div class="form-group">
          <label for="description">奖品描述</label>
          <textarea id="description" v-model="newPrize.description"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">添加奖品</button>
      </form>
    </div>
    
    <!-- 奖品列表 -->
    <div class="list-container">
      <h3>奖品列表</h3>
      <table class="prizes-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>奖品名称</th>
            <th>级别</th>
            <th>基础概率</th>
            <th>描述</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="prize in prizes" :key="prize.id">
            <td>{{ prize.id }}</td>
            <td>{{ prize.name }}</td>
            <td>{{ prize.level }}</td>
            <td>{{ prize.probability }}</td>
            <td>{{ prize.description }}</td>
            <td>
              <button @click="editPrize(prize)" class="btn btn-edit">编辑</button>
              <button @click="deletePrize(prize.id)" class="btn btn-delete">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 编辑奖品模态框 -->
    <div v-if="isEditModalVisible" class="modal">
      <div class="modal-content">
        <h3>编辑奖品</h3>
        <form @submit.prevent="updatePrize">
          <div class="form-group">
            <label for="edit-name">奖品名称</label>
            <input type="text" id="edit-name" v-model="editPrize.name" required>
          </div>
          <div class="form-group">
            <label for="edit-level">奖品级别</label>
            <input type="number" id="edit-level" v-model.number="editPrize.level" min="1" max="5" required>
          </div>
          <div class="form-group">
            <label for="edit-probability">基础概率</label>
            <input type="number" id="edit-probability" v-model.number="editPrize.probability" min="0" max="1" step="0.01" required>
          </div>
          <div class="form-group">
            <label for="edit-description">奖品描述</label>
            <textarea id="edit-description" v-model="editPrize.description"></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="isEditModalVisible = false" class="btn btn-cancel">取消</button>
            <button type="submit" class="btn btn-primary">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Prizes',
  data() {
    return {
      prizes: [],
      newPrize: {
        name: '',
        level: 1,
        probability: 0.1,
        description: ''
      },
      editPrize: {
        id: '',
        name: '',
        level: 1,
        probability: 0.1,
        description: ''
      },
      isEditModalVisible: false
    }
  },
  mounted() {
    this.fetchPrizes()
  },
  methods: {
    async fetchPrizes() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/prizes', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('获取奖品列表失败')
        this.prizes = await response.json()
      } catch (error) {
        console.error('获取奖品列表失败:', error)
        alert('获取奖品列表失败')
      }
    },
    async addPrize() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/prizes', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.newPrize)
        })
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.detail || '添加奖品失败')
        }
        const newPrize = await response.json()
        this.prizes.push(newPrize)
        this.newPrize = {
          name: '',
          level: 1,
          probability: 0.1,
          description: ''
        }
        alert('奖品添加成功')
      } catch (error) {
        console.error('添加奖品失败:', error)
        alert(error.message || '添加奖品失败')
      }
    },
    editPrize(prize) {
      this.editPrize = { ...prize }
      this.isEditModalVisible = true
    },
    async updatePrize() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/admin/prizes/${this.editPrize.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.editPrize)
        })
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.detail || '更新奖品失败')
        }
        const updatedPrize = await response.json()
        const index = this.prizes.findIndex(p => p.id === updatedPrize.id)
        if (index !== -1) {
          this.prizes[index] = updatedPrize
        }
        this.isEditModalVisible = false
        alert('奖品更新成功')
      } catch (error) {
        console.error('更新奖品失败:', error)
        alert(error.message || '更新奖品失败')
      }
    },
    async deletePrize(prizeId) {
      if (!confirm('确定要删除这个奖品吗？')) {
        return
      }
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/admin/prizes/${prizeId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('删除奖品失败')
        this.prizes = this.prizes.filter(p => p.id !== prizeId)
        alert('奖品删除成功')
      } catch (error) {
        console.error('删除奖品失败:', error)
        alert('删除奖品失败')
      }
    }
  }
}
</script>

<style scoped>
.prizes-container {
  max-width: 1000px;
  margin: 0 auto;
}

h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 25px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e0e0e0;
}

h3 {
  font-size: 1.4rem;
  color: #555;
  margin-bottom: 15px;
}

.form-container {
  background-color: #ffffff;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.form-group textarea {
  height: 120px;
  resize: vertical;
  font-family: inherit;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-edit {
  background-color: #2196F3;
  color: white;
  margin-right: 10px;
}

.btn-edit:hover {
  background-color: #0b7dda;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn-delete:hover {
  background-color: #da190b;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-cancel {
  background-color: #9e9e9e;
  color: white;
  margin-left: 10px;
}

.btn-cancel:hover {
  background-color: #757575;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.list-container {
  background-color: #ffffff;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.prizes-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border-radius: 6px;
  overflow: hidden;
}

.prizes-table th,
.prizes-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.prizes-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.prizes-table tr:hover {
  background-color: #f8f9fa;
}

.prizes-table tr:last-child td {
  border-bottom: none;
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
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 600px;
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-actions {
  margin-top: 25px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .prizes-container {
    padding: 0 10px;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  h3 {
    font-size: 1.2rem;
  }
  
  .form-container,
  .list-container {
    padding: 20px;
  }
  
  .prizes-table {
    font-size: 14px;
  }
  
  .prizes-table th,
  .prizes-table td {
    padding: 10px;
  }
  
  .btn {
    padding: 8px 16px;
    font-size: 14px;
  }
  
  .modal-content {
    padding: 20px;
  }
}
</style>
<template>
  <div class="stations-container">
    <h2>站点设置</h2>
    
    <!-- 添加站点表单 -->
    <div class="form-container">
      <h3>添加新站点</h3>
      <form @submit.prevent="addStation">
        <div class="form-group">
          <label for="name">站点名称</label>
          <input type="text" id="name" v-model="newStation.name" required>
        </div>
        <div class="form-group">
          <label for="content">站点内容</label>
          <textarea id="content" v-model="newStation.content" required></textarea>
        </div>
        <div class="form-group">
          <label for="position">位置</label>
          <input type="number" id="position" v-model="newStation.position" required>
        </div>
        <button type="submit" class="btn btn-primary">添加站点</button>
      </form>
    </div>
    
    <!-- 站点列表 -->
    <div class="list-container">
      <h3>站点列表</h3>
      <table class="stations-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>名称</th>
            <th>位置</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="station in stations" :key="station.id">
            <td>{{ station.id }}</td>
            <td>{{ station.name }}</td>
            <td>{{ station.position }}</td>
            <td>
              <button @click="editStation(station)" class="btn btn-edit">编辑</button>
              <button @click="deleteStation(station.id)" class="btn btn-delete">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 编辑站点对话框 -->
    <div v-if="editingStation" class="modal">
      <div class="modal-content">
        <h3>编辑站点</h3>
        <form @submit.prevent="updateStation">
          <div class="form-group">
            <label for="edit-name">站点名称</label>
            <input type="text" id="edit-name" v-model="editingStation.name" required>
          </div>
          <div class="form-group">
            <label for="edit-content">站点内容</label>
            <textarea id="edit-content" v-model="editingStation.content" required></textarea>
          </div>
          <div class="form-group">
            <label for="edit-position">位置</label>
            <input type="number" id="edit-position" v-model="editingStation.position" required>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">保存</button>
            <button type="button" @click="editingStation = null" class="btn btn-cancel">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Stations',
  data() {
    return {
      stations: [],
      newStation: {
        name: '',
        content: '',
        position: 1
      },
      editingStation: null
    }
  },
  mounted() {
    this.fetchStations()
  },
  methods: {
    async fetchStations() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/stations', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('获取站点失败')
        this.stations = await response.json()
      } catch (error) {
        console.error('获取站点失败:', error)
        alert('获取站点失败')
      }
    },
    async addStation() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/stations', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.newStation)
        })
        if (!response.ok) throw new Error('添加站点失败')
        const newStation = await response.json()
        this.stations.push(newStation)
        this.newStation = {
          name: '',
          content: '',
          position: 1
        }
        alert('站点添加成功')
      } catch (error) {
        console.error('添加站点失败:', error)
        alert('添加站点失败')
      }
    },
    editStation(station) {
      this.editingStation = { ...station }
    },
    async updateStation() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/admin/stations/${this.editingStation.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.editingStation)
        })
        if (!response.ok) throw new Error('更新站点失败')
        const updatedStation = await response.json()
        const index = this.stations.findIndex(s => s.id === updatedStation.id)
        if (index !== -1) {
          this.stations[index] = updatedStation
        }
        this.editingStation = null
        alert('站点更新成功')
      } catch (error) {
        console.error('更新站点失败:', error)
        alert('更新站点失败')
      }
    },
    async deleteStation(stationId) {
      if (!confirm('确定要删除这个站点吗？')) return
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/admin/stations/${stationId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('删除站点失败')
        this.stations = this.stations.filter(s => s.id !== stationId)
        alert('站点删除成功')
      } catch (error) {
        console.error('删除站点失败:', error)
        alert('删除站点失败')
      }
    }
  }
}
</script>

<style scoped>
.stations-container {
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

.stations-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border-radius: 6px;
  overflow: hidden;
}

.stations-table th,
.stations-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.stations-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stations-table tr:hover {
  background-color: #f8f9fa;
}

.stations-table tr:last-child td {
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
  .stations-container {
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
  
  .stations-table {
    font-size: 14px;
  }
  
  .stations-table th,
  .stations-table td {
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

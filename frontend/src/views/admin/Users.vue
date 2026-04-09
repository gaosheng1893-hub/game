<template>
  <div class="users-container">
    <h2>用户设置</h2>
    
    <!-- 添加用户表单 -->
    <div class="form-container">
      <h3>添加新用户</h3>
      <form @submit.prevent="addUser">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="newUser.username" required>
        </div>
        <div class="form-group">
          <label for="email">邮箱</label>
          <input type="email" id="email" v-model="newUser.email" required>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="newUser.password" required>
        </div>
        <button type="submit" class="btn btn-primary">添加用户</button>
      </form>
    </div>
    
    <!-- 用户列表 -->
    <div class="list-container">
      <h3>用户列表</h3>
      <table class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>总积分</th>
            <th>完成站点数</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.total_score }}</td>
            <td>{{ user.completed_stations }}</td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <button @click="editUser(user)" class="btn btn-edit">编辑</button>
              <button @click="deleteUser(user.id)" class="btn btn-delete">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 编辑用户对话框 -->
    <div v-if="editingUser" class="modal">
      <div class="modal-content">
        <h3>编辑用户</h3>
        <form @submit.prevent="updateUser">
          <div class="form-group">
            <label for="edit-username">用户名</label>
            <input type="text" id="edit-username" v-model="editingUser.username" required>
          </div>
          <div class="form-group">
            <label for="edit-email">邮箱</label>
            <input type="email" id="edit-email" v-model="editingUser.email" required>
          </div>
          <div class="form-group">
            <label for="edit-password">密码</label>
            <input type="password" id="edit-password" v-model="editingUser.password" required>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">保存</button>
            <button type="button" @click="editingUser = null" class="btn btn-cancel">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Users',
  data() {
    return {
      users: [],
      newUser: {
        username: '',
        email: '',
        password: ''
      },
      editingUser: null
    }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/users', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('获取用户失败')
        this.users = await response.json()
      } catch (error) {
        console.error('获取用户失败:', error)
        alert('获取用户失败')
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString()
    },
    async addUser() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/admin/users', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.newUser)
        })
        if (!response.ok) throw new Error('添加用户失败')
        const newUser = await response.json()
        this.users.push(newUser)
        this.newUser = {
          username: '',
          email: '',
          password: ''
        }
        alert('用户添加成功')
      } catch (error) {
        console.error('添加用户失败:', error)
        alert('添加用户失败')
      }
    },
    editUser(user) {
      this.editingUser = { ...user, password: '' }
    },
    async updateUser() {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/admin/users/${this.editingUser.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.editingUser)
        })
        if (!response.ok) throw new Error('更新用户失败')
        const updatedUser = await response.json()
        const index = this.users.findIndex(u => u.id === updatedUser.id)
        if (index !== -1) {
          this.users[index] = updatedUser
        }
        this.editingUser = null
        alert('用户更新成功')
      } catch (error) {
        console.error('更新用户失败:', error)
        alert('更新用户失败')
      }
    },
    async deleteUser(userId) {
      if (!confirm('确定要删除这个用户吗？')) return
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/admin/users/${userId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!response.ok) throw new Error('删除用户失败')
        this.users = this.users.filter(u => u.id !== userId)
        alert('用户删除成功')
      } catch (error) {
        console.error('删除用户失败:', error)
        alert('删除用户失败')
      }
    }
  }
}
</script>

<style scoped>
.users-container {
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

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
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

.users-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.users-table th,
.users-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.users-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.users-table tr:hover {
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
  max-width: 400px;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .users-table {
    font-size: 14px;
  }
  
  .users-table th,
  .users-table td {
    padding: 8px;
  }
  
  .btn {
    padding: 8px 12px;
    font-size: 14px;
  }
}
</style>

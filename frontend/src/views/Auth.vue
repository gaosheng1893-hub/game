<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>{{ isLogin ? '登录' : '注册' }}</h2>
      <form @submit.prevent="handleSubmit">
        <div v-if="!isLogin" class="form-group">
          <label>用户名</label>
          <input type="text" v-model="form.username" required>
        </div>
        <div v-if="!isLogin" class="form-group">
          <label>邮箱</label>
          <input type="email" v-model="form.email" required>
        </div>
        <div v-if="isLogin" class="form-group">
          <label>用户名/邮箱</label>
          <input type="text" v-model="form.username" required>
        </div>
        <div class="form-group">
          <label>密码</label>
          <input type="password" v-model="form.password" required>
        </div>
        <button type="submit" class="submit-btn">{{ isLogin ? '登录' : '注册' }}</button>
      </form>
      <p class="toggle-text">
        {{ isLogin ? '还没有账号？' : '已有账号？' }}
        <span @click="toggleMode">{{ isLogin ? '立即注册' : '立即登录' }}</span>
      </p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import auth from '../services/auth.js'

export default {
  data() {
    return {
      isLogin: true,
      form: {
        username: '',
        email: '',
        password: ''
      },
      error: ''
    }
  },
  methods: {
    async handleSubmit() {
      try {
        this.error = ''
        if (this.isLogin) {
          await auth.login(this.form.username, this.form.password)
        } else {
          await auth.register(this.form.username, this.form.email, this.form.password)
          await auth.login(this.form.username, this.form.password)
        }
        
        const user = await auth.getCurrentUser()
        if (user) {
          this.$router.push('/')
        }
      } catch (error) {
        this.error = error.message
      }
    },
    toggleMode() {
      this.isLogin = !this.isLogin
      this.error = ''
      this.form = {
        username: '',
        email: '',
        password: ''
      }
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-box {
  background: white;
  padding: 2.5rem;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
  font-size: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s;
}

.submit-btn:hover {
  transform: translateY(-2px);
}

.toggle-text {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.toggle-text span {
  color: #667eea;
  cursor: pointer;
  font-weight: 600;
  text-decoration: underline;
}

.error {
  text-align: center;
  color: #f44336;
  margin-top: 1rem;
  padding: 0.8rem;
  background: #ffebee;
  border-radius: 5px;
}
</style>
const API_BASE_URL = 'http://localhost:8000'

class AuthService {
  async register(username, email, password) {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, email, password }),
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || '注册失败')
    }
    
    return response.json()
  }
  
  async login(username, password) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    
    const response = await fetch(`${API_BASE_URL}/token`, {
      method: 'POST',
      body: formData,
    })
    
    if (!response.ok) {
      throw new Error('用户名或密码错误')
    }
    
    const data = await response.json()
    localStorage.setItem('token', data.access_token)
    return data
  }
  
  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
  
  getToken() {
    return localStorage.getItem('token')
  }
  
  isAuthenticated() {
    return !!this.getToken()
  }
  
  isAdmin() {
    const userStr = localStorage.getItem('user')
    if (!userStr) return false
    const user = JSON.parse(userStr)
    return user.username === 'admin'
  }
  
  async getCurrentUser() {
    const token = this.getToken()
    if (!token) return null
    
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    
    if (!response.ok) {
      this.logout()
      return null
    }
    
    const user = await response.json()
    localStorage.setItem('user', JSON.stringify(user))
    return user
  }
  
  async apiRequest(endpoint, options = {}) {
    const token = this.getToken()
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    }
    
    console.log('发送请求:', `${API_BASE_URL}${endpoint}`)
    console.log('请求头:', headers)
    console.log('请求体:', options.body)
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    })
    
    console.log('响应状态:', response.status)
    console.log('响应状态文本:', response.statusText)
    
    if (!response.ok) {
      const error = await response.json()
      console.log('错误信息:', error)
      throw new Error(error.detail || '请求失败')
    }
    
    const data = await response.json()
    console.log('响应数据:', data)
    return data
  }
}

export default new AuthService()
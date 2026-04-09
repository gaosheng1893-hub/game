import auth from './auth.js'

class GameService {
  async getStations() {
    return auth.apiRequest('/stations')
  }
  
  async getStation(stationId) {
    return auth.apiRequest(`/stations/${stationId}`)
  }
  
  async getUserProgress(userId) {
    return auth.apiRequest(`/user-progress/${userId}`)
  }
  
  async submitAnswer(userId, stationId, questionId, answer) {
    return auth.apiRequest('/submit-answer', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, station_id: stationId, question_id: questionId, answer }),
    })
  }
  
  async getUserAchievements(userId) {
    return auth.apiRequest(`/user-achievements/${userId}`)
  }
  
  async getLeaderboard(limit = 10) {
    return auth.apiRequest(`/leaderboard?limit=${limit}`)
  }
  
  async lottery(userId) {
    return auth.apiRequest('/lottery', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    })
  }
  
  async submitAddress(userId, name, phone, address) {
    return auth.apiRequest('/submit-address', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, name, phone, address }),
    })
  }
  
  async getLotteryResult(userId) {
    return auth.apiRequest(`/lottery-result/${userId}`)
  }
  
  async getWinners() {
    return auth.apiRequest('/admin/lottery/winners')
  }
}

export default new GameService()
<template>
  <div class="app">
    <nav v-if="isAuthenticated" class="navbar">
      <div class="nav-brand">地图闯关</div>
      <div class="nav-links">
        <router-link to="/map" class="nav-link">地图</router-link>
        <router-link to="/achievements" class="nav-link">成就</router-link>
        <router-link to="/leaderboard" class="nav-link">排行榜</router-link>
        <router-link v-if="canLottery || isAdmin" to="/lottery" class="nav-link">抽奖</router-link>
        <router-link v-if="isAdmin" to="/admin" class="nav-link">管理后台</router-link>
        <button @click="logout" class="logout-btn">退出</button>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
import auth from './services/auth.js'

export default {
  data() {
    return {
      isAuthenticated: auth.isAuthenticated(),
      canLottery: false,
      isAdmin: auth.isAdmin()
    }
  },
  async mounted() {
    await this.checkAuthStatus()
  },
  watch: {
    '$route': {
      handler: async function() {
        await this.checkAuthStatus()
      },
      immediate: true
    }
  },
  methods: {
    async checkAuthStatus() {
      this.isAuthenticated = auth.isAuthenticated()
      this.isAdmin = auth.isAdmin()
      if (this.isAuthenticated) {
        const user = await auth.getCurrentUser()
        if (this.isAdmin || (user && user.completed_stations >= 5)) {
          this.canLottery = true
        } else {
          this.canLottery = false
        }
      } else {
        this.canLottery = false
        this.isAdmin = false
      }
    },
    logout() {
      auth.logout()
      this.isAuthenticated = false
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-brand {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.logout-btn {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
</style>
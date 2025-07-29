<template>
  <div id="app">
    <nav style="background-color: #333; padding: 10px;">
      <div class="nav-container">
        <h1 style="color: white; display: inline;">Text Ledger</h1>
        <div style="float: right;">
          <router-link v-if="!isLoggedIn" to="/login" class="nav-link">Login</router-link>
          <router-link v-if="!isLoggedIn" to="/register" class="nav-link">Register</router-link>
          <router-link v-if="isLoggedIn" to="/" class="nav-link">Ledger</router-link>
          <router-link v-if="isLoggedIn" to="/users" class="nav-link">Users</router-link>
          <button v-if="isLoggedIn" @click="logout" class="nav-link" style="background: none; border: none; color: white; cursor: pointer;">Logout</button>
        </div>
      </div>
    </nav>
    
    <router-view/>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      user: null
    }
  },
  created() {
    this.checkLoginStatus()
  },
  methods: {
    checkLoginStatus() {
      axios.get('/api/me/')
        .then(response => {
          if (response.data.success) {
            this.isLoggedIn = true
            this.user = response.data.user
            this.$root.$user = response.data.user
            this.$root.$isLoggedIn = true
          }
        })
        .catch(error => {
          console.log('Not logged in')
          this.isLoggedIn = false
          this.user = null
        })
    },
    logout() {
      axios.post('/api/logout/')
        .then(response => {
          this.isLoggedIn = false
          this.user = null
          this.$root.$user = null
          this.$root.$isLoggedIn = false
          window.location.href = '/login'
        })
        .catch(error => {
          alert('Logout failed!')
        })
    }
  },
  watch: {
    $route() {
      this.checkLoginStatus()
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f0f0f0;
}

#app {
  min-height: 100vh;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
}

.nav-link {
  color: white;
  text-decoration: none;
  margin-left: 20px;
  padding: 5px 10px;
}

.nav-link:hover {
  background-color: #555;
  border-radius: 3px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
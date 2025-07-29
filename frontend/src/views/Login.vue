<template>
  <div class="login-page" style="padding: 50px;">
    <div class="login-container" style="max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 5px;">
      <h2 style="text-align: center; margin-bottom: 30px;">Login</h2>
      
      <form @submit.prevent="handleLogin">
        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px;">Email:</label>
          <input 
            type="text" 
            v-model="email" 
            style="width: 100%; padding: 8px; border: 1px solid #ccc;"
            placeholder="Enter your email"
          />
        </div>
        
        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px;">Password:</label>
          <input 
            type="password" 
            v-model="password" 
            style="width: 100%; padding: 8px; border: 1px solid #ccc;"
            placeholder="Enter your password"
          />
        </div>
        
        <div v-if="error" style="color: red; margin-bottom: 15px;">
          {{ error }}
        </div>
        
        <button 
          type="submit" 
          style="width: 100%; padding: 10px; background-color: #333; color: white; border: none; cursor: pointer;"
          :disabled="loading"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      
      <p style="text-align: center; margin-top: 20px;">
        Don't have an account? 
        <router-link to="/register" style="color: #333;">Register here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      loading: false
    }
  },
  methods: {
    handleLogin() {
      this.error = ''
      
      if (!this.email) {
        this.error = 'Email is required'
        return
      }
      
      if (!this.password) {
        this.error = 'Password is required'
        return
      }
      
      this.loading = true
      
      const loginData = {
        email: this.email,
        password: this.password
      }
      
      axios.post('/api/login/', loginData)
        .then(response => {
          console.log('Login response:', response)
          
          if (response.data.success) {
            this.$root.$user = response.data.user
            this.$root.$isLoggedIn = true
            
            setTimeout(() => {
              this.$router.push('/')
            }, 500)
          } else {
            this.error = response.data.message || 'Login failed'
          }
          
          this.loading = false
        })
        .catch(error => {
          console.error('Login error:', error)
          this.error = error.response?.data?.message || 'Login failed. Please try again.'
          this.loading = false
        })
    }
  },
  mounted() {
    console.log('Login component mounted')
  },
  beforeUnmount() {
    console.log('Login component unmounting')
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 60px);
  background-color: #f0f0f0;
}

input {
  font-size: 14px;
}

button:hover {
  background-color: #555 !important;
}
</style>
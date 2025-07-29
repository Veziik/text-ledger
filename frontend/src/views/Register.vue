<template>
  <div class="register-page" style="padding: 50px;">
    <div class="register-container" style="max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 5px;">
      <h2 style="text-align: center; margin-bottom: 30px;">Register</h2>
      
      <form @submit.prevent="handleRegister">
        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px;">Email:</label>
          <input 
            type="text" 
            v-model="formData.email" 
            style="width: 100%; padding: 8px; border: 1px solid #ccc;"
            placeholder="Enter your email"
          />
        </div>
        
        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px;">Password:</label>
          <input 
            type="password" 
            v-model="formData.password" 
            style="width: 100%; padding: 8px; border: 1px solid #ccc;"
            placeholder="Enter your password"
          />
        </div>
        
        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px;">Confirm Password:</label>
          <input 
            type="password" 
            v-model="confirmPassword" 
            style="width: 100%; padding: 8px; border: 1px solid #ccc;"
            placeholder="Confirm your password"
          />
        </div>
        
        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px;">First Name:</label>
          <input 
            type="text" 
            v-model="formData.first_name" 
            style="width: 100%; padding: 8px; border: 1px solid #ccc;"
            placeholder="Enter your first name"
          />
        </div>
        
        <div style="margin-bottom: 15px;">
          <label style="display: block; margin-bottom: 5px;">Last Name:</label>
          <input 
            type="text" 
            v-model="formData.last_name" 
            style="width: 100%; padding: 8px; border: 1px solid #ccc;"
            placeholder="Enter your last name"
          />
        </div>
        
        <div v-if="errors.length > 0" style="margin-bottom: 15px;">
          <div v-for="(error, index) in errors" :key="index" style="color: red;">
            {{ error }}
          </div>
        </div>
        
        <button 
          type="submit" 
          style="width: 100%; padding: 10px; background-color: #333; color: white; border: none; cursor: pointer;"
          :disabled="loading"
        >
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
      </form>
      
      <p style="text-align: center; margin-top: 20px;">
        Already have an account? 
        <router-link to="/login" style="color: #333;">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegisterView',
  data() {
    return {
      formData: {
        email: '',
        password: '',
        first_name: '',
        last_name: ''
      },
      confirmPassword: '',
      errors: [],
      loading: false
    }
  },
  methods: {
    validateForm() {
      this.errors = []
      
      if (!this.formData.email) {
        this.errors.push('Email is required')
      } else if (!this.formData.email.includes('@')) {
        this.errors.push('Please enter a valid email')
      }
      
      if (!this.formData.password) {
        this.errors.push('Password is required')
      } else if (this.formData.password.length < 6) {
        this.errors.push('Password must be at least 6 characters')
      }
      
      if (this.formData.password !== this.confirmPassword) {
        this.errors.push('Passwords do not match')
      }
      
      return this.errors.length === 0
    },
    handleRegister() {
      if (!this.validateForm()) {
        return
      }
      
      this.loading = true
      
      axios.post('/api/register/', this.formData)
        .then(response => {
          console.log('Register response:', response)
          
          if (response.data.success) {
            alert('Registration successful! Please login.')
            
            setTimeout(() => {
              this.$router.push('/login')
            }, 1000)
          } else {
            if (response.data.errors) {
              this.errors = response.data.errors
            } else {
              this.errors = ['Registration failed']
            }
          }
          
          this.loading = false
        })
        .catch(error => {
          console.error('Register error:', error)
          
          if (error.response?.data?.errors) {
            this.errors = error.response.data.errors
          } else {
            this.errors = ['Registration failed. Please try again.']
          }
          
          this.loading = false
        })
    }
  }
}
</script>

<style scoped>
.register-page {
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
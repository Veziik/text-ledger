<template>
  <div class="user-detail-page" style="padding: 20px;">
    <div class="container" style="max-width: 800px; margin: 0 auto;">
      <div v-if="!isLoggedIn" style="background: #f9f9f9; padding: 20px; border-radius: 5px;">
        <p>Please <router-link to="/login">login</router-link> to view user details.</p>
      </div>
      
      <div v-else>
        <div v-if="loading" style="text-align: center; padding: 50px;">
          Loading user details...
        </div>
        
        <div v-else-if="user" style="background: white; padding: 30px; border-radius: 5px;">
          <button 
            @click="goBack" 
            style="margin-bottom: 20px; padding: 5px 15px; background: #666; color: white; border: none; cursor: pointer;"
          >
            Back to Users
          </button>
          
          <h2>User Details</h2>
          
          <div style="margin: 20px 0;">
            <div style="padding: 20px; background: #f9f9f9; border-radius: 5px;">
              <h3 style="margin-bottom: 15px;">{{ user.full_name || 'No Name' }}</h3>
              
              <div style="margin-bottom: 10px;">
                <strong>Email:</strong> {{ user.email }}
              </div>
              
              <div style="margin-bottom: 10px;">
                <strong>User ID:</strong> {{ user.id }}
              </div>
              
              <div style="margin-bottom: 10px;">
                <strong>First Name:</strong> {{ user.first_name || 'Not provided' }}
              </div>
              
              <div style="margin-bottom: 10px;">
                <strong>Last Name:</strong> {{ user.last_name || 'Not provided' }}
              </div>
              
              <div style="margin-bottom: 10px;">
                <strong>Joined:</strong> {{ formatDate(user.date_joined) }}
              </div>
              
              <div style="margin-bottom: 10px;">
                <strong>Status:</strong> 
                <span v-if="user.is_active" style="color: green; font-weight: bold;">Active</span>
                <span v-else style="color: red; font-weight: bold;">Inactive</span>
              </div>
              
              <div style="margin-bottom: 10px;">
                <strong>Ledger Entries:</strong> {{ user.ledger_count || 0 }}
              </div>
            </div>
            
            <div style="margin-top: 20px; padding: 20px; background: #f0f0f0; border-radius: 5px;">
              <h4>Recent Activity</h4>
              <p style="color: #666;">Feature coming soon...</p>
            </div>
          </div>
        </div>
        
        <div v-else style="text-align: center; padding: 50px;">
          <p>User not found.</p>
          <button 
            @click="goBack" 
            style="margin-top: 20px; padding: 10px 20px; background: #333; color: white; border: none; cursor: pointer;"
          >
            Back to Users
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserDetailView',
  data() {
    return {
      user: null,
      loading: true,
      isLoggedIn: false,
      userId: null,
      activities: [],
      stats: {}
    }
  },
  created() {
    this.userId = this.$route.params.id
    this.checkAuthAndFetch()
  },
  methods: {
    checkAuthAndFetch() {
      this.isLoggedIn = this.$root.$isLoggedIn || false
      
      if (this.isLoggedIn) {
        this.fetchUserDetails()
      } else {
        this.loading = false
      }
    },
    fetchUserDetails() {
      const apiUrl = '/api/users/' + this.userId + '/'
      
      axios.get(apiUrl)
        .then(response => {
          console.log('User detail response:', response.data)
          
          if (response.data.success) {
            this.user = response.data.user
          } else {
            console.error('Failed to get user')
          }
          
          this.loading = false
        })
        .catch(error => {
          console.error('Error fetching user:', error)
          
          if (error.response?.status === 401) {
            this.isLoggedIn = false
            alert('Session expired. Please login again.')
            this.$router.push('/login')
          } else if (error.response?.status === 404) {
            alert('User not found!')
          }
          
          this.loading = false
        })
    },
    goBack() {
      this.$router.push('/users')
    },
    formatDate(dateString) {
      if (!dateString) return 'Unknown'
      
      const date = new Date(dateString)
      const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }
      
      return date.toLocaleDateString('en-US', options)
    }
  },
  computed: {
    userDisplayName() {
      if (!this.user) return ''
      return this.user.full_name || this.user.email
    }
  }
}
</script>

<style scoped>
button:hover {
  opacity: 0.8;
}

h2, h3, h4 {
  color: #333;
}
</style>
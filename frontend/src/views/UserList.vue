<template>
  <div class="user-list-page" style="padding: 20px;">
    <div class="container" style="max-width: 1200px; margin: 0 auto;">
      <h1>Users</h1>
      
      <div v-if="!isLoggedIn" style="background: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 5px;">
        <p>Please <router-link to="/login">login</router-link> to view users.</p>
      </div>
      
      <div v-else>
        <div v-if="loading" style="text-align: center; padding: 50px;">
          Loading users...
        </div>
        
        <div v-else-if="users.length > 0">
          <p style="margin-bottom: 20px;">Total users: {{ users.length }}</p>
          
          <table style="width: 100%; background: white; border-collapse: collapse;">
            <thead>
              <tr style="background: #f0f0f0;">
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">ID</th>
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Name</th>
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Email</th>
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Joined</th>
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Status</th>
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id" style="border-bottom: 1px solid #eee;">
                <td style="padding: 10px;">{{ user.id }}</td>
                <td style="padding: 10px;">{{ user.full_name || 'N/A' }}</td>
                <td style="padding: 10px;">{{ user.email }}</td>
                <td style="padding: 10px;">{{ formatDate(user.date_joined) }}</td>
                <td style="padding: 10px;">
                  <span v-if="user.is_active" style="color: green;">Active</span>
                  <span v-else style="color: red;">Inactive</span>
                </td>
                <td style="padding: 10px;">
                  <button 
                    @click="viewUser(user.id)" 
                    style="padding: 5px 10px; background: #333; color: white; border: none; cursor: pointer;"
                  >
                    View Details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-else style="text-align: center; padding: 50px;">
          <p>No users found.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserListView',
  data() {
    return {
      users: [],
      loading: true,
      isLoggedIn: false,
      sortBy: 'id',
      sortOrder: 'asc'
    }
  },
  created() {
    this.checkAuth()
  },
  methods: {
    checkAuth() {
      this.isLoggedIn = this.$root.$isLoggedIn || false
      
      if (this.isLoggedIn) {
        this.fetchUsers()
      } else {
        this.loading = false
      }
    },
    fetchUsers() {
      axios.get('/api/users/')
        .then(response => {
          console.log('Users response:', response.data)
          
          if (response.data.success) {
            this.users = response.data.users.map(user => {
              return {
                ...user,
                displayName: user.full_name || user.email
              }
            })
          }
          
          this.loading = false
        })
        .catch(error => {
          console.error('Error fetching users:', error)
          
          if (error.response?.status === 401) {
            this.isLoggedIn = false
            alert('Please login to view users')
          }
          
          this.loading = false
        })
    },
    viewUser(userId) {
      this.$router.push({
        name: 'user-detail',
        params: { id: userId }
      })
    },
    formatDate(dateString) {
      if (!dateString) return 'Unknown'
      
      const date = new Date(dateString)
      
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }
  },
  watch: {
    '$root.$isLoggedIn'(newVal) {
      if (newVal && !this.isLoggedIn) {
        this.isLoggedIn = true
        this.fetchUsers()
      } else if (!newVal) {
        this.isLoggedIn = false
        this.users = []
      }
    }
  }
}
</script>

<style scoped>
table {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

tr:hover {
  background-color: #f9f9f9;
}
</style>
<template>
  <div class="ledger-list-page" style="padding: 20px;">
    <div class="container" style="max-width: 1200px; margin: 0 auto;">
      <h1>Text Ledger</h1>
      
      <div v-if="isLoggedIn" class="add-ledger-section" style="background: white; padding: 20px; margin: 20px 0; border-radius: 5px;">
        <h3>Add New Entry</h3>
        <form @submit.prevent="addLedgerItem">
          <textarea 
            v-model="newItemContent" 
            style="width: 100%; padding: 10px; border: 1px solid #ccc; min-height: 100px;"
            placeholder="Enter your ledger entry..."
          ></textarea>
          <button 
            type="submit" 
            style="margin-top: 10px; padding: 10px 20px; background-color: #333; color: white; border: none; cursor: pointer;"
          >
            Add Entry
          </button>
        </form>
        
        <div v-if="addError" style="color: red; margin-top: 10px;">
          {{ addError }}
        </div>
      </div>
      
      <div v-else style="background: #f9f9f9; padding: 20px; margin: 20px 0; border-radius: 5px;">
        <p>Please <router-link to="/login">login</router-link> to add entries to the ledger.</p>
      </div>
      
      <div v-if="loading" style="text-align: center; padding: 50px;">
        Loading ledger items...
      </div>
      
      <div v-else-if="ledgerItems.length > 0">
        <h2>All Entries ({{ ledgerItems.length }})</h2>
        
        <div v-for="item in ledgerItems" :key="item.item_id" class="ledger-item" style="background: white; padding: 15px; margin: 10px 0; border-radius: 5px; cursor: pointer;" @click="goToDetail(item.item_id)">
          <div style="display: flex; justify-content: space-between;">
            <div>
              <strong>{{ item.author_name || 'Unknown' }}</strong> 
              <span style="color: #666;">{{ item.author_email }}</span>
            </div>
            <div style="color: #999;">
              {{ formatDate(item.created_datetime) }}
            </div>
          </div>
          <div style="margin-top: 10px;">
            {{ item.preview || item.contents }}
          </div>
        </div>
      </div>
      
      <div v-else style="text-align: center; padding: 50px;">
        <p>No ledger entries yet.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LedgerListView',
  data() {
    return {
      ledgerItems: [],
      loading: true,
      isLoggedIn: false,
      newItemContent: '',
      addError: '',
      totalCount: 0
    }
  },
  created() {
    this.checkLogin()
    this.fetchLedgerItems()
    
    this.pollInterval = setInterval(() => {
      this.fetchLedgerItems()
    }, 30000) // Every 30 seconds
  },
  beforeUnmount() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval)
    }
  },
  methods: {
    checkLogin() {
      this.isLoggedIn = this.$root.$isLoggedIn || false
    },
    fetchLedgerItems() {
      axios.get('/api/ledger/')
        .then(response => {
          console.log('Ledger items:', response.data)
          
          if (response.data.success) {
            this.ledgerItems = response.data.items
            this.totalCount = response.data.count
          }
          
          this.loading = false
        })
        .catch(error => {
          console.error('Error fetching ledger items:', error)
          this.loading = false
        })
    },
    addLedgerItem() {
      this.addError = ''
      
      if (!this.newItemContent.trim()) {
        this.addError = 'Please enter some content'
        return
      }
      
      const data = {
        contents: this.newItemContent
      }
      
      axios.post('/api/ledger/create/', data)
        .then(response => {
          if (response.data.success) {
            this.newItemContent = ''
            this.fetchLedgerItems()
            
            alert('Entry added successfully!')
          } else {
            this.addError = response.data.message || 'Failed to add entry'
          }
        })
        .catch(error => {
          console.error('Error adding ledger item:', error)
          
          if (error.response?.status === 401) {
            this.addError = 'Please login to add entries'
            this.isLoggedIn = false
          } else {
            this.addError = 'Failed to add entry. Please try again.'
          }
        })
    },
    goToDetail(itemId) {
      this.$router.push('/ledger/' + itemId)
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      const month = date.getMonth() + 1
      const day = date.getDate()
      const year = date.getFullYear()
      const hours = date.getHours()
      const minutes = date.getMinutes()
      
      return month + '/' + day + '/' + year + ' ' + hours + ':' + minutes
    }
  },
  watch: {
    '$root.$isLoggedIn'(newVal) {
      this.isLoggedIn = newVal
    }
  }
}
</script>

<style scoped>
.ledger-item:hover {
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transform: translateY(-2px);
  transition: all 0.3s;
}
</style>
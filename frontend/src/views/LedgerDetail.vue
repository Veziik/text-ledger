<template>
  <div class="ledger-detail-page" style="padding: 20px;">
    <div class="container" style="max-width: 800px; margin: 0 auto;">
      <div v-if="loading" style="text-align: center; padding: 50px;">
        Loading ledger item...
      </div>
      
      <div v-else-if="ledgerItem" style="background: white; padding: 30px; border-radius: 5px;">
        <button 
          @click="goBack" 
          style="margin-bottom: 20px; padding: 5px 15px; background: #666; color: white; border: none; cursor: pointer;"
        >
          Back to List
        </button>
        
        <h2>Ledger Entry #{{ ledgerItem.item_id }}</h2>
        
        <div style="margin: 20px 0; padding: 20px; background: #f9f9f9; border-radius: 5px;">
          <div style="margin-bottom: 15px;">
            <strong>Author:</strong> 
            <span @click="goToUser(ledgerItem.author_id)" style="color: #333; cursor: pointer; text-decoration: underline;">
              {{ ledgerItem.author_name }} ({{ ledgerItem.author_email }})
            </span>
          </div>
          
          <div style="margin-bottom: 15px;">
            <strong>Created:</strong> {{ ledgerItem.formatted_date || formatDate(ledgerItem.created_datetime) }}
          </div>
          
          <div>
            <strong>Content:</strong>
            <div style="margin-top: 10px; padding: 15px; background: white; border: 1px solid #ddd; border-radius: 3px;">
              {{ ledgerItem.contents }}
            </div>
          </div>
        </div>
        
        <div style="margin-top: 20px; color: #666; font-size: 14px;">
          <p>Entry ID: {{ ledgerItem.item_id }}</p>
          <p>Character count: {{ ledgerItem.contents ? ledgerItem.contents.length : 0 }}</p>
        </div>
      </div>
      
      <div v-else style="text-align: center; padding: 50px;">
        <p>Ledger item not found.</p>
        <button 
          @click="goBack" 
          style="margin-top: 20px; padding: 10px 20px; background: #333; color: white; border: none; cursor: pointer;"
        >
          Back to List
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LedgerDetailView',
  data() {
    return {
      ledgerItem: null,
      loading: true,
      itemId: null
    }
  },
  created() {
    this.itemId = this.$route.params.id
    this.fetchLedgerItem()
  },
  methods: {
    fetchLedgerItem() {
      const url = '/api/ledger/' + this.itemId + '/'
      
      axios.get(url)
        .then(response => {
          console.log('Ledger item detail:', response.data)
          
          if (response.data.success !== false) {
            this.ledgerItem = response.data
          }
          
          this.loading = false
        })
        .catch(error => {
          console.error('Error fetching ledger item:', error)
          this.loading = false
          
          if (error.response?.status === 404) {
            alert('Ledger item not found!')
          }
        })
    },
    goBack() {
      window.history.back()
    },
    goToUser(userId) {
      if (this.$root.$isLoggedIn) {
        this.$router.push('/users/' + userId)
      } else {
        alert('Please login to view user details')
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'Unknown'
      
      const date = new Date(dateString)
      const month = date.getMonth() + 1
      const day = date.getDate()
      const year = date.getFullYear()
      const hours = date.getHours()
      const minutes = date.getMinutes()
      
      return month + '/' + day + '/' + year + ' at ' + hours + ':' + minutes
    }
  },
  computed: {
    hasContent() {
      return this.ledgerItem && this.ledgerItem.contents
    }
  }
}
</script>

<style scoped>
button:hover {
  opacity: 0.8;
}
</style>
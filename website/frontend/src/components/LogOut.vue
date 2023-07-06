<template>
  <div>
    <!-- Other content -->
    <div v-if="loggedIn">
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      loggedIn: false // Initially set to false when the user is not logged in
    }
  },
  mounted () {
    this.checkLoggedIn()
  },
  methods: {
    checkLoggedIn () {
      const token = localStorage.getItem('token')
      if (token) {
        axios
          .get('', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
      } else {
        this.loggedIn = false
      }
    },
    logout () {
      // Handle the logout functionality
      // For example, you can clear the token from localStorage and redirect the user to the login page
      localStorage.removeItem('token') // Example: Remove the token from localStorage
      // Redirect the user to the login page
      this.$router.push('/login')
    }
  }
}
</script>

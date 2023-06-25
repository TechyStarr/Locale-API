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
        // Assuming you have a route in your backend to validate the token
        // You can send an AJAX request to the backend to validate the token
        // Replace 'YOUR_BACKEND_ENDPOINT' with the appropriate endpoint URL
        axios
          .get('http://127.0.0.1:5000/auth/validate_token', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
          .then(response => {
            // Token is valid, user is authenticated
            this.loggedIn = true
          })
          .catch(error => {
            if (error.response.status === 401) {
              // Token is either expired or invalid, user is not authenticated
              this.loggedIn = false
            } else {
              // Handle other errors
              console.log(error)
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

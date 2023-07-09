<template>
  <div class="login-container">
    <h1>Sign into your account</h1>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <div class="form-group">
        <button type="submit">Sign In</button>
      </div>
      <router-link to="/register">
        <span class="log-alt">Don't have an account? Register Now</span>
      </router-link>
    </form>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  data () {
    return {
      // isLoggedIn: false,
      email: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    login () {
      // Reset error message
      this.errorMessage = ''

      // Make API request to Login
      axios.post('https://locale-lkbw.onrender.com/auth/login', {
        email: this.email,
        password: this.password
      })
        .then(response => {
        // Successful login, redirect to home page
          console.log('Logged in successfully')
          this.$router.push('/') // Redirect to home page

          // Store the token in the localstorage
          // localStorage.setItem('token', response.data.access_token)

          // Set the logged in status to true
          // this.isLoggedIn = true
        })
        .catch(error => {
          if (error.response.status === 401) {
            // Invalid credentials, set error message
            this.errorMessage = 'Invalid email or password.'
          } else {
            // Handle other errors
            console.log(error)
            this.errorMessage = error.message
          }
          // Handle the error here
          console.log('Error: ', error.message)
        })
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 4px;
  display: block;
}
h1 {
  display: flex;
  justify-content: center;
  padding: 2rem;
  margin-bottom: 20px;
}
.form-group {
  margin-bottom: 32px;
  display: flex;
  flex-direction: column;

}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px;
  align-self: flex-start;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: 30rem;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 31.4rem;
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.log-alt {
  display: flex;
  justify-content: center;
  padding: 2rem;
  margin-bottom: 20px;
  color: #f44336;
  font-weight: bold;
  text-decoration: none;
}

.error-message {
  color: red;
  margin-top: 10px;
}

</style>

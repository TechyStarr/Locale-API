<template>
    <div class="login-container">
      <h1>Login</h1>
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
          <button type="submit">Login</button>
        </div>
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
      email: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    login () {
      // Reset error message
      this.errorMessage = ''

      // Make API request to login
      axios.post('http://127.0.0.1:5000/auth/login', {
        email: this.email,
        password: this.password
      })
        .then(response => {
        // Successful login, redirect to home page
          console.log('Login successful')
          this.$router.push('/') // Redirect to home page
        })
        // .catch(error => {
        //   // Invalid credentials, set error message
        //   this.errorMessage = 'Invalid email or password.'
        // })
        .catch(error => {
          // Handle the error here
          console.log('Error: ', error)
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
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  h1 {
    text-align: center;
  }
  .form-group {
    margin-bottom: 20px;
  }
  label {
    display: block;
    font-weight: bold;
  }

  input[type="email"],
  input[type="password"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .error-message {
    color: red;
    margin-top: 10px;
  }
</style>

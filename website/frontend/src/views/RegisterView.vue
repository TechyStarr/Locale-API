<template>
    <div class="register-container">
      <h1>Get Started Now</h1>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="username" id="username" v-model="username" required>
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <div class="form-group">
          <button type="submit">Register</button>
        </div>
        <router-link to="/login">
          <span class="log-alt">Already have an account? Sign In</span>
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
      username: '',
      email: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    register () {
      // Reset error message
      this.errorMessage = ''

      // Make API request to Register
      axios.post('http://127.0.0.1:5000/auth/signup', {
        username: this.username,
        email: this.email,
        password: this.password
      })
        .then(response => {
        // Successful login, redirect to home page
          console.log('Registered successfully')
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
.register-container {
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

input[type="username"],
input[type="email"],
input[type="password"] {
  width: 30rem;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
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

button {
  width: 31.4rem;
  padding: 10px 20px;
  background-color: #f44336;
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

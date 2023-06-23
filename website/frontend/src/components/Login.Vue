<template>
  <div>
    <h1>Login Page</h1>
    <form @submit.prevent="login">
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <div>
        <button type="submit">Login</button>
      </div>
    </form>
    <div v-if="loginError" class="error-message">
      {{ loginError }}
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      loginError: ''
    };
  },
  methods: {
    login() {
      // Reset error message
      this.loginError = '';
      

      // make an API call to the backend
      axios.post('http://127.0.0.1:5000/auth/login', {
        email: this.email,
        password: this.password
      })
        .then(response => {
          // Successful login, redirect to home page
          console.log('Login successful');
          this.$router.push('/'); // Redirect to home page
        })
        .catch(error => {
          // Invalid credentials, set error message
          this.loginError = 'Invalid email or password.';
        });


      // Perform login logic
      // Replace this code with your actual login API call or authentication logic
      if (this.email === 'user@example.com' && this.password === 'password') {
        // Successful login
        console.log('Login successful');
        // Redirect to another page or perform desired action
      } else {
        // Invalid credentials
        this.loginError = 'Invalid email or password.';
      }
    }
  }
}
</script>

<style>
/* Login page styles */
.error-message {
  color: red;
  margin-top: 10px;
}
</style>

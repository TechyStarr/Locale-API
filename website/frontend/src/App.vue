<template>
  <nav>
    <div class="logo">
      <i class="fas fa-rocket"></i> <!-- Replace "fa-rocket" with the desired icon from Font Awesome -->
    </div>
    <!-- <div class="logo"> -->
        <!-- <img src="/assets/logo.png" alt="logo" width="50px" height="50px">
        <span>Locale</span> -->
    <!-- </div>  -->
    <router-link to="/">
        <span class="nav-tab">Home</span>
      </router-link>
    <router-link to="/developer">
        <span class="nav-tab">Developer</span>
    </router-link>
    <router-link to="/fun">
        <span class="nav-tab">Fun</span>
    </router-link>
    <div>
      <router-link v-if="!isLoggedIn" to="/login">
        <span class="nav2">Sign In</span>
      </router-link>
    </div>
  </nav>
  <router-view/>
</template>

<script>
// import Login from './views/LoginView.vue'
// import { library } from '@fortawesome/fontawesome-svg-core'
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// import { faRocket } from '@fortawesome/free-solid-svg-icons'

// library.add(faRocket)

export default {
  name: 'App',
  components: {
    // Login
    // FontAwesomeIcon,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

/* .logo {
  padding: 30px;
  font-size: 1.2rem;
  font-weight: 300;
  margin-top: 0.5rem;
  float: left;
} */

.logo {
  font-size: 2rem; /* Adjust the size of the logo */
  color: #ff0000; /* Adjust the color of the logo */
  /* Add any other styling properties as per your design */
}

.nav-tab {
  padding: 30px;
  padding-left: 2rem;
  float: left;
  display: flex;
  justify-content: space-between;
}

.nav1 {
  padding: 30px;
  padding-left: 2rem;
  float: left;
  display: flex;
  justify-content: space-between;
}

.nav2 {
  font-weight: bold;
  padding: 30px;
  float: right;
  padding: 10px 20px;
  /* background-color: #f44336; */
  color: #2c3e50;
  border: 1px solid #ccc;
  border-radius: 4px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

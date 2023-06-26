<template>
  <div class="home">
    <div>
    <div class="header-text">
      <h1>Locale, your best bet to knowing Nigeria well</h1>
      <!-- <h2>Search for any location in Nigeria</h2> -->
    </div>
    <div>
      <router-link to="/register">
      <button class="get-started-btn">Get Started</button>
    </router-link>
    </div>
      <input type="text" v-model="searchQuery" placeholder="Search for locations in nigeria" class="search-input" @keyup.enter="performSearch">
      <button @click="performSearch" class="search-button">Search</button>
      <div v-if="searchResults">
        <ul>
          <li v-for="result in searchResults" :key="result.id">
            {{ result.name }}
          </li>
        </ul>
      </div>
      <search-component></search-component>
    </div>
    <log-out></log-out>
  </div>
</template>

<script>
import LogOut from '@/components/LogOut.vue'
import SearchComponent from '@/components/SearchComponent.vue'
// import RegisterView from './RegisterView.vue'

export default {
  name: 'HomeView',
  components: {
    LogOut,
    SearchComponent
    // RegisterView
  },
  data () {
    return {
      searchQuery: '',
      searchResults: null
    }
  }
}
</script>

<style>
.header-text {
  font-size: 1.2rem;
  font-weight: 300;
  margin-top: 4rem;
  display: flex;
  justify-content: center;
  align-items: center;
  /* padding-bottom: 2rem; */
}

.get-started-btn {
  padding: 10px 20px;
  background-color: #f44336;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 4rem;
}

.search-input {
  padding: 10px 4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-button {
  padding: 10px 20px;
  background-color: #f44336;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>

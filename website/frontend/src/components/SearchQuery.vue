<template>
    <div class="search-app">
      <h1>Search App</h1>
      <input v-model="keyword" type="text" placeholder="Enter search keyword" />
      <button @click="search">Search</button>
      <ul v-if="searchResults.length">
        <li v-for="result in searchResults" :key="result.name">{{ result.name }}</li>
      </ul>
    </div>
  </template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      keyword: '',
      searchResults: []
    }
  },
  methods: {
    search () {
      axios.post('/api/search', { keyword: this.keyword })
        .then(response => {
          this.searchResults = response.data.results
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>

  <style>
  .search-app {
    text-align: center;
  }
  </style>

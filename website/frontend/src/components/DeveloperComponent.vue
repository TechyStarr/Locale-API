<template>
    <div class="home">
      <div class="header-text">
        <h1>Developer content</h1>
      </div>
      <!-- <input type="text" v-model="apiKey" placeholder="Search for locations in nigeria" class="search-input" @keyup.enter="search"> -->
      <button @click="generateApiKey" class="search-button">Generate Api Key</button>
      <div v-if="apiKey">
        <ul>
          <li v-for="result in apiKey" :key="result.id">
            {{ result.key }}
          </li>
        </ul>
      </div>
    </div>
  </template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      apiKey: ''
    }
  },

  methods: {
    generateApiKey () {
      // Make API call to generate API key
      axios.post('http://127.0.0.1:5000/auth/generate-api-key')
        .then(response => {
          this.places = response.data
        })
        .catch(error => {
          console.error('Could not generate api key:', error)
        })
    }
  }
}
</script>

<style>
.header-text {
  font-size: 1.6rem;
  font-weight: 300;
  margin-top: 12rem;
  /* display: flex;
  justify-content: center;
  align-items: center; */
  /* white-space: ; */
  /* padding-bottom: 2rem; */
}
</style>

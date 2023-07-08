<template>
    <div class="home">
      <div class="header-text">
        <h1>Developer content</h1>
      </div>
      <button @click="generateApiKey" class="search-button">Generate Api Key</button>
      <api-key-modal :api-key="generatedApiKey" v-if="generatedApiKey" />
      <div v-if="apiKey">
          <div class="key" v-for="result in apiKey" :key="result.id">
            <p v-if="apiKey"> Copy your API Key</p>
            {{ apiKey }}
          </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios'
import ApiKeyModal from '@/components/ApiKeyModal.vue'

export default {
  data () {
    return {
      apiKey: [],
      generatedApiKey: null
    }
  },
  components: {
    ApiKeyModal
  },

  methods: {
    generateApiKey () {
      // Make API call to generate API key
      axios.post('http://127.0.0.1:5000/auth/generate-api-key')
        .then(response => {
          this.apiKey = response.data
        })
        .catch(error => {
          console.error('Could not generate api key:', error)
        })
      console.log(this.apiKey)
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
.key {
  font-size: 1.6rem;
  font-weight: 300;
}
</style>
